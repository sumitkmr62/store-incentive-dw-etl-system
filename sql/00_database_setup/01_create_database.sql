/*
	Project: Store Incentive Data Warehosue
	Version: 1 - SQL Server + Python
	Purpose: Create the primary data warehouse database
	Engine: Microsoft SQL Server 2022
*/

Use master;
GO

IF DB_ID(N'StoreIncentiveDW') IS NULL
BEGIN
	CREATE DATABASE StoreIncentiveDW;
	PRINT 'StoreIncentiveDW database created successfully.';
END
ELSE
BEGIN
	PRINT N'StoreIncentiveDW database alredy exists.';
END;
GO

-- Verify database creation
SELECT
	name as DatabaseName,
	state_desc AS DatabaseStatus,
	compatibility_level AS CompatibilityLevel
FROM sys.databases
WHERE name = N'StoreIncentiveDW';
GO
