-- ============================================================
-- Migration du 27/08/2026 — Corrections demandées par Khadija
-- 1. Fusion RESPONSABLE_IT dans UTILISATEUR (role via enum)
-- 2. APPLICATION.type -> type_hebergement (enum)
-- ============================================================

-- 1. Nouveaux champs sur utilisateur
CREATE TYPE role_enum AS ENUM ('ADMINISTRATEUR','RESPONSABLE_IT','AGENT_HELPDESK','UTILISATEUR');

ALTER TABLE utilisateur ADD COLUMN nom VARCHAR(100);
ALTER TABLE utilisateur ADD COLUMN prenom VARCHAR(100);
ALTER TABLE utilisateur ADD COLUMN role role_enum DEFAULT 'UTILISATEUR';

-- 2. Transfert des 18 responsables IT vers utilisateur
INSERT INTO utilisateur (email, id_departement, nom, prenom, role)
SELECT
  LOWER(SPLIT_PART(nom_responsable, ' ', 2)) || '.' || LOWER(SPLIT_PART(nom_responsable, ' ', 1)) || '@adoptai.local',
  (SELECT id_departement FROM departement WHERE nom_departement = 'IT'),
  SPLIT_PART(nom_responsable, ' ', 2),
  SPLIT_PART(nom_responsable, ' ', 1),
  'RESPONSABLE_IT'
FROM responsable_it;

-- 3. Redirection de appareil.id_responsable vers utilisateur
ALTER TABLE appareil ADD COLUMN id_responsable_new INT REFERENCES utilisateur(id_utilisateur);

UPDATE appareil a
SET id_responsable_new = u.id_utilisateur
FROM responsable_it r
JOIN utilisateur u ON u.prenom = SPLIT_PART(r.nom_responsable, ' ', 1)
                   AND u.nom = SPLIT_PART(r.nom_responsable, ' ', 2)
WHERE a.id_responsable = r.id_responsable;

ALTER TABLE appareil DROP COLUMN id_responsable CASCADE;
ALTER TABLE appareil RENAME COLUMN id_responsable_new TO id_responsable;

-- Recréation des policies RLS qui dépendaient de l'ancienne colonne
CREATE POLICY "Utilisateur voit ses appareils" ON appareil FOR SELECT
USING (
  id_utilisateur = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
  OR
  id_responsable = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
);

CREATE POLICY "Installation visible selon appareil" ON installation FOR SELECT
USING (
  id_appareil IN (
    SELECT id_appareil FROM appareil
    WHERE id_utilisateur = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
       OR id_responsable = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
  )
);

-- 4. Suppression de l'ancienne table
DROP TABLE responsable_it CASCADE;

-- 5. application.type -> type_hebergement
CREATE TYPE type_hebergement_enum AS ENUM ('ON_PREMISE','CLOUD','HYBRIDE');

ALTER TABLE application ADD COLUMN type_hebergement type_hebergement_enum;

UPDATE application SET type_hebergement = CASE
  WHEN type = 'Interne' THEN 'ON_PREMISE'::type_hebergement_enum
  WHEN type = 'SaaS'    THEN 'CLOUD'::type_hebergement_enum
  WHEN type = 'Legacy'  THEN 'ON_PREMISE'::type_hebergement_enum
  ELSE NULL
END;

ALTER TABLE application DROP COLUMN type;
