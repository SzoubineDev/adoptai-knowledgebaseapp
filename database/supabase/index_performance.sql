-- ============================================================
-- Index de performance - AdoptAI App Knowledge Base
-- Principe : indexer toutes les clés étrangères (FK), 
-- utilisées pour les jointures et les filtres RLS,
-- + quelques colonnes de filtre fréquentes (statut, etc.)
-- ============================================================

-- utilisateur
CREATE INDEX idx_utilisateur_departement ON utilisateur(id_departement);

-- appareil
CREATE INDEX idx_appareil_utilisateur ON appareil(id_utilisateur);
CREATE INDEX idx_appareil_responsable ON appareil(id_responsable);

-- application
CREATE INDEX idx_application_departement ON application(id_departement);
CREATE INDEX idx_application_statut ON application(statut);

-- alias_application
CREATE INDEX idx_alias_application ON alias_application(id_application);

-- ticket_helpdesk
CREATE INDEX idx_ticket_application ON ticket_helpdesk(id_application);
CREATE INDEX idx_ticket_departement ON ticket_helpdesk(id_departement);
CREATE INDEX idx_ticket_type_incident ON ticket_helpdesk(id_type_incident);
CREATE INDEX idx_ticket_statut ON ticket_helpdesk(statut);

-- service_sap
CREATE INDEX idx_service_sap_application ON service_sap(id_application);
CREATE INDEX idx_service_sap_processus ON service_sap(id_processus);
CREATE INDEX idx_service_sap_serveur ON service_sap(id_serveur);
CREATE INDEX idx_service_sap_departement ON service_sap(id_departement);
CREATE INDEX idx_service_sap_module ON service_sap(id_module);

-- installation (les colonnes de la PK composite sont déjà indexées automatiquement,
-- mais on ajoute l'index inverse pour accélérer les recherches par application)
CREATE INDEX idx_installation_application ON installation(id_application);

-- ============================================================
-- Fin du script
-- ============================================================
