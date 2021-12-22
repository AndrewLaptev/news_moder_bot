#!/bin/bash

python3 -u "extractor_gen.py" && python3 -u "extractor.py" & python3 -u "bot_news.py"