try:
    import netifaces
    MissingDependencies = False
except ModuleNotFoundError:
    MissingDependencies = True

import ipaddress
from typing import Optional

class NoopImplementation:
    def allowed_interfaces(self):
        return ["lo"]

    def get_ip_address(self, interface: str) -> Optional[str]:
        return "127.0.0.1"

    def is_valid_ipv4_address(self, ip: str) -> bool:
        return True

class NetifacesImplementation:
    def allowed_interfaces(self):
        return ["tun0", "tun1", "lo", "lo0"]

    def get_ip_address(self, interface: str) -> Optional[str]:
        try:
            return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["addr"]
        except (KeyError, ValueError):
            return None

    def is_valid_ipv4_address(self, ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False


if MissingDependencies:
    implementation = NoopImplementation()
else:
    implementation = NetifacesImplementation()

def allowed_interfaces():
    return implementation.allowed_interfaces()

def get_ip_address(interface: str) -> Optional[str]:
    return implementation.get_ip_address(interface)

def is_valid_ipv4_address(ip: str) -> bool:
    return implementation.is_valid_ipv4_address(ip)
