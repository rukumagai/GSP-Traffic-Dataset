function [ output_args ] = plot_graph(A, x, y)
% A: adjacency matrix
% x,y: position
  msize=75;
  [ki,kj]=find(A);
%   figure;
  set(gcf,'renderer','zbuffer');
%   set(gcf,'position',[0,600,400,400]);
  %clf('reset');
  hold on
  plot([x(ki)';x(kj)'],[y(ki)';y(kj)'],'Color',[50/255 50/255 50/255],'LineWidth',1.3);
  scatter(x,y,msize,[.5 .5 .5],'k','o','fill');
%  scatter(x,y,msize,S_opt,'o','fill');
  set(gca,'Xtick',[]);
  set(gca,'Ytick',[]);
  axis equal
  axis off

end
