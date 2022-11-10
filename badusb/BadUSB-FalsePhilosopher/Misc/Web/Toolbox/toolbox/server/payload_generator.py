from flask import (
    Blueprint,
    Flask,
    render_template,
    make_response,
    app,
    abort,
    current_app,
    request,
    redirect,
    url_for,
)
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from pathlib import Path
from .interfaces import get_ip_address, is_valid_ipv4_address, allowed_interfaces
from urllib.parse import urlparse

TEMPLATE_DIRECTORY = Path(__file__).parent / "templates"
MODULE_DIRECTORY = TEMPLATE_DIRECTORY / "modules"


@dataclass
class DataStore:
    lhost: str
    lport: int
    srvhost_domain: str
    srvhost_port: str
    srvhost_url: str


class PayloadGenerator:
    VALID_INTERFACES = ["tun0", "tun1", "lo", "lo0"]

    def __init__(self):
        pass

    def generate(
        self, name: str, lhost: Optional[str], lport: Optional[str]
    ) -> Optional[str]:
        if name not in self:
            return None

        # TODO: Decide if it would be better to remove render_template and call jinja or similar directly
        payload = render_template(
            f"modules/{name}", datastore=self._get_datastore(lhost, lport)
        )
        return payload

    def __contains__(self, name):
        return name in self.module_names

    @property
    def module_names(self):
        # TODO: Decide if this should honor jinja's templates_auto_reload mechanism
        return [module.name for module in Path(MODULE_DIRECTORY).iterdir()]

    @property
    def default_lport(self) -> int:
        return 4444

    @property
    def default_lhost(self) -> str:
        for interface in allowed_interfaces():
            result = get_ip_address(interface)
            if result is not None:
                return result
        raise ValueError(
            f"Unable to get ip address for default interfaces: '{str.join(allowed_interfaces(), ', ')}'"
        )

    def _get_datastore(self, lhost: Optional[str], lport: Optional[str]) -> DataStore:
        srvhost_url = request.host_url
        srvhost_parsed = urlparse(srvhost_url)

        return DataStore(
            lhost=(lhost if lhost else self.default_lhost),
            lport=(int(lport) if lport else self.default_lport),
            srvhost_domain=srvhost_parsed.hostname,
            srvhost_port=srvhost_parsed.port,
            srvhost_url=srvhost_url,
        )

    def _get_lhost(self, lhost: Optional[str]) -> str:
        if lhost is None:
            return self.default_lhost()

        if lhost in allowed_interfaces():
            address = get_ip_address(lhost)
            if address is None:
                raise ValueError(f"interface not found: '{lhost}'")
            return address

        if is_valid_ipv4_address(lhost):
            return lhost

        raise ValueError(f"Unexpected lhost: '{lhost}'")
