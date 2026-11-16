-- 1. Verify source database exists or not
USE master;
GO

SELECT
  name AS database_name,
  state_desc AS database_status,
  compatibility_level,
  recovery_model_desc,
  create_date
FROM sys.databases
WHERE name = 'StoreIncentiveOLTP'
GO

-- 2. Inspect schemas and tables
USE StoreIncentiveOLTP;
GO

SELECT
  s.name AS schema_name,
  t.name AS table_name,
  t.create_date
FROM sys.tables AS t
INNER JOIN sys.schemas AS s
  ON t.schema_id = s.schema_id
WHERE s.name IN ('retail', 'hr', 'clinical', 'ops')
ORDER BY
s.name,
t.name
GO

-- 3. Inspect primary keys and foreign keys
USE StoreIncentiveOLTP;
GO

SELECT
  'PRIMARY KEY' AS constraint_type,
  s.name AS schema_name,
  t.name AS table_name,
  kc.name AS constraint_name,
  c.name AS column_name,
  ic.key_ordinal
FROM sys.key_constraints AS kc
INNER JOIN sys.tables AS t
  ON kc.parent_object_id= t.object_id
INNER JOIN sys.schemas AS s
  ON t.schema_id = s.schema_id
INNER JOIN sys.index_columns AS ic
  ON kc.parent_object_id = ic.object_id
  AND kc.unique_index_id = ic.index_id
INNER JOIN sys.columns AS c
  ON ic.object_id = c.object_id
  AND ic.column_id = c.column_id
WHERE kc.[type] = 'PK'

UNION ALL

SELECT
  'FOREIGN KEY' AS constraint_type,
  ps.name AS schema_name,
  pt.name AS table_name,
  fk.name AS constraint_name,
  pc.name AS column_name,
  fkc.constraint_column_id AS key_ordinal
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
  ON fk.object_id = fkc.constraint_object_id
INNER JOIN sys.tables AS pt
  ON fk.parent_object_id = pt.object_id
INNER JOIN sys.schemas AS ps
  ON pt.schema_id = ps.schema_id
INNER JOIN sys.columns AS pc
  ON fkc.parent_object_id = pc.object_id
  AND fkc.parent_column_id = pc.column_id
ORDER BY constraint_type, schema_name, table_name, key_ordinal



--
USE StoreIncentiveOLTP;
GO

SELECT
    fk.name AS foreign_key_name,

    ps.name AS child_schema,
    pt.name AS child_table,
    pc.name AS child_column,

    rs.name AS parent_schema,
    rt.name AS parent_table,
    rc.name AS parent_column,

    fk.update_referential_action_desc AS on_update_action,
    fk.delete_referential_action_desc AS on_delete_action,

    fk.is_disabled,
    fk.is_not_trusted
FROM sys.foreign_keys AS fk

INNER JOIN sys.foreign_key_columns AS fkc
    ON fk.object_id = fkc.constraint_object_id

INNER JOIN sys.tables AS pt
    ON fkc.parent_object_id = pt.object_id

INNER JOIN sys.schemas AS ps
    ON pt.schema_id = ps.schema_id

INNER JOIN sys.columns AS pc
    ON fkc.parent_object_id = pc.object_id
    AND fkc.parent_column_id = pc.column_id

INNER JOIN sys.tables AS rt
    ON fkc.referenced_object_id = rt.object_id

INNER JOIN sys.schemas AS rs
    ON rt.schema_id = rs.schema_id

INNER JOIN sys.columns AS rc
    ON fkc.referenced_object_id = rc.object_id
    AND fkc.referenced_column_id = rc.column_id

ORDER BY
    child_schema,
    child_table,
    foreign_key_name,
    fkc.constraint_column_id;
GO

---
USE StoreIncentiveOLTP;
GO

SELECT
    s.name AS schema_name,
    t.name AS table_name,
    cc.name AS constraint_name,
    'CHECK' AS constraint_type,
    cc.definition AS constraint_definition,
    cc.is_disabled
FROM sys.check_constraints AS cc
INNER JOIN sys.tables AS t
    ON cc.parent_object_id = t.object_id
INNER JOIN sys.schemas AS s
    ON t.schema_id = s.schema_id

UNION ALL

SELECT
    s.name,
    t.name,
    dc.name,
    'DEFAULT',
    dc.definition,
    dc.is_system_named
FROM sys.default_constraints AS dc
INNER JOIN sys.tables AS t
    ON dc.parent_object_id = t.object_id
INNER JOIN sys.schemas AS s
    ON t.schema_id = s.schema_id

UNION ALL

SELECT
    s.name,
    t.name,
    i.name,
    'UNIQUE',
    STRING_AGG(c.name, ', '),
    i.is_disabled
FROM sys.indexes AS i
INNER JOIN sys.tables AS t
    ON i.object_id = t.object_id
INNER JOIN sys.schemas AS s
    ON t.schema_id = s.schema_id
INNER JOIN sys.index_columns AS ic
    ON i.object_id = ic.object_id
    AND i.index_id = ic.index_id
INNER JOIN sys.columns AS c
    ON ic.object_id = c.object_id
    AND ic.column_id = c.column_id
WHERE i.is_unique = 1
  AND i.is_primary_key = 0
  AND ic.key_ordinal > 0
GROUP BY
    s.name,
    t.name,
    i.name,
    i.is_disabled

ORDER BY
    schema_name,
    table_name,
    constraint_type;
GO

--
USE StoreIncentiveOLTP;
GO

DECLARE @sql NVARCHAR(MAX);

SELECT
    @sql = STRING_AGG(
        CAST(
            'SELECT ' +
            '''' + s.name + ''' AS schema_name, ' +
            '''' + t.name + ''' AS table_name, ' +
            'COUNT_BIG(*) AS row_count ' +
            'FROM ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name)
            AS NVARCHAR(MAX)
        ),
        ' UNION ALL '
    )
FROM sys.tables AS t
INNER JOIN sys.schemas AS s
    ON t.schema_id = s.schema_id
WHERE s.name IN ('retail', 'hr', 'clinical', 'ops');

SET @sql = @sql +
    ' ORDER BY schema_name, table_name;';

EXEC sys.sp_executesql @sql;
GO