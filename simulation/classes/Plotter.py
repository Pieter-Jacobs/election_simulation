from imports import *
import numpy as np
class Plotter:
    def __init__(self) -> None:
        pass
    

    def plot_parties_2d(self, parties):
        pca = PCA(n_components=2)
        parties_2d = pca.fit_transform(parties)
        print(parties_2d)
        x = [party[0] for party in parties_2d]
        y = [party[1] for party in parties_2d]
        fig, ax = plt.subplots()
        ax.scatter(x=x, y=y)       
        for i, (x0, y0) in enumerate(zip(x, y)):
            ab = AnnotationBbox(OffsetImage(plt.imread(hydra.utils.get_original_cwd() + os.path.sep + 'party_logos' + os.path.sep + str(i) + '.png'), zoom = 0.1), (x0, y0), frameon=False)
            ax.add_artist(ab)
            ax.autoscale()
        plt.show()
        pass


    def plot_heatmaps(self):
        pass
    
    def plot_strategic_voting():
        pass

    def plot_election_results():
        pass
