-- ============================================================
-- AdoptAI / App Knowledge Base
-- Script de création du schéma - Supabase (PostgreSQL)
-- Ordre respecté : tables sans dépendances d'abord,
-- puis tables avec clés étrangères
-- ============================================================

-- 1. DEPARTEMENT (aucune dépendance)
CREATE TABLE departement (
    id_departement  SERIAL PRIMARY KEY,
    nom_departement VARCHAR(150) NOT NULL
);

-- 2. RESPONSABLE_IT (aucune dépendance)
CREATE TABLE responsable_it (
    id_responsable  SERIAL PRIMARY KEY,
    nom_responsable VARCHAR(150) NOT NULL
);

-- 3. TYPE_INCIDENT (aucune dépendance)
CREATE TABLE type_incident (
    id_type_incident SERIAL PRIMARY KEY,
    libelle_type     VARCHAR(150) NOT NULL
);

-- 4. PROCESSUS_METIER (aucune dépendance)
CREATE TABLE processus_metier (
    id_processus     SERIAL PRIMARY KEY,
    nom_processus    VARCHAR(200) NOT NULL,
    numero_workflow  VARCHAR(100)
);

-- 5. SERVEUR (aucune dépendance)
CREATE TABLE serveur (
    id_serveur      SERIAL PRIMARY KEY,
    environnement   VARCHAR(100)
);

-- 6. MODULE_SAP (aucune dépendance)
CREATE TABLE module_sap (
    id_module   SERIAL PRIMARY KEY,
    nom_module  VARCHAR(150) NOT NULL
);

-- 7. UTILISATEUR (dépend de DEPARTEMENT)
CREATE TABLE utilisateur (
    id_utilisateur  SERIAL PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    id_departement  INT NOT NULL REFERENCES departement(id_departement)
);

-- 8. APPAREIL (dépend de UTILISATEUR et RESPONSABLE_IT)
CREATE TABLE appareil (
    id_appareil           SERIAL PRIMARY KEY,
    hardware_model        VARCHAR(150),
    serial_number         VARCHAR(100) UNIQUE,
    os_version            VARCHAR(50),
    storage_capacity_gb   INT,
    mdm_status            VARCHAR(50),
    id_utilisateur        INT NOT NULL REFERENCES utilisateur(id_utilisateur),
    id_responsable        INT NOT NULL REFERENCES responsable_it(id_responsable)
);

-- 9. APPLICATION (dépend de DEPARTEMENT)
CREATE TABLE application (
    id_application      SERIAL PRIMARY KEY,
    nom_canonique       VARCHAR(200) NOT NULL,
    description         TEXT,
    type                VARCHAR(100),
    criticite           VARCHAR(50),
    statut              VARCHAR(50),
    date_derniere_maj   DATE,
    id_departement      INT NOT NULL REFERENCES departement(id_departement)
);

-- 10. ALIAS_APPLICATION (dépend de APPLICATION)
CREATE TABLE alias_application (
    id_alias        SERIAL PRIMARY KEY,
    nom_source      VARCHAR(200) NOT NULL,
    systeme_source  VARCHAR(100),
    id_application  INT NOT NULL REFERENCES application(id_application)
);

-- 11. TICKET_HELPDESK (dépend de APPLICATION, DEPARTEMENT, TYPE_INCIDENT)
CREATE TABLE ticket_helpdesk (
    id_ticket          SERIAL PRIMARY KEY,
    description        TEXT,
    priorite           VARCHAR(50),
    statut             VARCHAR(50),
    date_creation      DATE,
    id_application     INT NOT NULL REFERENCES application(id_application),
    id_departement     INT NOT NULL REFERENCES departement(id_departement),
    id_type_incident   INT NOT NULL REFERENCES type_incident(id_type_incident)
);

-- 12. SERVICE_SAP (dépend de APPLICATION [nullable], PROCESSUS_METIER, SERVEUR, DEPARTEMENT, MODULE_SAP)
CREATE TABLE service_sap (
    id_service_sap  SERIAL PRIMARY KEY,
    nom_service     VARCHAR(200) NOT NULL,
    version         VARCHAR(50),
    id_application  INT NULL REFERENCES application(id_application),
    id_processus    INT NOT NULL REFERENCES processus_metier(id_processus),
    id_serveur      INT NOT NULL REFERENCES serveur(id_serveur),
    id_departement  INT NOT NULL REFERENCES departement(id_departement),
    id_module       INT NOT NULL REFERENCES module_sap(id_module)
);

-- 13. INSTALLATION - table de jonction N,N (dépend de APPAREIL et APPLICATION)
CREATE TABLE installation (
    id_appareil     INT NOT NULL REFERENCES appareil(id_appareil),
    id_application  INT NOT NULL REFERENCES application(id_application),
    PRIMARY KEY (id_appareil, id_application)
);

-- ============================================================
-- Fin du script - 13 tables créées
-- ============================================================
