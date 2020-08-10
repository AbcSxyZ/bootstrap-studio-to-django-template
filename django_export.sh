#!/bin/bash

SCRIPT_DIR=$(dirname $0)
BSS_DIR=$1

function load_venv()
{
    local env_file=$SCRIPT_DIR/env

    source $env_file

    if [ -n "$VIRTUAL_ENV" ]
    then
        #Activate virtual env
        source $SCRIPT_DIR/$VIRTUAL_ENV/bin/activate
    fi
}

#Load virtual env if necessary
load_venv

#Run bss template converter
python3 $SCRIPT_DIR/converter.py $1
