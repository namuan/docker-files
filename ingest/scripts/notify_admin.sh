#!/usr/bin/env bash
if [[ $# -eq 0 ]] ; then
    echo 'Job type (dockerfile or dockercompose) required as first argument'
    exit 0
fi

source .env

JOBTYPE="$1"

curl -s -F "token=${PUSHOVER_TOKEN}" \
    -F "user=uJ4uDGCKmkD5vaAnK26QkUqLXofXGp" \
    -F "title=Dockerfiles" \
    -F "message=Finished downloading ${JOBTYPE}" https://api.pushover.net/1/messages.json
