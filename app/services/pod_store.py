from uuid import uuid4
from ipaddress import IPv4Address
from typing import Dict
from app.models.pod_model import *
from app.Exceptions.exceptions import *


class PodDB:
    def __init__(self):
        # lab_id -> pod_id -> Pod
        self.pods_by_id: Dict[str, Dict[str, PodExists]] = {}
        # lab_id -> pod_id -> set[IPv4Address]
        self.pod_ip_list: Dict[str, Dict[str, set[IPv4Address]]] = {}

    # ---------- internal helpers ----------

    def _init_pod(self, lab_id: str) -> str:
        """Initialize a pod in pods_by_id and pod_ip_list db's.

        Args:
            lab_id: Identifier of the lab to place the pod in. 

        Returns:
            a UUID representing the pod id.
    """
        pod_id = str(uuid4())
        self.pods_by_id.get(lab_id).setdefault(pod_id, {})
        self.pod_ip_list.get(lab_id).setdefault(pod_id, set())
        return pod_id
    
    def _init_device(self) -> str: 
        """Initialize a pod in pods_by_id and pod_ip_list db's.

        Args:
            lab_id: Identifier of the lab to place the pod in. 

        Returns:
            a UUID representing the pod id.
    """
        device_id = str(uuid4())

        return device_id

    def _init_lab(self) -> str: 
        """Initialize a lab in pods_by_id and pod_ip_list db's.

        Returns:
            a UUID representing the lab id.
    """
        lab_id = str(uuid4())
        self.pods_by_id.setdefault(lab_id, {})
        self.pod_ip_list.setdefault(lab_id, {})
        return lab_id
    
    def _get_device_or_error(self, assets, device_id: str) -> DeviceCreate:
        """Return a pods existing device by id.
        Args: 
            assets: A pods devices
            device_id: A device identifier

        Returns:
            a DeviceCreate object
        """
        try: 
           return assets[device_id]
        except KeyError:
            raise DeviceNotFoundError({'detail': f'Device {device_id} not found'})

    def _get_lab_or_error(self, lab_id) -> Dict:
        """Check if a lab exists and return it.

        Args:
            lab_id: Identifier of the lab.

        Returns:
            A pod object. 

        Raises:
            LabNotFoundError: If the lab does not exist.
        """
        try:
            lab = self.pods_by_id[lab_id]
            return lab
        except KeyError:
            raise LabNotFoundError({'detail': f"Lab {lab_id} not found"})

    def _get_pod_or_error(self, lab_id: str, pod_id: str) -> dict[str, dict[str, DeviceExists]]:
        """Check if a pod exists and return it.

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod

        Returns:
            A PodExists object. 

        Raises:
            LabNotFoundError: If the lab does not exist.
            PodNotFoundError: If the pod does not exist.
        """
        lab_pods = self._get_lab_or_error(lab_id)

        try:
            return lab_pods[pod_id]
        except KeyError:
            raise PodNotFoundError({'detail': f"Pod {pod_id} not found"})

    def _get_ip_set(self, lab_id: str, pod_id: str) -> set[IPv4Address]:
        """Return a pods list of used ip's.

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod

        Returns:
            A set of IPv4Addresses
        """
        return self.pod_ip_list[lab_id][pod_id]

    def _track_pod_ip_addresses(
        self,
        lab_id: str | None = None,
        pod_id: str | None = None,
        ip: IPv4Address | None = None,
        assets: list[DeviceCreate] | None = None,
    ):
        """Check if a newly created pod has duplicate IP's or if a singular IP
        for a newly created device for a pod has a duplicate IP. 

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod
            ip: the IP for a newly created device
            assets: a list of pod devices

        Returns:
            bool 

        Raises:
            LabNotFoundError: If the lab does not exist.
            PodNotFoundError: If the pod does not exist.
            DuplicateIPv4Error: If a pod device has a duplicate IP
        """
        temp_ip_set = set()
        
        # Full rebuild: check all devices' primary IPs for duplicates
        if ip is None:
            for device in assets:
                if not device.ports:
                    continue
                addr = device.ports[0].interface.address
                if addr in temp_ip_set:
                    DuplicateIPv4Error("Duplicate IPv4 addresses not allowed")
                temp_ip_set.add(addr)
            
            return temp_ip_set
            
        
        ip_set = self._get_ip_set(lab_id, pod_id)

        # Single IP add
        if ip in ip_set:
            raise DuplicateIPv4Error("Duplicate IPv4 addresses not allowed")


    # ---------- get methods ----------

    def get_pod_by_id(self, lab_id: str, pod_id: str) -> PodExists:
        """Get a pod

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod

        Returns:
            A PodExists object 

        Raises:
            LabNotFoundError: If the lab does not exist.
            PodNotFoundError: If the pod does not exist.
        """
        pod = self._get_pod_or_error(lab_id, pod_id)
        return PodExists(id=pod_id, 
                         assets=[
                             DeviceExists.model_validate({'id': device_id, **device})
                         for device_id, device in pod['assets'].items()])

    def get_pod_devices(self, lab_id: str, pod_id: str) -> list[DeviceExists]:
        """Get a pods devices

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod

        Returns:
            A list of DeviceExists objects

        Raises:
            LabNotFoundError: If the lab does not exist.
            PodNotFoundError: If the pod does not exist.
        """
        pod = self._get_pod_or_error(lab_id, pod_id)
        return [DeviceExists.model_validate({'id': device_id, **device})
                         for device_id, device in pod['assets'].items()]

    def get_pod_device_by_id(
        self,
        lab_id: str,
        pod_id: str,
        device_id: str,
    ) -> DeviceExists:
        """Get a pod device

        Args:
            lab_id: Identifier of the lab.
            pod_id: Identifier of the pod
            device_id: Identifier of a pod device

        Returns:
            A DeviceExists object

        Raises:
            LabNotFoundError: If the lab does not exist.
            PodNotFoundError: If the pod does not exist.
        """
        pod = self._get_pod_or_error(lab_id, pod_id)
        device = self._get_device_or_error(pod['assets'], device_id)
        return DeviceExists.model_validate({'id': device_id, **device})

    def get_pod_network(self, lab_id: str, pod_id: str) -> IPv4Network:
        """Return derived pod network (first device's first port's parent), or None."""
        pod = self._get_pod_or_error(lab_id, pod_id)
        if pod.get('assets') == []:
            return None
        first_device = next(iter(pod['assets'].values()))
        if not first_device['ports']:
            return None
        return first_device['ports'][0]['interface']['parent']['network']

    def get_all_pod_ip(self, lab_id: str, pod_id: str) -> list[IPv4Address]:
        """Return all IPs used in this pod (sorted)."""
        return sorted(self._get_ip_set(lab_id, pod_id))

    def get_free_pod_ip(self, lab_id: str, pod_id: str) -> list[IPv4Address]:
        """Return all unused IPs in the pod's network."""

        net:IPv4Network = self.get_pod_network(lab_id, pod_id)
        if net is None:
            return []

        usable = set(net.hosts())
        used = set(self.get_all_pod_ip(lab_id, pod_id))

        return sorted(usable - used)

    # ---------- post methods ----------

    def create_pod(self, lab_id: str, pod: PodCreate) -> DeviceExists:
        """Create a pod entry under a lab.

        Raises:
            LabNotFoundError
            DuplicateIPv4Error
        """
        lab_pods = self._get_lab_or_error(lab_id)

        pod_id = self._init_pod(lab_id)

        lab_pods[pod_id]['assets'] = {}

        list_of_devices = []

        for device in pod.assets: 
            device_exists = self.create_device(lab_id, pod_id, device)
            list_of_devices.append(device_exists)
            lab_pods[pod_id]['assets'][device_exists.id] = device.model_dump()

        return PodExists(id=pod_id, 
                         assets=list_of_devices
                         )
    
    def create_device(self, lab_id: str, pod_id: str, device: DeviceCreate) -> DeviceExists:
        """Create a new device within a pod.

        Returns:
            A DeviceExists object

        Raises: 
            LabNotFoundError
            PodNotFoundError
            DuplicateIPv4Error
        """
        pod: PodCreate = self._get_pod_or_error(lab_id, pod_id)

        if device.ports:
            new_ip = device.ports[0].interface.address
            self._track_pod_ip_addresses(lab_id=lab_id, pod_id=pod_id, ip=new_ip)
            self.pod_ip_list[lab_id][pod_id].add(new_ip)
        
        device_id = self._init_device()

        return DeviceExists.model_validate({'id': device_id, **device})

    # ---------- patch methods ----------

    def patch_device_ip(
        self,
        lab_id: str,
        pod_id: str,
        device_id: str,
        ip: IPv4Address,
    ) -> DeviceExists:
        """Update a pod device's IP address.

        Returns:
            True if updated (or unchanged).
            False if the new IP would clash or the device/ports are missing.
        """

        device = self.get_pod_device_by_id(lab_id, pod_id, device_id)
        if not device.ports:
            return False

        current_ip = device.ports[0]['interface']['address']

        # No change
        if ip == current_ip:
            return True

        # Check if new IP is free for this pod
        self._track_pod_ip_addresses(lab_id, pod_id, ip)

        # Update device IP and clean up old IP in index
        device.ports[0]['interface']['address'] = ip
        ip_set = self._get_ip_set(lab_id, pod_id)
        # discard avoids ValueError if it's missing
        ip_set.discard(current_ip)
        return DeviceExists.model_validate({'id': device_id, **device})

    def patch_device_name(
        self,
        lab_id: str,
        pod_id: str,
        device_id: str,
        name: str,
    ) -> DeviceExists:
        """Patch a device's name."""

        pod = self._get_pod_or_error(lab_id, pod_id)

        device = self._get_device_or_error(pod['assets'], device_id)

        device[name] = name

        return DeviceExists.model_validate({'id': device_id, **device})

    def patch_device_access_method(
        self,
        lab_id: str,
        pod_id: str,
        device_id: str,
        access_method: AccessMethod,
    ) -> DeviceExists:
        """Patch a device's first access method."""
        pod = self._get_pod_or_error(lab_id, pod_id)

        device = self._get_device_or_error(pod['assets'], device_id)

        device['accessMethods'][0] = access_method

        return DeviceExists.model_validate({'id': device_id, **device})

    def patch_pod_devices_network(
        self,
        lab_id: str,
        pod_id: str,
        network: Network,
    ) -> list[DeviceExists]:
        """Patch all devices in a pod to use the given network."""
        pod = self._get_pod_or_error(lab_id, pod_id)
        for device in pod['assets'].keys():
            for port in device['ports']:
                port['interface']['parent'] = network
        return [DeviceExists.model_validate({'id': device_id, **device})
                         for device_id, device in pod['assets'].items()]
    
    def patch_pod_devices_location(
        self,
        lab_id: str,
        pod_id: str,
        location: Location,
    ) -> list[DeviceExists]:
        """Patch all devices in a pod to share the same location."""
        pod = self._get_pod_or_error(lab_id, pod_id)
        for device in pod['assets'].keys():
            device['location'] = location
        return [DeviceExists.model_validate({'id': device_id, **device})
                         for device_id, device in pod['assets'].items()]

    # ---------- delete methods ----------

    def delete_lab_and_pod(
            self, 
            lab_id: str
    ) -> bool:
        """delete a lab and it's pods"""
        self._get_lab_or_error(lab_id)
        del self.pods_by_id[lab_id]
        del self.pod_ip_list[lab_id]
        return True
    
    def delete_pod(
        self, 
        lab_id: str,
        pod_id: str
    ) -> bool:
        """delete a pod"""
        self._get_pod_or_error(lab_id, pod_id)
        del self.pods_by_id[lab_id][pod_id]
        del self.pod_ip_list[lab_id][pod_id]
        return True
    
    def delete_device(
            self, 
            lab_id: str, 
            pod_id: str, 
            device_id: str
    ) -> bool:
        """delete a device from a pod"""
        pod = self._get_pod_or_error(lab_id, pod_id)

        device = self._get_device_or_error(pod['assets'], device_id)
        addr = device.ports[0].interface.address
        
        del pod['assets'][device_id]

        self._get_ip_set(lab_id, pod_id).remove(addr)

        return True