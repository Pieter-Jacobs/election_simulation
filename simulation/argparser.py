#!/bin/python3

import argparse

parser = argparse.ArgumentParser(description="Strategic voting simulation.")
parser.add_argument("-N", metavar="nr_agents", nargs=1, type=int, help="Number of agents, default = 100", default=100)
parser.add_argument("-P", metavar="nr_parties", nargs=1, type=int, help="Number of parties, default = 10", default=10)

args = parser.parse_args()

def main():
  nr_of_agents = args.N
  nr_of_parties = args.P


if __name__ =="__main__":
  main()