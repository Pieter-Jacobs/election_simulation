# DoMAS
Design of Multi-Agent Systems

Thijs Visee - s2982129 <br>
Pieter Jacobs - s3777693 <br>
Mathew Melcherts - s3777693

This repo will be used to investigate the influence of strategic voting on democratic elections by using a simulation with multiple agents having different political profiles. These agents will be used to see how the election results change when agents vote on parties that are not a perfect fit for their profile, but have similar ideas and a larger chance to end up governing the country. 

## Installation
Python 3 is required to run this project.
Moreover, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following dependencies:
```bash
pip install dill hydra matplotlib numba sklearn seaborn
```
## Usage
To run the model:
```bash
    python main.py -m swing=0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0 polls=polls_2012
    python main.py -m swing=0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0 polls=polls_2021
    python plot.py
```