-- Insere dados iniciais nas tabelas.
-- Este script é idempotente: ele verifica se os dados já existem antes de inserir.

-- Inserção de Culturas (Crops)
IF NOT EXISTS (SELECT 1 FROM Crops WHERE CommonName = 'Mandioca')
BEGIN
    INSERT INTO Crops (CommonName, ScientificName, Family, ImagePath, TempMinC, TempMaxC, PhMin, PhMax, PhotoperiodMinH, PhotoperiodMaxH, WaterNeed, EvidenceLevel, Sources)
    VALUES 
    ('Mandioca', 'Manihot esculenta', 'Euphorbiaceae', 'https://images.pexels.com/photos/8064761/pexels-photo-8064761.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 25.0, 29.0, 5.5, 6.5, 10.0, 12.0, 'media', 'alto', 'Embrapa'),
    ('Batata-doce', 'Ipomoea batatas', 'Convolvulaceae', 'https://images.pexels.com/photos/5945763/pexels-photo-5945763.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 20.0, 30.0, 5.0, 7.0, 8.0, 11.0, 'media', 'alto', 'FAO'),
    ('Inhame', 'Dioscorea spp.', 'Dioscoreaceae', 'https://images.pexels.com/photos/8699268/pexels-photo-8699268.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 22.0, 32.0, 5.5, 7.0, 11.0, 13.0, 'alta', 'medio', 'Wikipedia'),
    ('Cará', 'Dioscorea alata', 'Dioscoreaceae', 'https://images.pexels.com/photos/8437032/pexels-photo-8437032.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 24.0, 30.0, 5.0, 6.5, 10.0, 12.0, 'alta', 'medio', 'HortiFruti Brasil');
END
GO

-- Inserção de Ambientes (Environments)
IF NOT EXISTS (SELECT 1 FROM Environments WHERE Name = 'Marte')
BEGIN
    INSERT INTO Environments (Name, Type, Description, ImagePath, TempMinC, TempMaxC, PressureKPa, GravityG, RadiationIndex, SoilPh, SoilType, WaterAvailability, PhotoperiodH, Atmosphere, EvidenceLevel)
    VALUES 
    ('Marte', 'Planeta', 'O Planeta Vermelho, com uma atmosfera fina de CO2 e solo rico em ferro.', 'https://images.pexels.com/photos/73910/mars-mars-rover-space-travel-robot-73910.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', -125.0, 20.0, 0.6, 0.38, 8.0, 8.2, 'Regolito basáltico', 'baixa', 24.6, '95% CO2', 'alto'),
    ('Lua', 'Lua', 'Satélite natural da Terra, sem atmosfera e com temperaturas extremas.', 'https://images.pexels.com/photos/681405/pexels-photo-681405.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', -173.0, 127.0, 0.0, 0.16, 9.0, 7.0, 'Regolito anortosítico', 'baixa', 708.0, 'Vácuo', 'alto'),
    ('Europa', 'Lua', 'Lua de Júpiter com um oceano de água líquida sob uma crosta de gelo.', 'https://images.pexels.com/photos/116933/pexels-photo-116933.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', -220.0, -160.0, 0.0, 0.13, 10.0, NULL, 'Gelo de água', 'alta', 85.0, 'O2 (fina)', 'medio'),
    ('Vênus', 'Planeta', 'Planeta com efeito estufa descontrolado, chuvas de ácido sulfúrico e pressão esmagadora.', 'https://images.pexels.com/photos/433309/pexels-photo-433309.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 437.0, 487.0, 9300.0, 0.9, 5.0, 8.0, 'Rocha basáltica', 'baixa', 2802.0, '96% CO2, 3% N2', 'alto');
END
GO

