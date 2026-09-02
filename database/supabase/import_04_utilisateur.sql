-- Import utilisateur (22 comptes uniques, FK id_departement via sous-requete sur le nom)
INSERT INTO utilisateur (email, id_departement)
SELECT 'j.smith@company.com', id_departement FROM departement WHERE nom_departement = 'Engineering'
UNION ALL
SELECT 'a.dupont@company.com', id_departement FROM departement WHERE nom_departement = 'Marketing'
UNION ALL
SELECT 'm.garcia@company.com', id_departement FROM departement WHERE nom_departement = 'Design'
UNION ALL
SELECT 'k.lee@company.com', id_departement FROM departement WHERE nom_departement = 'RH'
UNION ALL
SELECT 'r.chen@company.com', id_departement FROM departement WHERE nom_departement = 'Engineering'
UNION ALL
SELECT 'l.dube@company.com', id_departement FROM departement WHERE nom_departement = 'Commercial'
UNION ALL
SELECT 'p.smith@company.com', id_departement FROM departement WHERE nom_departement = 'Opérations'
UNION ALL
SELECT 'e.tremblay@company.com', id_departement FROM departement WHERE nom_departement = 'IT'
UNION ALL
SELECT 'd.kim@company.com', id_departement FROM departement WHERE nom_departement = 'Finance'
UNION ALL
SELECT 's.boulanger@company.com', id_departement FROM departement WHERE nom_departement = 'Direction'
UNION ALL
SELECT 't.jensen@company.com', id_departement FROM departement WHERE nom_departement = 'Video Production'
UNION ALL
SELECT 'it.lab.01@company.com', id_departement FROM departement WHERE nom_departement = 'IT'
UNION ALL
SELECT 'v.patel@company.com', id_departement FROM departement WHERE nom_departement = 'Reception'
UNION ALL
SELECT 'w.williams@company.com', id_departement FROM departement WHERE nom_departement = 'Data Science'
UNION ALL
SELECT 'build.server@company.com', id_departement FROM departement WHERE nom_departement = 'Engineering'
UNION ALL
SELECT 'retail.pos.01@company.com', id_departement FROM departement WHERE nom_departement = 'Retail'
UNION ALL
SELECT 'n.rodriguez@company.com', id_departement FROM departement WHERE nom_departement = 'Commercial'
UNION ALL
SELECT 'c.miller@company.com', id_departement FROM departement WHERE nom_departement = 'IT'
UNION ALL
SELECT 'b.taylor@company.com', id_departement FROM departement WHERE nom_departement = 'Video Production'
UNION ALL
SELECT 'retail.pos.02@company.com', id_departement FROM departement WHERE nom_departement = 'Retail'
UNION ALL
SELECT 'contractor.01@company.com', id_departement FROM departement WHERE nom_departement = 'Engineering'
UNION ALL
SELECT 'h.wilson@company.com', id_departement FROM departement WHERE nom_departement = 'Data Science';
