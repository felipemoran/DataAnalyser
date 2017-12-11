clear;
clc;
close all;

% delays = importdata('Data/ubuntu_night_gologic_output-3.0.csv');
delays = importdata('Data/molink_gologic_output-3.0.csv');
delays = delays.data;
% delays2 = importdata('Data/ema_quinta_a_sexta.csv');
% delays = [delays1; delays2];

% delays = delays(abs(delays(:,1))<1*10^5, :);

type = 7;

% delays = delays(1:32000, :);

max_delay = max(delays(:,1));
min_delay = min(delays(:,1));

fprintf('Max: %g ms\n', max_delay/1000);
fprintf('Min: %g ms\n', min_delay/1000);
fprintf('Total time: %g h\n', delays(end,2)/1000000/3600);


switch type
    case 1
        categories = 10.^(2:0.2:8);

        % histogram(delays, categories)
        % set(gca, 'YScale', 'log')
        % set(gca, 'XScale', 'log')

        % log_d_pos = log10(abs(delays(delays>0)));
        % log_d_neg = log10(abs(delays(delays<0)));

        delay_pos = delays(delays(:,1)>0);
        delay_neg = abs(delays(delays(:,1)<0));

        histogram(delay_pos, categories)
        hold on
        histogram(delay_neg, categories)
        set(gca, 'YScale', 'log')
        set(gca, 'XScale', 'log')
   
    case 2        
        edge = 500*1000;
        step = 100;
        categories = 0:step:edge;
        histogram(abs(delays(delays(:,1)<0)), categories)
        hold on
        histogram(delays(delays(:,1)>0), categories)
        set(gca, 'YScale', 'log')
        set(gca, 'XScale', 'log')

    case 3
        edge = 500*1000;
        step = 1;
        categories = -edge:step:edge;
        [histFreq, histXout] = hist(delays(:,1), categories);
        histogram(delays(:,1), categories)
        
        figure;
        bar(histXout, histFreq/sum(histFreq)*100);
        xlabel('offset (us)');
        ylabel('Frequency (percent)');
        
	case 4
        histogram(delays(:,1),1000)
        
    case 5
%         delays = [delays, (1:size(delays,1))'];
        delays = delays(abs(delays(:,1))<1000, :);
        hist3(delays, [500, 20])
        xlabel('microseconds'); ylabel('sample');

    case 6
%         delays = [delays, (1:size(delays,1))'];
        delays = delays(abs(delays(:,1))<500, :);
        
        n = hist3(delays, [300, 50]); % default is to 10x10 bins
        n1 = n';
        n1(size(n',1) + 1, size(n',2) + 1) = 0;
        xb = linspace(min(delays(:,1)),max(delays(:,1)),size(n,1)+1);
        yb = linspace(min(delays(:,2)),max(delays(:,2)),size(n,2)+1);
        h = pcolor(xb,yb,n1);
        h.ZData = ones(size(n1)) * -max(max(n));
%         colormap(hot) % heat map
%         title('Seamount:Data Point Density Histogram and Intensity Map');
        grid on
        view(3);
        
    case 7
        plot(delays(:,2), delays(:,1))
        xlabel('time (us)'); ylabel('offset (us)');
end