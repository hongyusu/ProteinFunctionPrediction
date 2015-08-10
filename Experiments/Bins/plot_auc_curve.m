
function plot_auc_curve()

  addpath('./savefigure/');

  [xFilenameList,yFilenameList,svmCList] = textread('parameter_setting','%s %s %s');

  figure1 = figure('visible','off');
  set(figure1, 'PaperUnits', 'centimeters');
  set(figure1, 'Position',[0 0 800 800]);
              
  for i=1:size(xFilenameList,1)
    xFilename = xFilenameList{i};
    yFilename = yFilenameList{i};
    [X] = dlmread(sprintf('../Results/perf_%s_%s',regexprep(xFilename,'.*/',''),regexprep(yFilename,'.*/','')));
    plot(X(:,1),X(:,2));
    hold on;
  end
  lgd = legend(xFilenameList);
  set(lgd, 'interpreter','latex','Position', [0.7,0.5,0.0,0.0]);
  xlabel('False positive rate'); 
  ylabel('True positive rate');
  title('ROC Curves')
  hold off;
  export_fig(sprintf('../Plots/auc.jpg'))

end


