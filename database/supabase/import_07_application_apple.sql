-- Import application (51 logiciels Apple, distincts du catalogue ServiceNow)
-- id_departement = departement dominant parmi les appareils ou le logiciel est installe
INSERT INTO application (nom_canonique, id_departement)
SELECT '1Password', (SELECT id_departement FROM departement WHERE nom_departement = 'Direction')
UNION ALL
SELECT 'Adobe CC', (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Adobe Creative Cloud', (SELECT id_departement FROM departement WHERE nom_departement = 'Design')
UNION ALL
SELECT 'Adobe Fresco', (SELECT id_departement FROM departement WHERE nom_departement = 'Design')
UNION ALL
SELECT 'Chrome', (SELECT id_departement FROM departement WHERE nom_departement = 'Reception')
UNION ALL
SELECT 'Citrix Workspace', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Concur', (SELECT id_departement FROM departement WHERE nom_departement = 'Finance')
UNION ALL
SELECT 'DaVinci Resolve', (SELECT id_departement FROM departement WHERE nom_departement = 'Video Production')
UNION ALL
SELECT 'Docker', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Excel', (SELECT id_departement FROM departement WHERE nom_departement = 'Finance')
UNION ALL
SELECT 'Fastlane', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Figma', (SELECT id_departement FROM departement WHERE nom_departement = 'Design')
UNION ALL
SELECT 'Final Cut Pro', (SELECT id_departement FROM departement WHERE nom_departement = 'Video Production')
UNION ALL
SELECT 'Git', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'GitHub Mobile', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'GlobalProtect VPN', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Instagram', (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'IntelliJ IDEA', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Inventory Scanner App', (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations')
UNION ALL
SELECT 'Jamf', (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Jamf Pro', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Jamf Self Service', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Jenkins', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Jupyter', (SELECT id_departement FROM departement WHERE nom_departement = 'Data Science')
UNION ALL
SELECT 'Logic Pro', (SELECT id_departement FROM departement WHERE nom_departement = 'Video Production')
UNION ALL
SELECT 'Miro', (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Notability', (SELECT id_departement FROM departement WHERE nom_departement = 'Direction')
UNION ALL
SELECT 'Office 365', (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Okta', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Outlook', (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'PagerDuty', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Postman', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Procreate', (SELECT id_departement FROM departement WHERE nom_departement = 'Design')
UNION ALL
SELECT 'Python', (SELECT id_departement FROM departement WHERE nom_departement = 'Data Science')
UNION ALL
SELECT 'RStudio', (SELECT id_departement FROM departement WHERE nom_departement = 'Data Science')
UNION ALL
SELECT 'SAP FI-CO', (SELECT id_departement FROM departement WHERE nom_departement = 'Finance')
UNION ALL
SELECT 'SAP Fiori', (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations')
UNION ALL
SELECT 'SAP GUI', (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations')
UNION ALL
SELECT 'Safari', (SELECT id_departement FROM departement WHERE nom_departement = 'Retail')
UNION ALL
SELECT 'Salesforce', (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'Slack', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Square POS', (SELECT id_departement FROM departement WHERE nom_departement = 'Retail')
UNION ALL
SELECT 'SuccessFactors', (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'SuccessFactors Mobile', (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'Teams', (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'Terminal', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Visitor Log App', (SELECT id_departement FROM departement WHERE nom_departement = 'Reception')
UNION ALL
SELECT 'Wireshark', (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Xcode', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Xcode Server', (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering')
UNION ALL
SELECT 'Zoom', (SELECT id_departement FROM departement WHERE nom_departement = 'Direction');
