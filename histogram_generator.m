clear;
clc;
close all;

delays = importdata('Data/long_test_4_output.csv');
% delays2 = importdata('Data/long_test_2_output.csv');

% delays = [delays1; delays2];

type = 6;

max_delay = max(delays);
min_delay = min(delays);

fprintf('Max: %g ms\n', max_delay/1000);
fprintf('Min: %g ms\n', min_delay/1000);

switch type
    case 1
        categories = 10.^(2:0.2:8);

        % histogram(delays, categories)
        % set(gca, 'YScale', 'log')
        % set(gca, 'XScale', 'log')

        % log_d_pos = log10(abs(delays(delays>0)));
        % log_d_neg = log10(abs(delays(delays<0)));

        delay_pos = delays(delays>0);
        delay_neg = abs(delays(delays<0));

        histogram(delay_pos, categories)
        hold on
        histogram(delay_neg, categories)
        set(gca, 'YScale', 'log')
        set(gca, 'XScale', 'log')
   
    case 2        
        edge = 3000;
        step = 100;
        categories = 0:step:edge;
        histogram(abs(delays(delays<0)), categories)
        hold on
        histogram(delays(delays>0), categories)
%         set(gca, 'YScale', 'log')
%         set(gca, 'XScale', 'log')

    case 3
        edge = 30*1000;
        step = 100;
        categories = -edge:step:edge;
        histogram(delays, categories)
        
        
	case 4
        histogram(delays,1000)
        
    case 5
        delays = [delays, (1:size(delays,1))'];
        hist3(delays, [100, 100])
        xlabel('microseconds'); ylabel('sample');

    case 6
        delays = [delays, (1:size(delays,1))'];
        n = hist3(delays, [100, 100]); % default is to 10x10 bins
        n1 = n';
        n1(size(n,1) + 1, size(n,2) + 1) = 0;
        xb = linspace(min(delays(:,1)),max(delays(:,1)),size(n,1)+1);
        yb = linspace(min(delays(:,2)),max(delays(:,2)),size(n,1)+1);
        h = pcolor(xb,yb,n1);
        h.ZData = ones(size(n1)) * -max(max(n));
        colormap(hot) % heat map
        title('Seamount:Data Point Density Histogram and Intensity Map');
        grid on
        view(3);
        
end