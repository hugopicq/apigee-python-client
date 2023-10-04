from typing import TypeVar, Generic, Dict, Any
import logging

T = TypeVar("T")
logger = logging.getLogger(__name__)


def extract_as_object(object: dict[str, Any], ObjectType: Generic[T] = dict[str, Any]) -> T:
    """
    Convertit un objet (souvent de type dict[str, Any] récupéré via une GET request) dans un type donné.
    La conversion utilise la librairie Pydantic et lève une ValidationError s'il n'y arrive pas.

    :param object: l'objet dont le type doit être converti
    :param ObjectType: le type d'objet dans lequel on souhaite le convertir
    """

    if object is None:
        return None

    result_obj = ObjectType(**object)

    return result_obj
