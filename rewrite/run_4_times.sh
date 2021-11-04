#!/bin/bash

python3 main.py --multirun upper_swing=0.0,0.1,0.2,0.3 & python3 main.py --multirun upper_swing=0.4,0.5,0.6 & python3 main.py --multirun upper_swing=0.7,0.8,0.9,1.0
