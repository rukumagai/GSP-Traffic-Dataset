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

    t = 0  # decide the signal time
    util.draw_graph(G, pos, data[:, t], image="Italy_Rome_signal.png")
    util.draw_graph(G, pos, image="Italy_Rome.png")

    normilized_data = util.normalize_graph_signal(data[:, t])
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image="Italy_Rome_normalized_signal.png",
        normalized_data=normilized_data,
    )

    gft_signal = util.apply_gft_to_signal(G, normilized_data)
    util.save_gs_spectrum(gft_signal, save_image_name="Italy_Rome_spectrum.png")


if __name__ == "__main__":
    main()
