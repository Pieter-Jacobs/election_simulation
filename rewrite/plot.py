from imports import *
from serialize import *
import numpy as np


def to_str(number: float) -> str:
    return str(round(number, 1))


def average_results(folder_path: str, n_runs: int, type: str, poll: int) -> None:
    x = [x for x in np.arange(0, 1.1, 0.1)]
    y = []
    stdevs = []
    for s in x:
        values = []
        for run in range(n_runs):
            path = folder_path + os.sep + "2021" + "_swing_" + \
                to_str(s) + "_run_" + str(run) + "_poll_" + str(poll)
            if type == 'float':
                values.append(read_float_from_file(path))
            elif type == 'matrix':
                values.append(read_matrix_from_file(path))
            elif type == 'list':
                values.append(read_list_from_file(path))
        stdev = np.std(values) if type == "float" else np.std(values, axis=0)
        stdevs.append(stdev)
        y.append(sum(values)/n_runs)
    return x, y, stdevs


def plot_parties_2d(filename: str, save_folder: str, logos=True) -> None:
    party_profiles = np.genfromtxt(hydra.utils.get_original_cwd(
    ) + os.path.sep + 'party_profiles.csv', delimiter=',')
    pca = PCA(n_components=2)
    profiles_2d = pca.fit_transform(party_profiles)
    x = [profile[0] for profile in profiles_2d]
    y = [profile[1] for profile in profiles_2d]
    fig, ax = plt.subplots()
    plt.title("Party profiles")
    line = ax.scatter(x=x, y=y, s=0)
    for i, (x0, y0) in enumerate(zip(x, y)):
        if logos:
            img = OffsetImage(plt.imread(hydra.utils.get_original_cwd(
            ) + os.path.sep + 'img' + os.sep + 'party_logos' + os.path.sep + str(i) + '.png'), zoom=0.2)
            ab = AnnotationBbox(img, (x0, y0), frameon=False)
            ax.add_artist(ab)
        else:
            plt.text(x0, y0, i, ha="center", va="center")
    fig.set_size_inches(16, 9)
    plt.savefig(save_folder + "party_profiles" + os.sep + filename + ".pdf")
    plt.clf()


def plot_strategic_voting(folder_path: str, save_folder: str, n_runs: int, filename: str, poll: int) -> None:
    x, y, stdevs = average_results(folder_path, n_runs, poll=poll, type='float')
    plt.plot(x, y)
    plt.title("Swing vs Strategic votes")
    plt.xlabel(r"$s^\uparrow$")
    plt.ylabel("Strategic voting percentage")
    plt.ylim([0, 100])
    plt.errorbar(x, y, stdevs)
    plt.savefig(save_folder + "linegraphs" + os.sep + filename + ".pdf")
    plt.clf()


def plot_heatmap(folder_path: str, save_folder: str, n_runs: int, n_voters: int, filename: str, poll: int) -> None:
    x, y, _ = average_results(folder_path, n_runs, poll=poll, type="matrix")
    for swing, matrix in zip(x, y):
        for i in range(len(matrix)):
            row_votes = np.sum(matrix[i])
            matrix[i] = ((matrix[i]/row_votes) * 100) if row_votes > 0 else 0
        seaborn.heatmap(matrix, vmin=0, vmax=100, cmap="vlag", cbar_kws={"label": "Percentage of voters"})
        plt.xlabel("Voted For")
        plt.ylabel("Original Party")
        plt.suptitle(
            r"Voting Distribution for $s^{\uparrow}$ of " + str(round(swing, 1)))
        plt.savefig(save_folder + "heatmaps" + os.sep +
                    filename + "__swing__" + str(swing) + ".pdf")
        plt.clf()


def plot_histogram(folder_path: str, save_folder: str, n_runs: int, filename: str, poll: int) -> None:
    x, y, stdevs = average_results(folder_path, n_runs, poll=poll, type="list")
    party_mappings = [i for i in range(0, len(y[0]))]
    for swing, result, stdev in zip(x, y, stdevs):
        plt.figure(figsize=(16, 9)) 
        n_seats = int(sum(result))
        fig, ax = plt.subplots() 
        plt.barh(party_mappings, result, xerr=stdev,
                align='center', alpha=0.5, ecolor='black', capsize=5)
        for i, v in enumerate(result):
            ax.text(v - v/2, i-0.25, str(v), color='black', fontweight='bold')
        plt.yticks(party_mappings)
        plt.title(
            r"Seat Distribution for $s^{\uparrow}$ of " + str(round(swing, 1)))
        plt.ylabel("Party")
        plt.xlabel("Number of seats")
        fig.set_size_inches(16, 9)
        plt.savefig(save_folder + "bargraphs" + os.sep +
                    filename + "__swing__" + str(swing) + ".pdf")
        plt.clf()


def plot_happiness(folder_path, save_folder, upper_swing) -> None:
    happiness = []
    x = []

    for swing in range(0, int(10 * upper_swing) + 1):
        x.append(swing/ 10)
        path = folder_path + "2021_swing_" + to_str(swing/10)
        happiness.append(read_float_from_file(path))
    plt.plot(x, happiness)
    plt.title("Swing vs Happiness")
    plt.xlabel(r"$s^\uparrow$")
    plt.ylabel("Happiness")
    plt.savefig(save_folder + "happiness" + os.sep + "happiness.pdf")

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    figure_folder = hydra.utils.get_original_cwd() + os.path.sep + "img" + \
        os.sep + "figures" + os.sep
    data_folder = hydra.utils.get_original_cwd() + os.sep + "data" + os.sep
    for poll in range(cfg.n_polls):
        plot_strategic_voting(folder_path=data_folder
                                + "strategic_voting_stats", n_runs=cfg.n_runs, save_folder=figure_folder, filename="first_election", poll=poll)
        plot_heatmap(folder_path=data_folder
                    + "voter_matrices", n_runs=cfg.n_runs, n_voters=cfg.n_voters, save_folder=figure_folder, filename="first_heatmap", poll=poll)
        plot_histogram(folder_path=data_folder
                        + "election_results", save_folder=figure_folder, n_runs=cfg.n_runs, filename="first_histogram", poll=poll)
        plot_parties_2d(filename="profiles_logos", save_folder=figure_folder)
        plot_parties_2d(filename="profiles_text",
                        save_folder=figure_folder, logos=False)
        plot_happiness(data_folder + "/happiness/", figure_folder, cfg.upper_swing)


if __name__ == "__main__":
    main()
