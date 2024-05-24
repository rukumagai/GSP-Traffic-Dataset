import util
import numpy as np
from pygsp import graphs


def main():

    npz_path = util.top_dir() / "train" / "Italy_Rome.npz"
    npz = np.load(npz_path)
    N, T, W, L, data, pos = (
        npz["N"],
        npz["T"],
        npz["W"],
        npz["L"],
        npz["data"],
        npz["pos"],
    )
    G = graphs.Graph(W)

    t = 0
    util.draw_graph(G, pos, data[:, t], iamge="Italy_Rome_signal.png")
    util.draw_graph(G, pos, image="Italy_Rome.png")


if __name__ == "__main__":
    main()
