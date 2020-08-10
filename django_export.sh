#!/bin/bash

SCRIPT_DIR=$(dirname $0)
BSS_DIR=$1

function load_venv()
{
    local env_file=$SCRIPT_DIR/env

    source $env_file

    if [ -n "$VIRTUAL_ENV" ]
    then
        #Actiave virtual env
        source $SCRIPT_DIR/$VIRTUAL_ENV/bin/activate
    fi
}

load_venv
