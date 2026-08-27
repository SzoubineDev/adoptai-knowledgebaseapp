-- Valeurs par defaut basees sur les valeurs les plus frequentes dans les donnees reelles

ALTER TABLE application ALTER COLUMN statut SET DEFAULT 'Actif';
ALTER TABLE ticket_helpdesk ALTER COLUMN statut SET DEFAULT 'En attente';
ALTER TABLE appareil ALTER COLUMN mdm_status SET DEFAULT 'Managed';
