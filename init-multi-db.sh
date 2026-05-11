#!/bin/bash
# This script runs during the first container startup to initialize multiple databases and users.

mariadb -u root -p"$MYSQL_ROOT_PASSWORD" <<-EOSQL
    -- 1. Create Databases
    CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\`;
    CREATE DATABASE IF NOT EXISTS \`$EXPL_MYSQL_DATABASE\`;

    -- 2. Create and Grant simplewebapp User
    CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
    GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';

    -- 3. Create and Grant explicolivais User
    CREATE USER IF NOT EXISTS '$EXPL_MYSQL_USER'@'%' IDENTIFIED BY '$EXPL_MYSQL_PASSWORD';
    GRANT ALL PRIVILEGES ON \`$EXPL_MYSQL_DATABASE\`.* TO '$EXPL_MYSQL_USER'@'%';

    FLUSH PRIVILEGES;
EOSQL
