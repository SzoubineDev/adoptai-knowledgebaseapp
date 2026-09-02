-- Import installation (relie chaque appareil aux logiciels qui y sont installes)
INSERT INTO installation (id_appareil, id_application)
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG123MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Xcode')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG123MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Docker')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG123MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG123MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG456MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Adobe CC')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG456MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG456MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG456MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Jamf')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG789MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Figma')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG789MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Adobe CC')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG789MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG789MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Chrome')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG012MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'SuccessFactors')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG012MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG012MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'Zoom')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG345MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'IntelliJ IDEA')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG345MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'Git')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG345MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG345MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'GlobalProtect VPN')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG678MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Salesforce')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG678MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG678MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG901MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG901MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'SAP GUI')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG901MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG234MD6A'), (SELECT id_application FROM application WHERE nom_canonique = 'Jamf Pro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG234MD6A'), (SELECT id_application FROM application WHERE nom_canonique = 'Terminal')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG234MD6A'), (SELECT id_application FROM application WHERE nom_canonique = 'Wireshark')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG234MD6A'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG567MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'Excel')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG567MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'SAP FI-CO')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG567MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG890MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG890MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Zoom')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG890MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CG890MD6D'), (SELECT id_application FROM application WHERE nom_canonique = '1Password')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG123MD6F'), (SELECT id_application FROM application WHERE nom_canonique = 'Final Cut Pro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG123MD6F'), (SELECT id_application FROM application WHERE nom_canonique = 'DaVinci Resolve')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG123MD6F'), (SELECT id_application FROM application WHERE nom_canonique = 'Adobe CC')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG456MD6G'), (SELECT id_application FROM application WHERE nom_canonique = 'Jenkins')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG456MD6G'), (SELECT id_application FROM application WHERE nom_canonique = 'Postman')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG456MD6G'), (SELECT id_application FROM application WHERE nom_canonique = 'Git')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG789MD6H'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG789MD6H'), (SELECT id_application FROM application WHERE nom_canonique = 'Chrome')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG789MD6H'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG012MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Python')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG012MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Jupyter')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG012MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Docker')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG012MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG345MD6K'), (SELECT id_application FROM application WHERE nom_canonique = 'Xcode Server')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG345MD6K'), (SELECT id_application FROM application WHERE nom_canonique = 'Fastlane')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02DG345MD6K'), (SELECT id_application FROM application WHERE nom_canonique = 'Docker')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG123MD6L'), (SELECT id_application FROM application WHERE nom_canonique = 'Miro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG123MD6L'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG123MD6L'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG456MD6Z'), (SELECT id_application FROM application WHERE nom_canonique = 'Salesforce')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG456MD6Z'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG456MD6Z'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG789MD6X'), (SELECT id_application FROM application WHERE nom_canonique = 'SAP Fiori')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG789MD6X'), (SELECT id_application FROM application WHERE nom_canonique = 'Inventory Scanner App')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG012MD6C'), (SELECT id_application FROM application WHERE nom_canonique = 'Square POS')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG012MD6C'), (SELECT id_application FROM application WHERE nom_canonique = 'Safari')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG345MD6V'), (SELECT id_application FROM application WHERE nom_canonique = 'Notability')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG345MD6V'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG345MD6V'), (SELECT id_application FROM application WHERE nom_canonique = 'Zoom')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG678MD6B'), (SELECT id_application FROM application WHERE nom_canonique = 'SuccessFactors Mobile')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG678MD6B'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG901MD6N'), (SELECT id_application FROM application WHERE nom_canonique = 'Procreate')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG901MD6N'), (SELECT id_application FROM application WHERE nom_canonique = 'Adobe Fresco')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG901MD6N'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG234MD6M'), (SELECT id_application FROM application WHERE nom_canonique = 'Visitor Log App')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCG234MD6M'), (SELECT id_application FROM application WHERE nom_canonique = 'Chrome')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG123MD6Q'), (SELECT id_application FROM application WHERE nom_canonique = 'Okta')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG123MD6Q'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG123MD6Q'), (SELECT id_application FROM application WHERE nom_canonique = 'PagerDuty')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG456MD6W'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG456MD6W'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG456MD6W'), (SELECT id_application FROM application WHERE nom_canonique = 'Instagram')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG789MD6E'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG789MD6E'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG789MD6E'), (SELECT id_application FROM application WHERE nom_canonique = '1Password')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG012MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Salesforce')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG012MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG012MD6R'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG345MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'SAP Fiori')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG345MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG345MD6T'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG678MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Jamf Self Service')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG678MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Okta')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG678MD6Y'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG901MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG901MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG901MD6U'), (SELECT id_application FROM application WHERE nom_canonique = 'Concur')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG234MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG234MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'Okta')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG234MD6I'), (SELECT id_application FROM application WHERE nom_canonique = 'GitHub Mobile')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG567MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG567MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG567MD6O'), (SELECT id_application FROM application WHERE nom_canonique = 'Adobe Creative Cloud')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG890MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'SuccessFactors Mobile')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG890MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CG890MD6P'), (SELECT id_application FROM application WHERE nom_canonique = 'Outlook')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH123MD6A'), (SELECT id_application FROM application WHERE nom_canonique = 'Office 365')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH456MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'Jamf Pro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH456MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH456MD6S'), (SELECT id_application FROM application WHERE nom_canonique = 'Chrome')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH789MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Final Cut Pro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH789MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Logic Pro')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH789MD6D'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCH012MD6F'), (SELECT id_application FROM application WHERE nom_canonique = 'Square POS')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'DLXCH012MD6F'), (SELECT id_application FROM application WHERE nom_canonique = 'Safari')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'F17CH345MD6G'), (SELECT id_application FROM application WHERE nom_canonique = 'Teams')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH678MD6H'), (SELECT id_application FROM application WHERE nom_canonique = 'Citrix Workspace')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH678MD6H'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH901MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Python')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH901MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'RStudio')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH901MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Docker')
UNION ALL
SELECT (SELECT id_appareil FROM appareil WHERE serial_number = 'C02CH901MD6J'), (SELECT id_application FROM application WHERE nom_canonique = 'Slack');
