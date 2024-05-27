import util
import numpy as np
from pygsp import graphs, filters


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
    ## Graph construction
    G = graphs.Graph(W)

    ## Plotting signal + graph
    t = 0  # decide the signal time
    util.draw_graph(
        G, pos, data[:, t], image="Italy_Rome_signal.png", fig_title="Italy - Rome"
    )
    util.draw_graph(G, pos, image="Italy_Rome.png", fig_title="Italy - Rome")

    ## Signal Filtering
    ### Noise vector
    data_size = data.shape[0]
    noize_signal = np.random.normal(loc=0, scale=0.75, size=data_size)

    ### Normalize data
    normilized_data = util.normalize_graph_signal(data[:, t])
    noizy_signal = normilized_data + noize_signal

    ### Plot signal
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image="Italy_Rome_normalized_signal.png",
        use_node_values=normilized_data,
        fig_title="Normalized Signal",
    )
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image="Italy_Rome_noisy_signal.png",
        use_node_values=noizy_signal,
        fig_title="Noizy Signal",
    )

    ## Design filter
    g = util.gsp_design_smooth_indicator(G, 0, 0.5)
    x = g.filter(noizy_signal)
    f = util.apply_gft_to_signal(G, normilized_data)
    util.save_gs_spectrum(
        f, save_image_name="Italy_Rome_spectrum.png", fig_title="Signal Spectrum"
    )
    util.save_filter(g, "Italy_Rome_filter.png", fig_title="Filter")

    default_mse = np.sqrt(np.sum((normilized_data - noizy_signal) ** 2)) / G.N
    filtered_mse = np.sqrt(np.sum((normilized_data - x) ** 2)) / G.N

    ## Plot results
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image="Italy_Rome_noisy_signal_with_mse.png",
        use_node_values=noizy_signal,
        fig_title=f"Noizy Signal - MSE: {default_mse:.4f}",
    )
    util.draw_graph(
        G,
        pos,
        data[:, t],
        image="Italy_Rome_filtered_signal.png",
        use_node_values=x,
        fig_title=f"Filtered Signal - MSE: {filtered_mse:.4f}",
    )


if __name__ == "__main__":
    main()
