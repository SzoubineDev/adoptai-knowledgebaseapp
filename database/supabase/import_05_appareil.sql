-- Import appareil (40 lignes), id_responsable laisse NULL::INT (donnee absente de la source Apple)
INSERT INTO appareil (hardware_model, serial_number, os_version, storage_capacity_gb, mdm_status, id_utilisateur, id_responsable)
SELECT 'MacBook Pro 16"', 'C02CG123MD6R', 'macOS 14.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'j.smith@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M2', 'C02CG456MD6T', 'macOS 14.5', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'a.dupont@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 14"', 'C02CG789MD6Y', 'macOS 14.4', 1024, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'm.garcia@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M1', 'C02CG012MD6U', 'macOS 13.6', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'k.lee@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 16"', 'C02CG345MD6I', 'macOS 14.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'r.chen@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 14"', 'C02CG678MD6O', 'macOS 14.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'l.dube@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M2', 'C02CG901MD6P', 'macOS 14.4', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'p.smith@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 16"', 'C02CG234MD6A', 'macOS 14.5', 1024, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'e.tremblay@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M1', 'C02CG567MD6S', 'macOS 13.6', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'd.kim@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 14"', 'C02CG890MD6D', 'macOS 14.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 's.boulanger@company.com'), NULL::INT
UNION ALL
SELECT 'Mac Studio M2 Max', 'C02DG123MD6F', 'macOS 14.5', 2048, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 't.jensen@company.com'), NULL::INT
UNION ALL
SELECT 'Mac Mini M2', 'C02DG456MD6G', 'macOS 14.5', 512, 'Shared Device', (SELECT id_utilisateur FROM utilisateur WHERE email = 'it.lab.01@company.com'), NULL::INT
UNION ALL
SELECT 'iMac 24"', 'C02DG789MD6H', 'macOS 14.4', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'v.patel@company.com'), NULL::INT
UNION ALL
SELECT 'Mac Studio M1 Ultra', 'C02DG012MD6J', 'macOS 14.5', 1024, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'w.williams@company.com'), NULL::INT
UNION ALL
SELECT 'Mac Mini M2 Pro', 'C02DG345MD6K', 'macOS 14.5', 1024, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'build.server@company.com'), NULL::INT
UNION ALL
SELECT 'iPad Pro 12.9"', 'DLXCG123MD6L', 'iPadOS 17.5', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'a.dupont@company.com'), NULL::INT
UNION ALL
SELECT 'iPad Air 5th Gen', 'DLXCG456MD6Z', 'iPadOS 17.4', 64, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'l.dube@company.com'), NULL::INT
UNION ALL
SELECT 'iPad mini 6', 'DLXCG789MD6X', 'iPadOS 17.5', 64, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'p.smith@company.com'), NULL::INT
UNION ALL
SELECT 'iPad 10th Gen', 'DLXCG012MD6C', 'iPadOS 17.5', 64, 'Shared Device', (SELECT id_utilisateur FROM utilisateur WHERE email = 'retail.pos.01@company.com'), NULL::INT
UNION ALL
SELECT 'iPad Pro 11"', 'DLXCG345MD6V', 'iPadOS 17.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 's.boulanger@company.com'), NULL::INT
UNION ALL
SELECT 'iPad Air 5th Gen', 'DLXCG678MD6B', 'iPadOS 17.4', 64, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'k.lee@company.com'), NULL::INT
UNION ALL
SELECT 'iPad Pro 12.9"', 'DLXCG901MD6N', 'iPadOS 17.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'm.garcia@company.com'), NULL::INT
UNION ALL
SELECT 'iPad 10th Gen', 'DLXCG234MD6M', 'iPadOS 17.5', 64, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'v.patel@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 15 Pro', 'F17CG123MD6Q', 'iOS 17.5', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'j.smith@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 14', 'F17CG456MD6W', 'iOS 17.5', 128, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'a.dupont@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 15 Pro Max', 'F17CG789MD6E', 'iOS 17.5', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 's.boulanger@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 13', 'F17CG012MD6R', 'iOS 17.4', 128, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'l.dube@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 14 Pro', 'F17CG345MD6T', 'iOS 17.5', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'p.smith@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 15', 'F17CG678MD6Y', 'iOS 17.5', 128, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'e.tremblay@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 13 mini', 'F17CG901MD6U', 'iOS 17.4', 128, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'd.kim@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 14', 'F17CG234MD6I', 'iOS 17.5', 128, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'r.chen@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 15 Pro', 'F17CG567MD6O', 'iOS 17.5', 256, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'm.garcia@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone SE (3rd Gen)', 'F17CG890MD6P', 'iOS 17.5', 64, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'k.lee@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M3', 'C02CH123MD6A', 'macOS 14.5', 512, 'Pending Enrollment', (SELECT id_utilisateur FROM utilisateur WHERE email = 'n.rodriguez@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 14"', 'C02CH456MD6S', 'macOS 14.4', 512, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'c.miller@company.com'), NULL::INT
UNION ALL
SELECT 'Mac Studio M2 Ultra', 'C02CH789MD6D', 'macOS 14.5', 4096, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'b.taylor@company.com'), NULL::INT
UNION ALL
SELECT 'iPad mini 6', 'DLXCH012MD6F', 'iPadOS 17.5', 64, 'Shared Device', (SELECT id_utilisateur FROM utilisateur WHERE email = 'retail.pos.02@company.com'), NULL::INT
UNION ALL
SELECT 'iPhone 15', 'F17CH345MD6G', 'iOS 17.5', 128, 'Pending Enrollment', (SELECT id_utilisateur FROM utilisateur WHERE email = 'n.rodriguez@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Air M1', 'C02CH678MD6H', 'macOS 13.6', 256, 'BYOD', (SELECT id_utilisateur FROM utilisateur WHERE email = 'contractor.01@company.com'), NULL::INT
UNION ALL
SELECT 'MacBook Pro 16"', 'C02CH901MD6J', 'macOS 14.5', 1024, 'Managed', (SELECT id_utilisateur FROM utilisateur WHERE email = 'h.wilson@company.com'), NULL::INT;
