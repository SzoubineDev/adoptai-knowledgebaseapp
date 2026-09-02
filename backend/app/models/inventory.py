"""
SQLAlchemy models mapped to the AdoptAI inventory schema (public tables).

These tables already exist in PostgreSQL / Supabase. The models are read-oriented
and must not be used with Base.metadata.create_all() as a source of truth.
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Departement(Base):
    __tablename__ = "departement"

    id_departement: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_departement: Mapped[str] = mapped_column(String(150), nullable=False)

    applications: Mapped[List["Application"]] = relationship(back_populates="departement")
    utilisateurs: Mapped[List["Utilisateur"]] = relationship(back_populates="departement")
    tickets: Mapped[List["TicketHelpdesk"]] = relationship(back_populates="departement")
    services_sap: Mapped[List["ServiceSap"]] = relationship(back_populates="departement")


class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    id_departement: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departement.id_departement"),
        nullable=False
    )

    id_auth: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=True
    )

    departement: Mapped["Departement"] = relationship(
        "Departement",
        back_populates="utilisateurs"
    )

    # The user who owns/uses the device
    appareils: Mapped[List["Appareil"]] = relationship(
        "Appareil",
        foreign_keys="Appareil.id_utilisateur",
        back_populates="utilisateur"
    )

    # The IT responsible for the device
    appareils_responsable: Mapped[List["Appareil"]] = relationship(
        "Appareil",
        foreign_keys="Appareil.id_responsable",
        back_populates="responsable_it"
    )


class Appareil(Base):
    __tablename__ = "appareil"

    id_appareil: Mapped[int] = mapped_column(Integer, primary_key=True)
    hardware_model: Mapped[Optional[str]] = mapped_column(String(150))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    os_version: Mapped[Optional[str]] = mapped_column(String(50))
    storage_capacity_gb: Mapped[Optional[int]] = mapped_column(Integer)
    mdm_status: Mapped[Optional[str]] = mapped_column(String(50))

    id_utilisateur: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=False
    )

    id_responsable: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("utilisateur.id_utilisateur"),
        nullable=True
    )

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        foreign_keys=[id_utilisateur],
        back_populates="appareils"
    )

    responsable_it: Mapped[Optional["Utilisateur"]] = relationship(
        "Utilisateur",
        foreign_keys=[id_responsable],
        back_populates="appareils_responsable"
    )

    installations: Mapped[List["Installation"]] = relationship(
        "Installation",
        back_populates="appareil"
    )


class Application(Base):
    __tablename__ = "application"

    id_application: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_canonique: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(100))
    criticite: Mapped[Optional[str]] = mapped_column(String(50))
    statut: Mapped[Optional[str]] = mapped_column(String(50))
    date_derniere_maj: Mapped[Optional[date]] = mapped_column(Date)
    id_departement: Mapped[int] = mapped_column(
        Integer, ForeignKey("departement.id_departement"), nullable=False
    )

    departement: Mapped["Departement"] = relationship(back_populates="applications")
    aliases: Mapped[List["AliasApplication"]] = relationship(back_populates="application")
    installations: Mapped[List["Installation"]] = relationship(back_populates="application")
    services_sap: Mapped[List["ServiceSap"]] = relationship(back_populates="application")
    tickets: Mapped[List["TicketHelpdesk"]] = relationship(back_populates="application")


class AliasApplication(Base):
    __tablename__ = "alias_application"

    id_alias: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_source: Mapped[str] = mapped_column(String(200), nullable=False)
    systeme_source: Mapped[Optional[str]] = mapped_column(String(100))
    id_application: Mapped[int] = mapped_column(
        Integer, ForeignKey("application.id_application"), nullable=False
    )

    application: Mapped["Application"] = relationship(back_populates="aliases")


class Installation(Base):
    __tablename__ = "installation"

    id_appareil: Mapped[int] = mapped_column(
        Integer, ForeignKey("appareil.id_appareil"), primary_key=True
    )
    id_application: Mapped[int] = mapped_column(
        Integer, ForeignKey("application.id_application"), primary_key=True
    )

    appareil: Mapped["Appareil"] = relationship(back_populates="installations")
    application: Mapped["Application"] = relationship(back_populates="installations")


class TypeIncident(Base):
    __tablename__ = "type_incident"

    id_type_incident: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle_type: Mapped[str] = mapped_column(String(150), nullable=False)

    tickets: Mapped[List["TicketHelpdesk"]] = relationship(back_populates="type_incident")


class TicketHelpdesk(Base):
    __tablename__ = "ticket_helpdesk"

    id_ticket: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    priorite: Mapped[Optional[str]] = mapped_column(String(50))
    statut: Mapped[Optional[str]] = mapped_column(String(50))
    date_creation: Mapped[Optional[date]] = mapped_column(Date)
    id_application: Mapped[int] = mapped_column(
        Integer, ForeignKey("application.id_application"), nullable=False
    )
    id_departement: Mapped[int] = mapped_column(
        Integer, ForeignKey("departement.id_departement"), nullable=False
    )
    id_type_incident: Mapped[int] = mapped_column(
        Integer, ForeignKey("type_incident.id_type_incident"), nullable=False
    )

    application: Mapped["Application"] = relationship(back_populates="tickets")
    departement: Mapped["Departement"] = relationship(back_populates="tickets")
    type_incident: Mapped["TypeIncident"] = relationship(back_populates="tickets")


class ModuleSap(Base):
    __tablename__ = "module_sap"

    id_module: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_module: Mapped[str] = mapped_column(String(150), nullable=False)

    services_sap: Mapped[List["ServiceSap"]] = relationship(back_populates="module_sap")


class ProcessusMetier(Base):
    __tablename__ = "processus_metier"

    id_processus: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_processus: Mapped[str] = mapped_column(String(200), nullable=False)

    services_sap: Mapped[List["ServiceSap"]] = relationship(back_populates="processus_metier")


class Serveur(Base):
    __tablename__ = "serveur"

    id_serveur: Mapped[int] = mapped_column(Integer, primary_key=True)
    environnement: Mapped[Optional[str]] = mapped_column(String(100))
    nom_noeud: Mapped[Optional[str]] = mapped_column(String(50))

    services_sap: Mapped[List["ServiceSap"]] = relationship(back_populates="serveur")


class ServiceSap(Base):
    __tablename__ = "service_sap"

    id_service_sap: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom_service: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(50))
    id_application: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("application.id_application"), nullable=True
    )
    id_processus: Mapped[int] = mapped_column(
        Integer, ForeignKey("processus_metier.id_processus"), nullable=False
    )
    id_serveur: Mapped[int] = mapped_column(
        Integer, ForeignKey("serveur.id_serveur"), nullable=False
    )
    id_departement: Mapped[int] = mapped_column(
        Integer, ForeignKey("departement.id_departement"), nullable=False
    )
    id_module: Mapped[int] = mapped_column(
        Integer, ForeignKey("module_sap.id_module"), nullable=False
    )
    numero_workflow: Mapped[Optional[str]] = mapped_column(String(100))

    application: Mapped[Optional["Application"]] = relationship(back_populates="services_sap")
    processus_metier: Mapped["ProcessusMetier"] = relationship(back_populates="services_sap")
    serveur: Mapped["Serveur"] = relationship(back_populates="services_sap")
    departement: Mapped["Departement"] = relationship(back_populates="services_sap")
    module_sap: Mapped["ModuleSap"] = relationship(back_populates="services_sap")
