#!/usr/bin/env bash

CREDS="root"
HOST="localhost"
MYSQL="$(which mysql)"
MYSQLDUMP="$(which mysqldump)"
BACKUP_DIR="/var/lib/mysql/backup"
QUERY="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT REGEXP 'backup|mysql|information_schema|performance_schema'"
GZIP="$(which gzip)"
NOW=$(date +"%Y-%m-%d_%R")

DBS="$(${MYSQL} -h ${HOST} -u ${CREDS} -p${CREDS} -Bse "${QUERY}")"
for DB in ${DBS}
  do
    FILE=${BACKUP_DIR}/${DB}_${NOW}.gz
    ${MYSQLDUMP} -h ${HOST} -u ${CREDS} -p${CREDS} ${DB} | ${GZIP} -9 > ${FILE}
done
