/*
	Project: Store Incentive Data Warehouse
	Database: StoreIncentiveDW
	Purpose: Medallion Architecture schemas
*/

USE StoreIncentiveDW;
GO

-- Bronze schema
IF SCHEMA_ID(N'bronze') IS NULL
BEGIN
	EXEC(N'CREATE SCHEMA bronze');
	PRINT 'Bronze schema created.'
END;
ELSE
	PRINT 'Bronze schema alredy exists.'
GO

-- Silver schema
IF SCHEMA_ID(N'silver') IS NULL
BEGIN
	EXEC(N'CREATE SCHEMA silver');
	PRINT 'Silver schema created.'
END;
ELSE
	PRINT 'Silver schema already exists.'
GO

-- Gold schema
IF SCHEMA_ID(N'gold') IS NULL
BEGIN
	EXEC(N'CREATE SCHEMA gold');
	PRINT 'Gold schema created.'
END;
ELSE
	PRINT 'Gold schema already exists.'
GO

-- Verify schemas
SELECT
	name AS SchemaName,
	schema_id AS SchemaID
FROM sys.schemas
WHERE name IN ('bronze', 'silver', 'gold')
ORDER BY name;
GO