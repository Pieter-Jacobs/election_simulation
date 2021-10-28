from imports import *
import numpy as np
class Plotter:
    def __init__(self) -> None:
        pass
    

    def plot_parties_2d(self, parties):
        pca = PCA(n_components=2)
        parties_2d = pca.fit_transform(parties)
        x = [party[0] for party in parties_2d]
        y = [party[1] for party in parties_2d]
        fig, ax = plt.subplots()
        line = ax.scatter(x=x, y=y)
        for i, (x0, y0) in enumerate(zip(x, y)):
            img = OffsetImage(plt.imread(hydra.utils.get_original_cwd() + os.path.sep + 'party_logos' + os.path.sep + str(i) + '.png'), zoom=0.1)
            ab = AnnotationBbox(img, (x0, y0), frameon=False)
            ax.add_artist(ab)

        # def hover(event):
        #     # if the mouse is over the scatter points
        #     if line.contains(event)[0]:
        #         # find out the index within the array from the event
        #         ind = line.contains(event)[1]["ind"][0]
        #         img = OffsetImage(plt.imread(hydra.utils.get_original_cwd() + os.path.sep + 'party_logos' + os.path.sep + str(ind) + '.png'), zoom=0.1)
        #         ab = AnnotationBbox(img, (x[ind], y[ind]), frameon=False)
        #         ax.add_artist(ab)
        #     fig.canvas.draw_idle()
        # # add callback for mouse moves
        # fig.canvas.mpl_connect('motion_notify_event', hover) 
        plt.show()
        pass


    def plot_heatmaps(self):
        pass
    
    def plot_strategic_voting():
        pass

    def plot_election_results():
        pass
