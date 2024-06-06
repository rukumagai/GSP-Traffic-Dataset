%% Demo for GSP_Traffic Dataset

%Loading Data
path_name = "gsp/gspbox/gsp_traffic_directed";

country_name = "Italy";
city_name = "Rome";

load(path_search_directed(city_name))

%% Visualizatoin
% Graph construction
G = gsp_graph(double(W),pos);

% Plotting signal + graph
figure;
gsp_plot_signal(G,data(:,1));title(country_name +' - '+ city_name,FontSize=16);

%% Signal Filtering
G = gsp_compute_fourier_basis(G);

% Noize vector
noize = mvnrnd(zeros(N,1),0.75^2*eye(N));

% Normalize data
signal = double(data(:,1));
signal = (signal-mean(signal))./std(signal);
noizy_signal = signal + noize';

% Plot signal
figure;
subplot(121);gsp_plot_signal(G,signal);title("Normalized Signal",FontSize=16);lim=clim;
subplot(122);gsp_plot_signal(G,noizy_signal);title("Noisy Signal",FontSize=16);clim(lim);

%%
% Design filter
g = gsp_design_smooth_indicator(G,0.1,0.5);
x = gsp_filter(G,g,noizy_signal);
f = gsp_gft(G,signal);
% Plot filter and signal spectrum
figure;
subplot(121);gsp_plot_signal_spectral(G,f);title("Signal Spectrum",FontSize=16);
subplot(122);gsp_plot_filter(G,g);title("Filter",FontSize=16);
saveas(gcf,"filter.png")

default_mse = sqrt(sum((signal-noizy_signal).^2))/G.N;
filtered_mse = sqrt(sum((signal-x).^2))/G.N;

% Plot results
figure;
subplot(121);gsp_plot_signal(G,signal);title("Noisy Signal - MSE: "+num2str(default_mse,'%.4f'),FontSize=16);clim(lim);
subplot(122);gsp_plot_signal(G,x);title("Filtered Signal - MSE: "+num2str(filtered_mse,'%.4f'),FontSize=16);clim(lim);