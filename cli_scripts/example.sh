#!/usr/bin/env bash

# Create env_file to read USERNAME, PASSWORD and URL, see env_file_git_keep for reference
source ./env_file
FOLDER=/tmp/out

docker run omero-user-scripts:ome5-4-1 \
bash -c "mkdir -p ${FOLDER} && cd /tmp && OMERO_USERNAME='${USERNAME}' OMERO_USER_PASSWORD='${PASSWORD}' OMERO_APP_URL='${URL}' python download_files.py -d 2071 -p 759 -o -f '${FOLDER}'" -v ${FOLDER}:${FOLDER}
