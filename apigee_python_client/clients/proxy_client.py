from dataclasses import dataclass, field
from apigee_python_client.api_client.api_client import APIClient
import logging
from typing import List, Any
import zipfile
from io import BytesIO
import apigee_python_client.extractor as extractor

import apigee_python_client.models as models


logger = logging.getLogger(__name__)


@dataclass
class ProxyClient:
    api_client: APIClient = field(init=True)

    def list_proxies(self, organisation: str) -> List[models.ApiProxy]:
        """
        Récupère la liste des proxies

        :param organisation: l'organisation (le projet)
        :returns: la liste des noms des KVMs
        """

        url = f"/organizations/{organisation}/apis"

        response = self.api_client.get_request_json(url)
        if not response:
            return []

        response_typed: models.GetProxiesResponse = extractor.extract_as_object(response, models.GetProxiesResponse)

        return response_typed.proxies

    def list_proxy_deployments(self, organisation: str, proxy_name: str) -> List[models.ProxyDeployment]:
        """
        Récupère la liste des deployments pour un proxy

        :param organisation: l'organisation (le projet)
        :param proxy_name: le nom du proxy
        :returns: la liste des deployments
        """

        url = f"/organizations/{organisation}/apis/{proxy_name}/deployments"

        response: models.GetProxyDeploymentsResponse = self.api_client.get_request_json(url)

        if not response:
            return []

        response_typed: models.GetProxyDeploymentsResponse = extractor.extract_as_object(
            response, models.GetProxyDeploymentsResponse
        )

        return response_typed.deployments

    def undeploy_proxy(self, organisation: str, environment: str, proxy_name: str, revision: str):
        """
        Undeploy le proxy spécifié sur l'environnement

        :param organisation: l'organisation (le projet)
        :param environment: le nom de l'environnement
        :param proxy_name: le nom du proxy
        :param revision: la revision à undeploy
        """

        url = f"/organizations/{organisation}/environments/{environment}/apis/{proxy_name}/revisions/{revision}/deployments"

        self.api_client.delete_request(url)

    def get_proxy_bundle_for_environment(self, organisation: str, proxy_name: str, environment: str) -> zipfile.ZipFile:
        """
        Récupère le bundle de la revision déployée sur l'environnement donné pour un proxy

        :param organisation: l'organisation (le projet)
        :param proxy_name: le nom du proxy
        :param environment: le nom de l'environnement
        :returns: le bundle de la révision déployée ou None si le proxy n'est pas déployé sur l'environnement
        """

        deployments = self.list_proxy_deployments(organisation, proxy_name)

        if not deployments or len(deployments) == 0:
            return None

        deployment = next(iter([d for d in deployments if d.environment == environment]), None)

        if not deployment:
            return None

        url = f"/organizations/{organisation}/apis/{proxy_name}/revisions/{deployment.revision}?format=bundle"

        bundle = self.api_client.get_request_bytes(url)

        if not bundle:
            return None

        return zipfile.ZipFile(BytesIO(bundle))

    def get_revisions_by_env(self, organisation, proxy_name) -> dict[str, Any]:
        """
        Récupère la liste des révisions par environnement

        :param organisation: l'organisation (le projet)
        :param proxy_name: le nom du proxy
        :returns: un dictionnaire avec la clé qui correspond à l'environnement et la valeur est le détail de la révision
        """

        deployments = self.list_proxy_deployments(organisation, proxy_name)

        proxies_by_env: dict[str, Any] = {}

        proxies_by_revision = {}
        revisions = list(set([x.revision for x in deployments]))

        for revision in revisions:
            url = f"/organizations/{organisation}/apis/{proxy_name}/revisions/{str(revision)}"
            revision_details = self.api_client.get_request_json(url)
            proxies_by_revision[revision] = revision_details

        for deployment in deployments:
            proxies_by_env[deployment.environment] = proxies_by_revision[deployment.revision]

        return proxies_by_env
