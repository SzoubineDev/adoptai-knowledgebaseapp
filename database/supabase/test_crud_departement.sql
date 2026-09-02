-- ============================================================
-- TEST CRUD - table departement
-- A executer etape par etape (bloc par bloc) pour observer chaque resultat
-- ============================================================

-- 1) CREATE : ajouter un departement de test
INSERT INTO departement (nom_departement) VALUES ('Departement Test CRUD')
RETURNING *;

-- 2) READ : verifier qu'il existe bien
SELECT * FROM departement WHERE nom_departement = 'Departement Test CRUD';

-- 3) UPDATE : renommer ce departement de test
UPDATE departement 
SET nom_departement = 'Departement Test CRUD Modifie'
WHERE nom_departement = 'Departement Test CRUD'
RETURNING *;

-- 4) DELETE : supprimer la ligne de test (nettoyage)
DELETE FROM departement 
WHERE nom_departement = 'Departement Test CRUD Modifie'
RETURNING *;

-- 5) Verification finale : la ligne ne doit plus exister
SELECT * FROM departement WHERE nom_departement LIKE 'Departement Test%';
