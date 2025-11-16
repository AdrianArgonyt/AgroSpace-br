-- Verifica se a tabela Crops já existe, senão cria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Crops' AND xtype='U')
BEGIN
    CREATE TABLE Crops (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        CommonName NVARCHAR(120) NOT NULL,
        ScientificName NVARCHAR(200) NULL,
        Category NVARCHAR(60) NULL,
        TempMinC FLOAT NULL,
        TempMaxC FLOAT NULL,
        PhMin FLOAT NULL,
        PhMax FLOAT NULL,
        PhotoperiodMinH FLOAT NULL,
        PhotoperiodMaxH FLOAT NULL,
        WaterNeed NVARCHAR(16) NULL,
        EvidenceLevel NVARCHAR(16) NULL,
        Sources NVARCHAR(MAX) NULL
    );
END
GO

-- Verifica se a tabela Environments já existe, senão cria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Environments' AND xtype='U')
BEGIN
    CREATE TABLE Environments (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Name NVARCHAR(120) NOT NULL,
        Type NVARCHAR(30) NOT NULL,
        TempMinC FLOAT NULL,
        TempMaxC FLOAT NULL,
        PressureKPa FLOAT NULL,
        GravityG FLOAT NULL,
        RadiationIndex FLOAT NULL,
        SoilPh FLOAT NULL,
        SoilType NVARCHAR(60) NULL,
        WaterAvailability NVARCHAR(16) NULL,
        PhotoperiodH FLOAT NULL,
        Atmosphere NVARCHAR(120) NULL,
        EvidenceLevel NVARCHAR(16) NULL,
        Notes NVARCHAR(MAX) NULL,
        Sources NVARCHAR(MAX) NULL
    );
END
GO

-- Adiciona a coluna ImagePath à tabela Crops se ela não existir
IF NOT EXISTS (SELECT * FROM sys.columns WHERE Name = N'ImagePath' AND Object_ID = Object_ID(N'Crops'))
BEGIN
    ALTER TABLE Crops ADD ImagePath NVARCHAR(512) NULL;
END
GO

-- Adiciona a coluna ImagePath à tabela Environments se ela não existir
IF NOT EXISTS (SELECT * FROM sys.columns WHERE Name = N'ImagePath' AND Object_ID = Object_ID(N'Environments'))
BEGIN
    ALTER TABLE Environments ADD ImagePath NVARCHAR(512) NULL;
END
GO

-- (NOVO) Adiciona a tabela Users para autenticação
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
BEGIN
    CREATE TABLE Users (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Username NVARCHAR(100) NOT NULL UNIQUE,
        -- Armazena o hash da senha, nunca a senha em texto plano
        PasswordHash NVARCHAR(256) NOT NULL,
        -- Futuramente, podemos usar isso para diferenciar admin de usuário comum
        IsAdmin BIT NOT NULL DEFAULT 0
    );
END
GO

