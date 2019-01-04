#!/usr/bin/env bash

PDF_LINK=$1
DEST_FOLDER=$2
FORCE_DL=$3


if [ -z "$PDF_LINK" ]
then
    echo PDF not provided, exiting.
    exit
else
    if [ -z "$FORCE_DL" ]
    then
        python3 paper_helper.py ${PDF_LINK} ${DEST_FOLDER} ${FORCE_DL}
    else
        python3 paper_helper.py ${PDF_LINK} ${DEST_FOLDER}
    fi
fi



# todo : use sed to recreate the new summary filename
# todo call subl on new file
# todo : call evince on original PDF

