from apigee_python_client.api_client.api_client import APIClient
from dataclasses import dataclass, field

import logging

from apigee_python_client.clients.kvm_client import KVMClient
from apigee_python_client.clients.proxy_client import ProxyClient
from apigee_python_client.clients.environment_client import EnvironmentClient
from apigee_python_client.clients.stats_client import StatsClient

from apigee_python_client import constants


logger = logging.getLogger(__name__)


@dataclass
class ApigeeClient:
    """
    Client pour les requêtes Apigee au travers des sous-clients de la classe (kvm_client, proxy_client, etc.)
    """

    api_client: APIClient = field(init=False, default=APIClient(constants.APIGEE_API_URL))

    def __post_init__(self):
        self.kvm_client = KVMClient(self.api_client)
        self.proxy_client = ProxyClient(self.api_client)
        self.environment_client = EnvironmentClient(self.api_client)
        self.stats_client = StatsClient(self.api_client)