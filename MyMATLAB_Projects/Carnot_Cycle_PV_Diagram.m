clear; clc; close all;

%% Physical parameters (ideal monatomic gas)
n = 1;
R = 8.314;
TH = 420;                % K
TC = 350;                % K
gamma = 5/3;
VA = 0.020;              % m^3
VB = 0.048;              % m^3

k = (TH / TC)^(1 / (gamma - 1));
VC = VB * k;
VD = VA * k;
pA = n * R * TH / VA;
pB = n * R * TH / VB;
pC = n * R * TC / VC;
pD = n * R * TC / VD;

%% Exact Carnot paths (PV = const; PV^gamma = const)
N = 800;
V = cell(1,4);
p = cell(1,4);
V{1} = linspace(VA,VB,N);
p{1} = n*R*TH ./ V{1};
V{2} = linspace(VB,VC,N);
p{2} = pB*(VB./V{2}).^gamma;
V{3} = linspace(VC,VD,N);
p{3} = n*R*TC ./ V{3};
V{4} = linspace(VD,VA,N);
p{4} = pD*(VD./V{4}).^gamma;
for i = 1:4
    V{i} = V{i} * 1000;  % L
    p{i} = p{i} / 1000;  % kPa
end
statesV = [VA VB VC VD]*1000;
statesP = [pA pB pC pD]/1000;

%% Appearance
iso = [0.88 0.34 0.16];
adi = [0.08 0.39 0.75];
colors = {iso,adi,iso,adi};
fig = figure('Color','w','Position',[90 90 1650 690]);
t = tiledlayout(fig,1,2,'TileSpacing','loose','Padding','compact');

for mode = 1:2
    ax = nexttile(t);
    hold(ax,'on'); grid(ax,'on'); box(ax,'on');

    if mode == 1
        fillColor = [1.0 0.78 0.47];
        direction = 1;
        heading = 'Carnot Heat Engine  (A-B-C-D-A)';
    else
        fillColor = [0.56 0.78 1.0];
        direction = -1;
        heading = 'Carnot Refrigerator  (A-D-C-B-A)';
    end

    fill(ax,[V{1} V{2} V{3} V{4}],...
        [p{1} p{2} p{3} p{4}],fillColor,...
        'FaceAlpha',0.36,'EdgeColor','none','HandleVisibility','off');

    hIso = plot(ax,V{1},p{1},'Color',iso,'LineWidth',3.0);
    hAdi = plot(ax,V{2},p{2},'Color',adi,'LineWidth',3.0);
    plot(ax,V{3},p{3},'Color',iso,'LineWidth',3.0,'HandleVisibility','off');
    plot(ax,V{4},p{4},'Color',adi,'LineWidth',3.0,'HandleVisibility','off');

    plot(ax,statesV,statesP,'ko','MarkerFaceColor','k',...
        'MarkerSize',6.5,'HandleVisibility','off');
    labels = {'A','B','C','D'};
    dx = [-2.7,2.4,2.4,-3.5];
    dy = [7,6,-8,-7];
    for i = 1:4
        text(ax,statesV(i)+dx(i),statesP(i)+dy(i),labels{i},...
            'FontSize',15,'FontWeight','bold',...
            'HorizontalAlignment','center');
    end

    title(ax,heading,'FontWeight','bold','FontSize',16);
    xlabel(ax,'Volume V (L)','FontSize',13);
    ylabel(ax,'Pressure p (kPa)','FontSize',13);
    xlim(ax,[12 85]);
    ylim(ax,[30 195]);
    set(ax,'FontSize',12,'LineWidth',1.0,'GridAlpha',0.13,...
        'Layer','bottom');
    legend(ax,[hIso hAdi],{'Isothermal','Adiabatic'},...
        'Location','northeast','Box','off','FontSize',11);

    % IMPORTANT: finish layout first so pixel-to-data conversion is stable.
    drawnow;

    % Every arrow: 68 px long, 16 px away from its curve,
    % drawn as a full shaft + a clearly visible triangular head.
    % Positive offset is consistently on the OUTSIDE of the cycle.
    positions = [0.55 0.55 0.53 0.49];
    for i = 1:4
        drawSideArrow(ax,V{i},p{i},positions(i),direction,...
            colors{i},68,16);
    end
end

eta = 1-TC/TH;
COP = TC/(TH-TC);
fprintf('Heat engine efficiency: %.2f%%\n',eta*100);
fprintf('Refrigerator COP: %.3f\n',COP);
exportgraphics(fig,'Carnot_Cycle_PV_Fixed.png','Resolution',300);

%% Draw a continuous arrow in data space, sized in SCREEN PIXELS.
function drawSideArrow(ax,V,p,fraction,direction,color,lengthPx,offsetPx)
    % Find a point and the local tangent on the ORIGINAL path.
    i = max(6,min(numel(V)-5,round(fraction*numel(V))));

    % Get final on-screen plot width and height.
    oldUnits = ax.Units;
    ax.Units = 'pixels';
    ap = ax.Position;
    ax.Units = oldUnits;
    limX = xlim(ax); limY = ylim(ax);
    sx = ap(3)/diff(limX);   % pixels per L
    sy = ap(4)/diff(limY);   % pixels per kPa

    vx = (V(i+4)-V(i-4))*sx;
    vy = (p(i+4)-p(i-4))*sy;
    unitT = [vx vy]/hypot(vx,vy);
    unitN = [-unitT(2) unitT(1)];

    % For the reverse cycle, reverse only the arrow direction,
    % not the side of the curve where the arrow is drawn.
    vec = direction*unitT;
    center = [V(i)*sx p(i)*sy] + offsetPx*unitN;
    tail = center - 0.5*lengthPx*vec;
    tip = center + 0.5*lengthPx*vec;
    headLength = 15;
    headHalfWidth = 6.5;
    shaftEnd = tip-headLength*vec;

    % Convert pixel-like coordinates back into plot data coordinates.
    plot(ax,[tail(1) shaftEnd(1)]/sx,...
            [tail(2) shaftEnd(2)]/sy,...
            'Color',color,'LineWidth',2.8,...
            'Clipping','off','HandleVisibility','off');

    b1 = shaftEnd + headHalfWidth*[-vec(2) vec(1)];
    b2 = shaftEnd - headHalfWidth*[-vec(2) vec(1)];
    patch(ax,[tip(1) b1(1) b2(1)]/sx,...
             [tip(2) b1(2) b2(2)]/sy,color,...
             'EdgeColor','none','Clipping','off',...
             'HandleVisibility','off');
end
