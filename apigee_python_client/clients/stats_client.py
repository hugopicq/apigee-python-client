from dataclasses import dataclass, field
from apigee_python_client.api_client.api_client import APIClient
import logging
from typing import List, Any
import zipfile
from io import BytesIO
import apigee_python_client.extractor as extractor
from datetime import datetime

import apigee_python_client.models as models


logger = logging.getLogger(__name__)


@dataclass
class StatsClient:
    api_client: APIClient = field(init=True)

    def get_environment_stats(
        self,
        organisation: str,
        environment: str,
        dimension: str,
        metric: str,
        from_time: datetime,
        to_time: datetime = datetime.now(),
        time_unit: str = "day",
    ) -> models.EnvironmentStat:
        """
        Récupère les statistiques pour un environnement selon une dimension, pour une ou plusieurs métriques sur une plage de temps donnée

        :param dimension: dimension à sélectionner type "apiproxy". Pour plus d'informations voir https://cloud.google.com/apigee/docs/api-platform/analytics/analytics-reference#dimensions
        :param metric: liste de métriques (séparées par des virgules) qui peuvent être aggrégées. Voir :
            https://cloud.google.com/apigee/docs/api-platform/analytics/use-analytics-api-measure-api-program-performance#specifying-the-metrics-to-return
            https://cloud.google.com/apigee/docs/api-platform/analytics/analytics-reference#metrics
        :param time_unit: unité d'aggrégation (day, week, hour)
        :param from_time: datetime à partir duquel collecter les données
        :param to_time: datetime jusqu'au quel on collecte les données
        """
        from_time_str = from_time.strftime("%m/%d/%Y %H:%M")
        to_time_str = to_time.strftime("%m/%d/%Y %H:%M")
        url = f"/organizations/{organisation}/environments/{environment}/stats/{dimension}?select={metric}&timeUnit={time_unit}&timeRange={from_time_str}~{to_time_str}"

        response = self.api_client.get_request_json(url)

        response_typed: models.StatResponse = extractor.extract_as_object(response, models.StatResponse)

        if len(response_typed.environments) == 0:
            return None

        return response_typed.environments[0]
