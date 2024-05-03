--   Let's create a MySQL server with:
--   hbnb_dev_db Database.
--   a user with password hbnb_dev_pwd in the localhost.
--   making sure that all privileges for hbnb_dev on hbnb_dev_db.
--   and SELECT privilege for hbnb_dev on performance.

-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- all privileges on hbnb_dev_db to hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- SELECT privilege on performance_schema to hbnb_dev
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
