#!/bin/bash
# Creates reporting DB, migration/admin user, and app user with proper privileges
# Usage: ./setup_reporting_db.sh

DB_NAME="ardeo-services"
ADMIN_USER="ardeo_admin"
ADMIN_PASS="adminpassword"
APP_USER="reporting_user"
APP_PASS="apppassword"

# Check if running as postgres user
if [[ $EUID -ne 0 ]]; then
   echo "Please run as root or use sudo."
   exit 1
fi

# Create DB and Admin User
sudo -u postgres psql <<EOSQL
-- Drop DB if exists (optional)
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $ADMIN_USER;
DROP USER IF EXISTS $APP_USER;

CREATE USER $ADMIN_USER WITH PASSWORD '$ADMIN_PASS';
CREATE DATABASE $DB_NAME OWNER $ADMIN_USER;

-- App user
CREATE USER $APP_USER WITH PASSWORD '$APP_PASS';

-- Grant privileges to app user
GRANT CONNECT ON DATABASE $DB_NAME TO $APP_USER;
\c $DB_NAME
GRANT USAGE ON SCHEMA public TO $APP_USER;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $APP_USER;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $APP_USER;

-- Default privileges for future tables/sequences
ALTER DEFAULT PRIVILEGES FOR USER $ADMIN_USER IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $APP_USER;
ALTER DEFAULT PRIVILEGES FOR USER $ADMIN_USER IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO $APP_USER;
EOSQL

echo "Reporting database and users created successfully."
