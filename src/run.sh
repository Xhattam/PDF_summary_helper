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
    echo "No output given, will write to ${DEST_FOLDER}"
fi

echo "Searching for downloadeble sources..."

python3 download_data.py ${PDF_LINK} ${DEST_FOLDER}

echo "Sources found, searching for source .tex file to parse..."

python3 parse_latex.py ${DEST_FOLDER}

echo "Summary created, opening text editor and source PDF..."

# todo : use sed to recreate the new summary filename
# todo call subl on new file
# todo : call evince on original PDF

