"""Inventory endpoints — applications, data sources, and dashboard stats."""

import logging

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import ApplicationNotFoundException
from app.crud.crud_inventory import get_application, get_stats, list_applications, list_data_sources
from app.schemas.inventory import ApplicationOut, DataSourceOut, StatsOut

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/applications",
    response_model=list[ApplicationOut],
    status_code=status.HTTP_200_OK,
    tags=["Applications"],
    summary="List inventoried applications",
)
def get_applications(
    limit: int | None = Query(
        default=None,
        ge=1,
        le=500,
        description="Optional max number of applications to return (newest ids first).",
    ),
    db: Session = Depends(get_db),
) -> list[ApplicationOut]:
    logger.info("GET /applications limit=%s", limit)
    return list_applications(db, limit=limit)


@router.get(
    "/applications/{application_id}",
    response_model=ApplicationOut,
    status_code=status.HTTP_200_OK,
    tags=["Applications"],
    summary="Retrieve an application by ID",
)
def get_application_by_id(
    application_id: int = Path(..., ge=1, description="Numeric primary key of the application."),
    db: Session = Depends(get_db),
) -> ApplicationOut:
    logger.info("GET /applications/%s", application_id)
    app = get_application(db, application_id)
    if app is None:
        raise ApplicationNotFoundException(application_id)
    return app


@router.get(
    "/data-sources",
    response_model=list[DataSourceOut],
    status_code=status.HTTP_200_OK,
    tags=["Data Sources"],
    summary="Aggregated data-source counts",
)
def get_data_sources(db: Session = Depends(get_db)) -> list[DataSourceOut]:
    logger.info("GET /data-sources")
    return list_data_sources(db)


@router.get(
    "/stats",
    response_model=StatsOut,
    status_code=status.HTTP_200_OK,
    tags=["Stats"],
    summary="IAM and network stats derived from inventory data",
)
def get_inventory_stats(db: Session = Depends(get_db)) -> StatsOut:
    logger.info("GET /stats")
    return get_stats(db)
