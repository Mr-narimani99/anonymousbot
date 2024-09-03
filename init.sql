CREATE DATABASE IF NOT EXISTS mybot_db;
CREATE USER 'mohammad'@'%' IDENTIFIED WITH 'caching_sha2_password' BY 'Mr.mrn1041378';

-- Grant all privileges on all databases to the user
GRANT ALL PRIVILEGES ON *.* TO 'mohammad'@'%' WITH GRANT OPTION;

-- Apply the changes
FLUSH PRIVILEGES;
