import logging
import google.auth
from google.auth.transport import requests
from requests import JSONDecodeError
from typing import Any


logger = logging.getLogger(__name__)


def get_google_session() -> requests.AuthorizedSession:
    """
    Get the current Google session for application default (authenticated with gcloud CLI)

    :returns: the session
    """

    credentials, project = google.auth.default()
    return requests.AuthorizedSession(credentials)


class APIClient:
    """
    Client to perform Apigee API requests to Google APIs using google session

    :param base_url: the base Apigee URL
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = get_google_session()

    def _build_url(self, path: str):
        """
        Builds the complete URL by appending the path in param to the base url

        :param path: the subpath which will be appended to the base URL (str)
        :returns: the complete URL to which make the request
        """

        path = "/" + path.lstrip("/")
        return self.base_url + path

    def _get_request(self, path: str):
        """
        Performs a raw GET request with the current Google session. 404 errors are ignored and None is returned.
        This function is not te be called externally.

        :param path: the subpath to which make the request (ex: /organization/{organisation}/environments)
        :returns: the result of the get request or None
        """

        complete_url = self._build_url(path)

        logger.debug("GET " + complete_url)

        result = self.session.get(self.base_url + path)

        logging.debug("GET status code: " + str(result.status_code))
        logging.debug("GET body: " + result.text)

        if result.status_code == 404:
            logger.warning("GET request resource not found (%s)", path)
            return None
        elif result.status_code > 399:
            logger.error("GET request error occured: %s", result.text)
            result.raise_for_status()

        return result

    def post_request(self, path: str, body):
        """
        Performs a raw POST request with the current Google session.

        :param path: the subpath to which make the request (ex: /organization/{organisation}/environments)
        :param body: the body of the request (usually a dictionary)
        :returns: nothing
        """

        complete_url = self._build_url(path)

        logger.debug("POST " + complete_url)

        result = self.session.post(complete_url, json=body)

        logging.debug("POST status code: " + str(result.status_code))
        logging.debug("POST body: " + result.text)

        if result.status_code > 399:
            logging.error("POST request error occured: %s", result.text)
            result.raise_for_status()

    def delete_request(self, path: str):
        """
        Performs a raw DELETE request with the current Google session

        :param path: the subpath to which make the request (ex: /organization/{organisation}/environments)
        :returns: nothing
        """

        complete_url = self._build_url(path)

        logger.debug("DELETE " + complete_url)

        result = self.session.delete(complete_url)

        logging.debug("DELETE status code: " + str(result.status_code))
        logging.debug("DELETE body: " + result.text)

        if result.status_code > 399:
            logging.error("DELETE request error occured: %s", result.text)
            result.raise_for_status()

        return result

    def get_request_bytes(self, path: str) -> bytes:
        """
        Performs a GET request with the current Google session. 404 errors are ignored and an empty bytes() is returned.

        :param path: the subpath to which make the request (ex: /organization/{organisation}/environments)
        :returns: the result of the get request in bytes
        """

        result = self._get_request(path)

        return bytes() if result is None else result.content

    def get_request_json(self, path: str) -> Any:
        """
        Performs a GET request with the current Google session and calls .json() on the result which is returned. 404 errors are ignored and None is returned.

        :param path: the subpath to which make the request (ex: /organization/{organisation}/environments)
        :returns: the result of the get request (usually a dict or a list)
        """

        result = self._get_request(path)

        if result is None:
            return None

        result_json = result.json()

        return result_json
