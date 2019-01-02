#!/usr/bin/env bash

PDF_LINK=$1
DEST_FOLDER=$2

if [ -z "$PDF_LINK" ]
then
    echo PDF not provided, exiting.
    exit
fi


if [ -z "$DEST_FOLDER" ]
then
    DEST_FOLDER='/home/jessica/Desktop'
    echo No output given, will write to ${DEST_FOLDER}
fi


python3 download_data.py $PDF_LINK $DEST_FOLDER
