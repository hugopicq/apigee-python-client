from dataclasses import dataclass, field
from apigee_python_client.api_client.api_client import APIClient
import logging
from typing import List, Any
import apigee_python_client.extractor as extractor

import apigee_python_client.models as models


logger = logging.getLogger(__name__)


@dataclass
class EnvironmentClient:
    api_client: APIClient = field(init=True)

    def list_environments(self, organisation: str) -> List[str]:
        """
        Get the list of environments for a given organization.

        :param: organisation: the GCP project
        :returns: a string list corresponding to the list of environments
        """

        url = f"/organizations/{organisation}/environments"
        response = self.api_client.get_request_json(url)
        if not response:
            return []

        return response

    def list_environment_deployments(self, organisation: str, environment: str) -> List[models.ProxyDeployment]:
        """
        Gets the list of deployments for a given organization and an environment.

        :param: organisation: the GCP project
        :param: environment: the Apigee environment
        :returns: a list of models.ProxyDeployment
        """

        url = f"/organizations/{organisation}/environments/{environment}/deployments"
        response = self.api_client.get_request_json(url)

        if not response:
            return []

        response_typed: models.GetProxyDeploymentsResponse = extractor.extract_as_object(
            response, models.GetProxyDeploymentsResponse
        )

        return response_typed.deployments

    def list_environment_targets(self, organisation: str, environment: str) -> List[str]:
        """
        Gets the list of target servers in an environment for a given org.

        :param: organisation: the GCP project
        :param: environment: the Apigee environment
        :returns: a list of str corresponding to the names of target servers.
        """

        url = f"/organizations/{organisation}/environments/{environment}/targetservers"
        response = self.api_client.get_request_json(url)
        if not response:
            return []

        return response

    def get_environment_target(self, organisation: str, environment: str, target: str) -> models.TargetServer:
        """
        Gets the details of a target server for an environment.

        :param: organisation: the GCP project
        :param: environment: the Apigee environment
        :param: target: the name of the target server
        :returns: an instance of models.TargetServer with informations corresponding to the TargetServer
        """

        url = f"/organizations/{organisation}/environments/{environment}/targetservers/{target}"
        response = self.api_client.get_request_json(url)
        if not response:
            return None

        response_typed: models.TargetServer = extractor.extract_as_object(response, models.TargetServer)

        return response_typed

    def list_environment_groups(self, organisation: str) -> List[models.EnvironmentGroup]:
        """
        Gets the list of environment groups for a given organization.

        :param: organisation: the GCP project
        :returns: a list of models.EnvironmentGroup.
        """

        url = f"/organizations/{organisation}/envgroups"
        response = self.api_client.get_request_json(url)
        if not response:
            return []

        response_typed: models.GetEnvironmentGroupsResponse = extractor.extract_as_object(
            response, models.GetEnvironmentGroupsResponse
        )

        return response_typed.environmentGroups

    def get_hosts_by_env(self, organisation: str) -> dict[str, List[str]]:
        """
        Gets the list of hosts for an orgnization.

        :param: organisation: the GCP project
        :returns: a dictionary with environment name as key and list of hostnames for values.
        """

        env_groups = self.list_environment_groups(organisation)
        urls_by_env = {}

        for env_group in env_groups:
            url = f"/organizations/{organisation}/envgroups/{env_group.name}/attachments"
            group_attachments = self.api_client.get_request_json(url)

            if not group_attachments:
                continue

            for group_attachment in group_attachments["environmentGroupAttachments"]:
                if group_attachment["environment"] not in urls_by_env:
                    urls_by_env[group_attachment["environment"]] = env_group.hostnames.copy()
                else:
                    urls_by_env[group_attachment["environment"]] += env_group.hostnames.copy()

        return urls_by_env
