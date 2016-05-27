DO
$do$
BEGIN

IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'gestfg') THEN
   RAISE NOTICE 'Database already exists';
ELSE
   PERFORM dblink_exec('dbname=' || current_database()  -- current db
                     , 'CREATE DATABASE gestfg');
END IF;

END
$do$
