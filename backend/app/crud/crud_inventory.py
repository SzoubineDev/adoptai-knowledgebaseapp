"""Read-side queries and DTO mapping for the inventory (applications, stats)."""

from collections.abc import Sequence
from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.inventory import (
    Appareil,
    Application,
    Installation,
    ServiceSap,
    TicketHelpdesk,
    Utilisateur,
)
from app.schemas.inventory import (
    ApplicationOut,
    DataSourceOut,
    IamStatsOut,
    NetworkStatsOut,
    StatsOut,
)

_APP_LOAD_OPTIONS = (
    joinedload(Application.departement),
    selectinload(Application.aliases),
    selectinload(Application.installations)
    .selectinload(Installation.appareil)
    .joinedload(Appareil.responsable_it),
    selectinload(Application.installations)
    .selectinload(Installation.appareil)
    .joinedload(Appareil.utilisateur),
    selectinload(Application.services_sap).joinedload(ServiceSap.serveur),
    selectinload(Application.tickets),
)


def _format_date(value: date | datetime | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    return value.strftime("%Y-%m-%d")


def _normalize_criticality(raw: str | None) -> str:
    if not raw:
        return "Moyenne"
    mapping = {
        "haute": "Élevée",
        "élevée": "Élevée",
        "elevee": "Élevée",
        "critique": "Critique",
        "moyenne": "Moyenne",
        "basse": "Basse",
    }
    return mapping.get(raw.strip().lower(), raw)


def _resolve_source(app: Application) -> str:
    for alias in app.aliases or []:
        if alias.systeme_source:
            return alias.systeme_source
    if app.services_sap:
        return "SAP"
    if app.installations:
        return "Apple"
    if app.tickets:
        return "HelpDesk"
    return "ServiceNow"


def _resolve_tech_lead(app: Application) -> str:
    for inst in app.installations or []:
        responsable = inst.appareil.responsable_it if inst.appareil else None
        if responsable and responsable.nom_responsable:
            return responsable.nom_responsable
    return "—"


def _resolve_environment(app: Application) -> str:
    for service in app.services_sap or []:
        if service.serveur and service.serveur.environnement:
            return service.serveur.environnement
    if app.statut:
        return app.statut
    return "Production"


def _resolve_version(app: Application) -> str | None:
    for service in app.services_sap or []:
        if service.version:
            return service.version
    if app.date_derniere_maj:
        return str(app.date_derniere_maj)
    return None


def _resolve_iam_status(app: Application) -> str:
    linked = 0
    total = 0
    for inst in app.installations or []:
        user = inst.appareil.utilisateur if inst.appareil else None
        if user:
            total += 1
            if user.id_auth:
                linked += 1
    if total and linked == total:
        return "SSO / identité liée"
    if linked:
        return f"SSO partiel ({linked}/{total})"
    if app.statut and app.statut.lower() == "actif":
        return "En cours de migration SSO"
    return "Non renseigné"


def _resolve_network_policy(criticality: str) -> str:
    if criticality in {"Critique", "Élevée"}:
        return "Filtrage strict AHDIGITAL"
    if criticality == "Moyenne":
        return "VLAN interne filtré"
    return "HTTPS restreint"


def application_to_out(app: Application) -> ApplicationOut:
    criticality = _normalize_criticality(app.criticite)
    users = {
        inst.appareil.id_utilisateur
        for inst in (app.installations or [])
        if inst.appareil
    }
    return ApplicationOut(
        id=str(app.id_application),
        code=f"APP-{app.id_application:03d}",
        name=app.nom_canonique,
        category=app.type or "Non classé",
        source=_resolve_source(app),
        owner=app.departement.nom_departement if app.departement else "—",
        techLead=_resolve_tech_lead(app),
        criticality=criticality,
        iamStatus=_resolve_iam_status(app),
        networkPolicy=_resolve_network_policy(criticality),
        environment=_resolve_environment(app),
        description=app.description or "Aucune description renseignée.",
        version=_resolve_version(app),
        usersCount=len(users),
        status=app.statut,
    )


def list_applications(db: Session, *, limit: int | None = None) -> list[ApplicationOut]:
    stmt = (
        select(Application)
        .options(*_APP_LOAD_OPTIONS)
        .order_by(Application.id_application.desc())
    )
    if limit is not None:
        stmt = stmt.limit(limit)
    rows: Sequence[Application] = db.scalars(stmt).unique().all()
    return [application_to_out(app) for app in rows]


def get_application(db: Session, application_id: int) -> ApplicationOut | None:
    stmt = (
        select(Application)
        .options(*_APP_LOAD_OPTIONS)
        .where(Application.id_application == application_id)
    )
    app = db.scalars(stmt).unique().one_or_none()
    if app is None:
        return None
    return application_to_out(app)


def list_data_sources(db: Session) -> list[DataSourceOut]:
    apple_count = db.scalar(select(func.count()).select_from(Appareil)) or 0
    sap_count = db.scalar(select(func.count()).select_from(ServiceSap)) or 0
    servicenow_count = db.scalar(
        select(func.count()).select_from(Application).where(Application.type.is_not(None))
    ) or 0
    helpdesk_count = db.scalar(select(func.count()).select_from(TicketHelpdesk)) or 0

    last_app_update = db.scalar(select(func.max(Application.date_derniere_maj)))
    last_ticket = db.scalar(select(func.max(TicketHelpdesk.date_creation)))

    return [
        DataSourceOut(
            id="apple",
            name="Apple Infrastructure",
            type="Hardware & OS Inventory",
            count=apple_count,
            status="Active",
            lastSync=_format_date(last_app_update),
            description="Parc de devices et terminaux Apple (MacBook, iMac, iOS) sous supervision MDM.",
        ),
        DataSourceOut(
            id="sap",
            name="SAP Enterprise ERP",
            type="ERP & Business Modules",
            count=sap_count,
            status="Active",
            lastSync=_format_date(last_app_update),
            description="Modules cœurs SAP et services techniques recensés dans l'inventaire.",
        ),
        DataSourceOut(
            id="servicenow",
            name="ServiceNow ITSM",
            type="IT Service Catalog & Incidents",
            count=servicenow_count,
            status="Active",
            lastSync=_format_date(last_app_update),
            description="Catalogue des applications et services IT importés depuis ServiceNow.",
        ),
        DataSourceOut(
            id="helpdesk",
            name="HelpDesk Internal",
            type="Support & Tickets",
            count=helpdesk_count,
            status="Active",
            lastSync=_format_date(last_ticket),
            description="Base d'incidents N1/N2 et demandes d'assistance utilisateurs.",
        ),
    ]


def get_stats(db: Session) -> StatsOut:
    total_accounts = db.scalar(select(func.count()).select_from(Utilisateur)) or 0
    sso_enabled = db.scalar(
        select(func.count()).select_from(Utilisateur).where(Utilisateur.id_auth.is_not(None))
    ) or 0
    pending_audits = db.scalar(
        select(func.count())
        .select_from(TicketHelpdesk)
        .where(TicketHelpdesk.statut.in_(("En attente", "En cours")))
    ) or 0
    rate = f"{round((sso_enabled / total_accounts) * 100)}%" if total_accounts else "0%"

    open_high = db.scalar(
        select(func.count())
        .select_from(TicketHelpdesk)
        .where(
            TicketHelpdesk.priorite.in_(("Critique", "Haute")),
            TicketHelpdesk.statut != "Résolu",
        )
    ) or 0
    active_apps = db.scalar(
        select(func.count()).select_from(Application).where(Application.statut == "Actif")
    ) or 0
    application_count = db.scalar(select(func.count()).select_from(Application)) or 0
    installations = db.scalar(select(func.count()).select_from(Installation)) or 0

    return StatsOut(
        applicationCount=application_count,
        iam=IamStatsOut(
            totalAccounts=total_accounts,
            ssoEnabled=sso_enabled,
            pendingAudits=pending_audits,
            mfaEnforcedRate=rate,
        ),
        network=NetworkStatsOut(
            vlan="AHDIGITAL-SEC-01",
            inspectedPackets24h=str(installations),
            blockedThreats24h=open_high,
            activeFirewallRules=active_apps,
        ),
    )
