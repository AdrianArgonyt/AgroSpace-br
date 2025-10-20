-- Define a estrutura das tabelas do banco de dados.
-- Este script é idempotente e pode ser executado várias vezes sem causar erros.

-- Tabela para armazenar as culturas agrícolas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Crops' and xtype='U')
BEGIN
    CREATE TABLE Crops (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CommonName NVARCHAR(120) NOT NULL,        -- Ex.: "Mandioca"
        ScientificName NVARCHAR(200) NULL,      -- Ex.: "Manihot esculenta"
        Family NVARCHAR(100) NULL,               -- Ex.: "Euphorbiaceae"
        ImagePath NVARCHAR(255) NULL,            -- Caminho para a imagem, ex: 'resources/mandioca.png'
        
        -- Condições ideais para o crescimento
        TempMinC FLOAT NULL,                     -- Temperatura mínima em Celsius
        TempMaxC FLOAT NULL,                     -- Temperatura máxima em Celsius
        PhMin FLOAT NULL,                        -- pH mínimo do solo
        PhMax FLOAT NULL,                        -- pH máximo do solo
        PhotoperiodMinH FLOAT NULL,              -- Mínimo de horas de luz por dia
        PhotoperiodMaxH FLOAT NULL,              -- Máximo de horas de luz por dia
        WaterNeed NVARCHAR(16) NULL,             -- 'baixa', 'media', 'alta'
        
        -- Metadados
        EvidenceLevel NVARCHAR(16) NULL,         -- Nível de evidência científica: 'baixo', 'medio', 'alto'
        Sources NVARCHAR(MAX) NULL               -- Fontes, URLs, papers, etc.
    );
END
GO

-- Tabela para armazenar os ambientes planetários ou análogos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Environments' and xtype='U')
BEGIN
    CREATE TABLE Environments (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(120) NOT NULL,             -- Ex.: "Marte", "Lua"
        Type NVARCHAR(30) NOT NULL,              -- 'Planeta', 'Lua', 'Análogo Terrestre'
        Description NVARCHAR(MAX) NULL,          -- Breve descrição do ambiente
        ImagePath NVARCHAR(255) NULL,            -- Caminho para a imagem, ex: 'resources/mars.png'

        -- Características físicas e ambientais
        TempMinC FLOAT NULL,                     -- Temperatura mínima em Celsius na superfície
        TempMaxC FLOAT NULL,                     -- Temperatura máxima em Celsius na superfície
        PressureKPa FLOAT NULL,                  -- Pressão atmosférica em quiloPascals
        GravityG FLOAT NULL,                     -- Gravidade em relação à da Terra (G)
        RadiationIndex FLOAT NULL,               -- Índice de radiação (0-10)
        SoilPh FLOAT NULL,                       -- pH médio do solo/regolito
        SoilType NVARCHAR(60) NULL,              -- Ex.: "Regolito basáltico"
        WaterAvailability NVARCHAR(16) NULL,     -- 'baixa', 'media', 'alta' (presença de gelo, vapor, etc.)
        PhotoperiodH FLOAT NULL,                 -- Duração do dia em horas
        Atmosphere NVARCHAR(120) NULL,           -- Composição principal da atmosfera

        -- Metadados
        EvidenceLevel NVARCHAR(16) NULL,
        Notes NVARCHAR(MAX) NULL,
        Sources NVARCHAR(MAX) NULL
    );
END
GO

