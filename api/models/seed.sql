-- Limpa as tabelas antes de inserir novos dados (para idempotência)
DELETE FROM [dbo].[Crops];
DELETE FROM [dbo].[Environments];
GO

-- Reseta o contador de identidade para as tabelas
DBCC CHECKIDENT ('[dbo].[Crops]', RESEED, 0);
DBCC CHECKIDENT ('[dbo].[Environments]', RESEED, 0);
GO

-- Inserir Culturas Brasileiras (Tubérculos)
INSERT INTO [dbo].[Crops] 
    (CommonName, ScientificName, Category, TempMinC, TempMaxC, PhMin, PhMax, PhotoperiodMinH, PhotoperiodMaxH, WaterNeed, EvidenceLevel, ImagePath)
VALUES
    ('Batata-doce', 'Ipomoea batatas', 'Tubérculo', 24.0, 30.0, 5.0, 7.0, 9.0, 13.0, 'media', 'alto', 'web/resources/batata-doce.png'),
    ('Cará', 'Dioscorea alata', 'Tubérculo', 25.0, 30.0, 5.5, 6.5, 10.0, 14.0, 'media', 'medio', 'web/resources/cara.png'),
    ('Inhame', 'Colocasia esculenta', 'Tubérculo', 21.0, 27.0, 5.5, 6.5, 12.0, 12.0, 'alta', 'medio', 'web/resources/inhame.png'),
    ('Mandioca', 'Manihot esculenta', 'Raiz', 20.0, 35.0, 5.0, 8.0, 10.0, 12.0, 'baixa', 'alto', 'web/resources/mandioca.png');
GO

-- Inserir Ambientes Planetários e Análogos
INSERT INTO [dbo].[Environments]
    (Name, Type, TempMinC, TempMaxC, PressureKPa, GravityG, RadiationIndex, SoilPh, SoilType, WaterAvailability, PhotoperiodH, Atmosphere, EvidenceLevel, ImagePath)
VALUES
    ('Lua', 'Planetário', -173.0, 127.0, 0.0, 0.166, 10.0, 11.0, 'Regolito basáltico', 'baixa', 354.0, 'Exosfera (traços)', 'alto', 'web/resources/lua.png'),
    ('Marte', 'Planetário', -125.0, 20.0, 0.6, 0.379, 7.0, 8.5, 'Regolito (percloratos)', 'baixa', 24.6, '95% CO2', 'alto', 'web/resources/marte.png'),
    ('Estação Espacial Internacional (ISS)', 'Analógico', 20.0, 24.0, 101.3, 0.0, 0.1, 6.5, 'Hidropônico/Aeropônico', 'media', 16.0, '78% N2, 21% O2', 'alto', 'web/resources/iss.png'),
    ('Europa (Lua de Júpiter)', 'Planetário', -223.0, -163.0, 0.0, 0.134, 9.0, NULL, 'Gelo de água', 'alta', 85.2, 'Traços de O2', 'baixo', 'web/resources/europa.png'),
    ('Io (Lua de Júpiter)', 'Planetário', -183.0, 1627.0, 0.0, 0.183, 12.0, NULL, 'Enxofre, silicato', 'baixa', 42.5, 'SO2', 'baixo', 'web/resources/io.png'),
    ('Vênus', 'Planetário', 446.0, 486.0, 9200.0, 0.904, 2.0, 8.0, 'Rocha basáltica', 'baixa', 2802.0, '96% CO2, 3% N2', 'baixo', 'web/resources/venus.png');
GO

