from statistics import stdev
import matplotlib.pyplot as plt
import os
import seaborn

from numpy.lib.function_base import average 

VOTERS = 100000


def average_matrix(matrices):
  avg_matrix = [[0 for _ in row] for row in matrices[0]]

  for matrix in matrices:
    for idx, row in enumerate(matrix):
      for jdx, entry in enumerate(row):
        avg_matrix[idx][jdx] += entry
  
  avg_matrix = [[entry / len(matrices) for entry in row] for row in avg_matrix]
  to_return = []
  for row in avg_matrix:
    total = sum(row)
    new_row = []
    for entry in row:
      new_row.append(entry / total * 100 if total > 0 else 0)
    
    to_return.append(new_row)
  return to_return


def heat_map(matrix, label):
  seaborn.heatmap(matrix, vmin=0, vmax=100, cmap="vlag")
  plt.xlabel("Voted For")
  plt.ylabel("Original Party")
  plt.suptitle(f"Voter Distribution for swing of {label}")
  plt.savefig(os.getcwd() + os.sep + "figures" + os.sep + "heatmap" + str(label) + ".pdf")
  plt.show()
  


def get_stats():
  saved_files_folder = os.getcwd() + os.sep + "saver" + os.sep
  strategic_votes = {k/10: [] for k in range(11)}
  matrices = {k/10: [] for k in range(11)}
  
  stat_files = os.listdir(saved_files_folder)
  stat_files.sort()
  for filename in stat_files:
      with open(saved_files_folder + filename, "r") as f:
          firstline = f.readline()
          swing, strat_vote = firstline.split(" ")
          strategic_votes[float(swing)].append(int(strat_vote[:-1]))

          f.readline() ## Votes (not required)
          f.readline() ## seats (not required)
          matrix = []
          for line in f.readlines():
            entries = line.split('|')
            matrix.append([int(entry.strip()) for entry in entries if entry.strip() != ""])
            
          print(matrix)
          
          matrices[float(swing)].append(matrix)
  
  for k in matrices.keys():
    matrices[k] = average_matrix(matrices[k])

 
  return strategic_votes, matrices


def plot(strategic_votes: dict) -> None:
  swings = []
  strat_votes = []
  stddevs = []

  for k, v in strategic_votes.items():
    swings.append(k)
    strat_votes.append(average(v) / VOTERS * 100)
    stddevs.append(stdev(v) / VOTERS * 100 if len(v) > 1 else 0)
  
  print(swings)
  print(strat_votes)
  print(stddevs)

  plt.plot(swings, strat_votes)
  plt.xlabel("Max swing")
  plt.ylabel("Strategic voting percentage")
  plt.title("Swing vs Strategic votes")
  plt.axis([0, 1, 0, 1.25 * max(strat_votes)])
  plt.errorbar(swings, strat_votes, stddevs)
  plt.savefig(os.getcwd() + os.sep + "figures" + os.sep + "graph.pdf")
  plt.show()


def main():
  strategic_votes, matrices = get_stats()
  plot(strategic_votes)
  for idx in range(11):
    heat_map(matrices[idx/10], label = idx / 10)



if __name__=="__main__":
    main()