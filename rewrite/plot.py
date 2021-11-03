from imports import *
from serialize import *
import numpy as np


def average_results(folder_path: str, n_runs: int, type: str):
    x = [x for x in np.arange(0, 1.1, 0.1)]
    y = []
    stdevs = []
    for s in x:
        values = []
        if s == 0 or s == 1:
            s = int(s)
        for run in range(n_runs):
            path = folder_path + os.sep + "2021" + "_swing_" + \
                str(round(s, 1)) + "_run_" + str(run)
            if type == 'float':
                values.append(read_float_from_file(path))
            elif type == 'matrix':
                values.append(read_matrix_from_file(path))
            elif type == 'list':
                values.append(read_list_from_file(path))
        stdevs.append(np.std(values))
        y.append(sum(values)/n_runs)
    return x, y, stdevs


def plot_strategic_voting(folder_path: str, n_runs: int, filename: str) -> None:
    x, y, stdevs = average_results(folder_path, n_runs, type='float')
    plt.plot(x, y)
    plt.title("Swing vs Strategic votes")
    plt.xlabel(r"$s^\uparrow$")
    plt.ylabel("Strategic voting percentage")
    plt.ylim([0, 100])
    plt.errorbar(x, y, stdevs)
    plt.savefig(os.getcwd() + os.sep + "img" + os.sep + "figures" + os.sep
                + "linegraphs" + os.sep + filename + ".pdf")
    plt.show()

def plot_heatmap(folder_path: str, n_runs: int, filename: str) -> None:
    x, y, _ = average_results(folder_path, n_runs, type="matrix")
    for swing, matrix in zip(x, y):
        seaborn.heatmap(matrix, vmin=0, vmax=100, cmap="vlag")
        plt.xlabel("Voted For")
        plt.ylabel("Original Party")
        plt.suptitle(f"Voter Distribution for s of {round(swing,1)}")
        plt.show()
        plt.close()

def plot_histogram(folder_path: str, n_runs: int, filename: str) -> None:
    x, y, stdevs = average_results(folder_path, n_runs, type="list")
    party_mappings = [i for i in range(0, len(y[0]))]
    for result, stdev in zip(y,stdevs):
        plt.bar(party_mappings, result)
        #plt.errorbar(x, stdev)
        plt.xticks(party_mappings)
        plt.ylabel("Number of seats")
        plt.xlabel("Party")
        plt.show()
    pass


def main():
    data_folder = os.getcwd() + os.sep + "data" + os.sep
    plot_strategic_voting(folder_path=data_folder
                          + "strategic_voting_stats", n_runs=5, filename="first_election")
    plot_heatmap(folder_path=data_folder
                 + "voter_matrices", n_runs=5, filename="")
    plot_histogram(folder_path=data_folder
                   + "election_results", n_runs=5, filename="")


if __name__ == "__main__":
    main()
