from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime


class ProxyDeployment(BaseModel):
    environment: str
    apiProxy: str
    revision: str
    deployStartTime: datetime


class EnvironmentGroup(BaseModel):
    name: str
    hostnames: List[str]
    createdAt: str
    lastModifiedAt: str
    state: str


class TargetServer(BaseModel):
    name: str
    description: Optional[str] = ""
    host: str
    port: int
    isEnabled: Optional[bool] = True
    sslInfo: Optional[dict[str, Any]] = {}
    protocol: str


class KVMEntry(BaseModel):
    name: str
    value: str


class ApiProxy(BaseModel):
    name: str


class GetProxiesResponse(BaseModel):
    proxies: List[ApiProxy]


class GetProxyDeploymentsResponse(BaseModel):
    deployments: List[ProxyDeployment]


class GetKVMEntriesResponse(BaseModel):
    keyValueEntries: List[KVMEntry]
    nextPageToken: str


class GetEnvironmentGroupsResponse(BaseModel):
    environmentGroups: List[EnvironmentGroup]


class Metric(BaseModel):
    name: str
    values: List[Any]  # Float | {value: Float, timestamp: str}


class DimensionMetric(BaseModel):
    individualNames: List[str]
    metrics: List[Metric]


class EnvironmentStat(BaseModel):
    name: str
    metrics: Optional[List[Metric]] = []
    dimensions: Optional[List[DimensionMetric]] = []


class HostStat(BaseModel):
    name: str
    metrics: Optional[List[Metric]] = []
    dimensions: Optional[List[DimensionMetric]] = []


class StatResponse(BaseModel):
    environments: Optional[List[EnvironmentStat]] = []
    hosts: Optional[List[HostStat]] = []
    metaData: dict[str, Any]


class ApiProduct(BaseModel):
    name: Optional[str] = ""
    apiproduct: Optional[str] = ""
    status: Optional[str] = ""


class Attribute(BaseModel):
    name: str
    value: str


class Developer(BaseModel):
    email: str
    firstName: str
    lastName: str
    userName: str


class Credential(BaseModel):
    apiProducts: Optional[list[ApiProduct]] = []
    attributes: Optional[list[Attribute]] = []
    consumerKey: Optional[str] = ""
    consumerSecret: Optional[str] = ""
    expiresAt: Optional[int] = 0
    issuedAt: Optional[int] = 0
    scopes: Optional[list[str]] = []
    status: Optional[str] = ""


class DeveloperApp(BaseModel):
    appId: str
    attributes: Optional[list[Attribute]] = []
    callbackUrl: Optional[str] = ""
    createdAt: Optional[str] = ""
    credentials: Optional[list[Credential]] = []
    developerId: Optional[str] = ""
    lastModifiedAt: Optional[str] = ""
    name: Optional[str] = ""
    scopes: Optional[list[str]] = []
    status: Optional[str] = ""
    keyExpiresIn: Optional[str] = ""
    appFamily: Optional[str] = ""
    apiProducts: Optional[list[str]] = []


class GetDeveloperAppResponse(BaseModel):
    app: List[DeveloperApp]
