#!/bin/bash

# Теперь можно запускать из любой директории
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

python3 -u "extractor_gen.py" && python3 -u "extractor.py" & python3 -u "bot_news.py"