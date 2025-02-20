#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/config.cfg"
python3 -m venv ${HOME_FOLDER}/.venv/
source "${HOME_FOLDER}/.venv/bin/activate"
pip3 install psutil
deactivate