#!/bin/bash

python3 main.py --multirun upper_swing=0.0,0.1,0.2 & python3 main.py --multirun upper_swing=0.3,0.4,0.5 & python3 main.py --multirun upper_swing=0.6,0.7,0.8 & python3 main.py --multirun upper_swing= 0.9,1.0
