#!/usr/bin/env bash

#given
# python3 task.py "$@"

# create var pythonScriptLocation with value of current bash file location
pythonScriptLocation="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/task.py"
# run python script with arguments
# echo "python3 ${pythonScriptLocation} $@";
python3 ${pythonScriptLocation} $@
