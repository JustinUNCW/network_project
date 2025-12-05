from ipaddress import IPv4Address
from typing import Dict, Optional
from app.models.pod_model import Pod, Device, Network, Location, AccessMethod


class PodDB:
    def __init__(self):
        # lab_id -> pod_id -> Pod
        self.pods_by_id: Dict[str, Dict[str, Pod]] = {}
        # lab_id -> pod_id -> list[IPv4Address]
        self.pod_ip_list: Dict[str, Dict[str, list[IPv4Address]]] = {}

    # ---------- internal helpers ----------

    def _get_pod_or_none(self, lab_id: str, pod_id: str) -> Optional[Pod]:
        lab_pods = self.pods_by_id.get(lab_id)
        if lab_pods is None:
            return None
        return lab_pods.get(pod_id)

    def _get_ip_list(self, lab_id: str, pod_id: str) -> list[IPv4Address]:
        """Ensure nested dicts exist and return the IP list for this pod."""
        lab_map = self.pod_ip_list.setdefault(lab_id, {})
        return lab_map.setdefault(pod_id, [])

    def _track_pod_ip_addresses(
        self,
        lab_id: str,
        pod_id: str,
        ip: IPv4Address | None = None,
        pod_override: Pod | None = None,
    ) -> bool:
        """
        Helper to keep track of used IPs for a pod.
        - If ip is None: rebuild from pod.assets or pod_override.assets
        - If ip is not None: check if it's already used, and record it if not.
        """
        pod = pod_override or self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return False

        ip_list = self._get_ip_list(lab_id, pod_id)

        # Full rebuild: check all devices' primary IPs for duplicates
        if ip is None:
            ip_list.clear()
            for device in pod.assets:
                if not device.ports:
                    continue
                addr = device.ports[0].interface.address
                if addr in ip_list:
                    return False
                ip_list.append(addr)
            return True

        # Single IP add
        if ip in ip_list:
            return False
        ip_list.append(ip)
        return True

    # ---------- read methods ----------

    def get_pod_by_id(self, lab_id: str, pod_id: str) -> Optional[Pod]:
        return self._get_pod_or_none(lab_id, pod_id)

    def get_pod_devices(self, lab_id: str, pod_id: str) -> list[Device]:
        pod = self._get_pod_or_none(lab_id, pod_id)
        return pod.assets if pod is not None else []

    def get_pod_device_by_id(self, lab_id: str, pod_id: str, device_id: str) -> Optional[Device]:
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return None
        for device in pod.assets:
            if device.id == device_id:
                return device
        return None

    def get_pod_location(self, lab_id: str, pod_id: str) -> Optional[Location]:
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None or not pod.assets:
            return None
        return pod.assets[0].location

    def get_pod_network(self, lab_id: str, pod_id: str) -> Optional[Network]:
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None or not pod.assets:
            return None
        first_device = pod.assets[0]
        if not first_device.ports:
            return None
        return first_device.ports[0].interface.parent

    # ---------- write methods ----------

    def create_pod(self, lab_id: str, pod: Pod) -> bool:
        """Create a pod entry under a lab."""
        lab_pods = self.pods_by_id.setdefault(lab_id, {})
        if pod.id in lab_pods:
            return False   # pod_id already exists

        # Check all IPs for duplicates before storing pod
        if not self._track_pod_ip_addresses(lab_id, pod.id, ip=None, pod_override=pod):
            return False

        lab_pods[pod.id] = pod
        return True

    def create_device(self, lab_id: str, pod_id: str, device: Device) -> bool:
        """Create a new device within a pod. Returns False if pod not found or IP duplicate."""
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return False

        if device.ports:
            new_ip = device.ports[0].interface.address
            if not self._track_pod_ip_addresses(lab_id, pod_id, ip=new_ip):
                return False

        pod.assets.append(device)
        return True

    def update_pod(self, lab_id: str, pod: Pod) -> bool:
        """Replace a pod by id."""
        # Check IPs using the new pod definition first
        if not self._track_pod_ip_addresses(lab_id, pod.id, ip=None, pod_override=pod):
            return False

        lab_pods = self.pods_by_id.setdefault(lab_id, {})
        lab_pods[pod.id] = pod
        return True

    def update_device_ip(self, lab_id: str, pod_id: str, device_id: str, ip: IPv4Address) -> bool:
        """Update a pod device's IP address. Returns True if updated, False otherwise."""
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return False

        device = self.get_pod_device_by_id(lab_id, pod_id, device_id)
        if device is None or not device.ports:
            return False

        current_ip = device.ports[0].interface.address

        # No change: trivially okay
        if ip == current_ip:
            return True

        # Check if new IP is free for this pod
        if not self._track_pod_ip_addresses(lab_id, pod_id, ip):
            return False

        # Update device IP and clean up old IP in index
        device.ports[0].interface.address = ip
        ip_list = self._get_ip_list(lab_id, pod_id)
        try:
            ip_list.remove(current_ip)
        except ValueError:
            # If it's somehow missing, just ignore
            pass
        return True

    def update_device_name(self, lab_id: str, pod_id: str, device_id: str, name: str) -> bool:
        device = self.get_pod_device_by_id(lab_id, pod_id, device_id)
        if device is None:
            return False
        device.name = name
        return True

    def update_device_access_method(
        self,
        lab_id: str,
        pod_id: str,
        device_id: str,
        access_method: AccessMethod,
    ) -> bool:
        device = self.get_pod_device_by_id(lab_id, pod_id, device_id)
        if device is None or not device.accessMethods:
            return False
        device.accessMethods[0] = access_method
        return True

    def update_pod_devices_network(self, lab_id: str, pod_id: str, network: Network) -> bool:
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return False
        for device in pod.assets:
            for port in device.ports:
                port.interface.parent = network
        return True

    def update_pod_devices_location(self, lab_id: str, pod_id: str, location: Location) -> bool:
        pod = self._get_pod_or_none(lab_id, pod_id)
        if pod is None:
            return False
        for device in pod.assets:
            device.location = location
        return True
