-- ============================================================
-- RLS + Policies pour les tables restantes
-- ============================================================

-- ------------------------------------------------------------
-- APPAREIL : un utilisateur voit ses propres appareils,
-- un responsable_it voit ceux dont il a la charge
-- ------------------------------------------------------------
ALTER TABLE appareil ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Utilisateur voit ses appareils"
ON appareil
FOR SELECT
TO authenticated
USING (
  id_utilisateur = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
  OR
  id_responsable = (SELECT id_responsable FROM responsable_it WHERE id_auth = auth.uid())
);

-- ------------------------------------------------------------
-- Tables de référence / catalogue commun : lecture ouverte
-- à tout utilisateur authentifié
-- ------------------------------------------------------------
ALTER TABLE application ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture application" ON application
FOR SELECT TO authenticated USING (true);

ALTER TABLE alias_application ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture alias_application" ON alias_application
FOR SELECT TO authenticated USING (true);

ALTER TABLE service_sap ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture service_sap" ON service_sap
FOR SELECT TO authenticated USING (true);

ALTER TABLE module_sap ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture module_sap" ON module_sap
FOR SELECT TO authenticated USING (true);

ALTER TABLE processus_metier ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture processus_metier" ON processus_metier
FOR SELECT TO authenticated USING (true);

ALTER TABLE serveur ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture serveur" ON serveur
FOR SELECT TO authenticated USING (true);

ALTER TABLE type_incident ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Lecture type_incident" ON type_incident
FOR SELECT TO authenticated USING (true);

-- ------------------------------------------------------------
-- INSTALLATION : visible si l'appareil concerné est visible
-- (même logique que la table appareil)
-- ------------------------------------------------------------
ALTER TABLE installation ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Installation visible selon appareil"
ON installation
FOR SELECT
TO authenticated
USING (
  id_appareil IN (
    SELECT id_appareil FROM appareil
    WHERE id_utilisateur = (SELECT id_utilisateur FROM utilisateur WHERE id_auth = auth.uid())
       OR id_responsable = (SELECT id_responsable FROM responsable_it WHERE id_auth = auth.uid())
  )
);

-- ------------------------------------------------------------
-- UTILISATEUR / RESPONSABLE_IT : chacun voit sa propre fiche
-- ------------------------------------------------------------
ALTER TABLE utilisateur ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Utilisateur voit sa propre fiche" ON utilisateur
FOR SELECT TO authenticated USING (id_auth = auth.uid());

ALTER TABLE responsable_it ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Responsable voit sa propre fiche" ON responsable_it
FOR SELECT TO authenticated USING (id_auth = auth.uid());

-- ============================================================
-- Fin du script
-- ============================================================
