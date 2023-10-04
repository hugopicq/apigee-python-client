from dataclasses import dataclass, field
from apigee_python_client.api_client.api_client import APIClient
import apigee_python_client.models as models
import logging
from typing import List, Any
import apigee_python_client.extractor as extractor


logger = logging.getLogger(__name__)


@dataclass
class KVMClient:
    api_client: APIClient = field(init=True)

    def list_proxy_kvms(self, organisation: str, proxy: str) -> List[str]:
        """
        Récupère la liste des Key Value Maps pour un proxy

        :param: organisation: l'organisation (le projet)
        :param: proxy: le nom du proxy
        :returns: la liste des noms des KVMs sur le proxy
        """

        url = f"/organizations/{organisation}/apis/{proxy}/keyvaluemaps"

        response = self.api_client.get_request_json(url)
        if not response:
            return []

        return response

    def list_proxy_kvm_entries(self, organisation: str, proxy: str, kvm: str) -> List[models.KVMEntry]:
        """
        Récupère la liste des entrées pour une KVM d'un proxy

        :param: organisation: l'organisation (le projet)
        :param: proxy: le nom du proxy
        :param: kvm: le nom de la KVM
        :returns: la liste des entrées (clé/valeur) pour la KVM
        """

        url = f"/organizations/{organisation}/apis/{proxy}/keyvaluemaps/{kvm}/entries"

        response = self.api_client.get_request_json(url)
        if not response:
            return []

        response: models.GetKVMEntriesResponse = extractor.extract_as_object(response, models.GetKVMEntriesResponse)

        return response.keyValueEntries

    def get_proxy_kvm_entry(self, organisation: str, proxy: str, kvm: str, entry_name: str) -> str:
        """
        Récupère la valeur d'une entrée d'une KVM

        :param: organisation: l'organisation (le projet)
        :param: proxy: le nom du proxy
        :param: kvm: le nom de la KVM
        :param: entry_name: le nom de l'entrée
        :returns: la valeur de l'entrée
        """

        url = f"/organizations/{organisation}/apis/{proxy}/keyvaluemaps/{kvm}/entries/{entry_name}"
        response = self.api_client.get_request_json(url)

        if not response:
            return ""

        response: models.KVMEntry = extractor.extract_as_object(response, models.KVMEntry)

        return response.value

    def create_proxy_kvm_if_not_exists(self, organisation: str, proxy: str, kvm: str):
        """
        Crée une KVM de proxy si celle-ci n'existe pas

        :param organisation: l'organisation (le projet)
        :param proxy: le nom de proxy
        :param: kvm: le nom de la KVM
        """

        url = f"/organizations/{organisation}/apis/{proxy}/keyvaluemaps"

        kvms = self.api_client.get_request_json(url)
        if kvm not in kvms:
            logger.debug("Creation de la kvm: " + kvm)
            payload = {"name": kvm, "encrypted": True}
            self.api_client.post_request(url, payload)
        else:
            logger.debug(f"KVM {kvm} already exists")

    def create_or_update_proxy_kvm_entry(
        self, organisation: str, proxy: str, kvm: str, entry_name: str, entry_value: str
    ):
        """
        Crée ou met à jour une entrée dans une KVM de proxy

        :param organisation: l'organisation (le projet)
        :param proxy: le nom de proxy
        :param: kvm: le nom de la KVM
        :param entry_name: le nom de l'entrée
        :param entry_value: la valeur de l'entrée
        """

        entry = models.KVMEntry(name=entry_name, value=entry_value)

        entries_url = f"/organizations/{organisation}/apis/{proxy}/keyvaluemaps/{kvm}/entries"
        entry_url = f"{entries_url}/{entry.name}"

        existing_entry = self.api_client.get_request_json(entry_url)
        existing_entry: models.KVMEntry = extractor.extract_as_object(existing_entry, models.KVMEntry)

        if existing_entry and existing_entry.value != entry.value:
            logger.debug("Suppression de la valeur précédente")
            self.api_client.delete_request(entry_url)
            existing_entry = None

        if not existing_entry:
            logger.debug("Mise à jour de l'entrée " + entry.name)
            self.api_client.post_request(entries_url, entry.model_dump())
        else:
            logger.info("La valeur de l'entrée " + entry.name + " déjà présente est identique à celle fournie")

    def list_environment_kvms(self, organisation: str, environment: str) -> List[str]:
        """
        Récupère la liste des KVM pour un environnement

        :param organisation: l'organisation (le projet)
        :param environment: l'environnement
        :returns: la liste des noms des KVMs
        """

        url = f"/organizations/{organisation}/environments/{environment}/keyvaluemaps"

        response = self.api_client.get_request_json(url)
        if not response:
            return []

        return response

    def list_environment_kvm_entries(self, organisation: str, environment: str, kvm: str) -> List[models.KVMEntry]:
        """
        Récupère la liste des entrées pour une KVM d'un environnement

        :param organisation: l'organisation (le projet)
        :param environment: l'environnement
        :param kvm: le nom de la KVM
        :returns: la liste des entrées pour la KVM
        """

        url = f"/organizations/{organisation}/environments/{environment}/keyvaluemaps/{kvm}/entries"

        response = self.api_client.get_request_json(url)
        if not response:
            return []

        response: models.GetKVMEntriesResponse = extractor.extract_as_object(response, models.GetKVMEntriesResponse)

        return response.keyValueEntries
