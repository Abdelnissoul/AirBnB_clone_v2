-- Configures a MySQL server with the following specifications:
--   - Database: hbnb_test_db
--   - User: hbnb_test with password hbnb_test_pwd on localhost
--   - Grants all privileges for hbnb_test on hbnb_test_db
--   - Grants SELECT privilege for hbnb_test on performance_schema

-- Creates the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Creates the user if it doesn't already exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grants all privileges on hbnb_test_db to the hbnb_test user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grants SELECT privilege on performance_schema to the hbnb_test user
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flushes privileges to apply changes
FLUSH PRIVILEGES;
