#!/usr/bin/env bash

#SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "/opt/apps/systemStatus/scripts/config.cfg"

bash -c "${PYTHON_INTERPETER} ${HOME_FOLDER}/src/systemStatus.py $@"


