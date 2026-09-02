"""Pydantic schemas for inventory API responses consumed by the Next.js UI."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=False)

    id: str = Field(description="Numeric application id as a string (used in UI routes).")
    code: str
    name: str
    category: str
    source: str
    owner: str
    techLead: str
    criticality: str
    iamStatus: str
    networkPolicy: str
    environment: str
    description: str
    version: Optional[str] = None
    usersCount: int = 0
    status: Optional[str] = None


class DataSourceOut(BaseModel):
    id: str
    name: str
    type: str
    count: int
    status: str
    lastSync: Optional[str] = None
    description: str


class IamStatsOut(BaseModel):
    totalAccounts: int
    ssoEnabled: int
    pendingAudits: int
    mfaEnforcedRate: str


class NetworkStatsOut(BaseModel):
    vlan: str
    inspectedPackets24h: str
    blockedThreats24h: int
    activeFirewallRules: int


class StatsOut(BaseModel):
    applicationCount: int = 0
    iam: IamStatsOut
    network: NetworkStatsOut
