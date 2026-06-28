%% 电磁学模型对比与安培环路推导
%% MATLAB R2026a LaTeX稳定版

clear;
clc;
close all;


fig = figure(...
    'Name','电磁学模型对比与安培环路推导',...
    'Position',[100 100 1300 650],...
    'Color','w');


%% ================= 长直螺线管 =================

subplot(1,2,1);

hold on;
grid on;
axis equal;
view(35,20);


%% 铁芯

[Xc,Yc,Zc]=cylinder(1.3,60);

Zc=Zc*10-5;


surf(Zc,Xc,Yc,...
    'FaceColor',[0.7 0.7 0.7],...
    'EdgeColor','none',...
    'FaceAlpha',0.35,...
    'DisplayName','铁芯');



%% 线圈

R=1.5;
L=10;
N=16;


t=linspace(0,N*2*pi,2000);


x=linspace(-L/2,L/2,2000);
y=R*cos(t);
z=R*sin(t);



plot3(x,y,z,...
    'Color',[0.65 0.35 0.15],...
    'LineWidth',3,...
    'DisplayName','线圈');



%% 磁感线

yb=linspace(-1,1,5);
zb=linspace(-1,1,5);


[Y,Z]=meshgrid(yb,zb);


id=(Y.^2+Z.^2)<1.1^2;


Y=Y(id);
Z=Z(id);


quiver3(...
    -4.5*ones(size(Y)),...
    Y,Z,...
    9*ones(size(Y)),...
    zeros(size(Y)),...
    zeros(size(Y)),...
    0,...
    'r',...
    'LineWidth',1.5,...
    'MaxHeadSize',0.2,...
    'DisplayName','$B$');



%% 安培环路

plot3([-2.5 2.5 2.5 -2.5 -2.5],...
      [0 0 0 0 0],...
      [0 0 2.8 2.8 0],...
      'b--',...
      'LineWidth',3,...
      'DisplayName','Ampere loop');



%% 文字点

text(-2.5,0,-0.6,'a','FontSize',14);
text(2.5,0,-0.6,'b','FontSize',14);
text(2.5,0,3.3,'c','FontSize',14);
text(-2.5,0,3.3,'d','FontSize',14);



%% 左公式框

annotation('rectangle',...
    [0.12 0.55 0.31 0.32],...
    'FaceColor',[1 1 0.95]);


left_formula={

'\bf 长直螺线管安培环路定理'

'\oint_C \mathbf{B}\cdot d\mathbf{l}=\mu_0 I_{\rm in}'

'\int_a^b Bdl=\mu_0(nL_{ab}I)'

'BL_{ab}=\mu_0 nL_{ab}I'

'\Rightarrow \mathbf{B}=\mu_0 nI'

};


for i=1:length(left_formula)

annotation('textbox',...
    [0.14 0.81-(i-1)*0.055 0.28 0.05],...
    'String',left_formula{i},...
    'Interpreter','latex',...
    'FontSize',13,...
    'EdgeColor','none');

end



title('长直螺线管磁场与安培环路',...
    'FontSize',14,...
    'FontWeight','bold');


xlabel('X');
ylabel('Y');
zlabel('Z');


xlim([-6 6]);
ylim([-4 4]);
zlim([-4 6]);


legend('Interpreter','latex',...
    'Location','northwest');


camlight;
material dull;



%% ================= 螺绕环 =================


subplot(1,2,2);

hold on;
grid on;
axis equal;
view(20,30);



%% 环形铁芯


Rt=4;
rt=0.9;


u=linspace(0,2*pi,80);
v=linspace(0,2*pi,50);


[U,V]=meshgrid(u,v);


Xt=(Rt+rt*cos(V)).*cos(U);
Yt=(Rt+rt*cos(V)).*sin(U);
Zt=rt*sin(V);



surf(Xt,Yt,Zt,...
    'FaceColor',[0.45 0.45 0.45],...
    'EdgeColor','none',...
    'FaceAlpha',0.45,...
    'DisplayName','环形铁芯');



%% 环形线圈


turns=45;


tt=linspace(0,2*pi,2500);


theta=turns*tt;


xc=(Rt+cos(theta)).*cos(tt);
yc=(Rt+cos(theta)).*sin(tt);
zc=sin(theta);



plot3(xc,yc,zc,...
    'Color',[0.1 0.5 0.25],...
    'LineWidth',2.5,...
    'DisplayName','线圈');



%% 磁场方向


tb=linspace(0,2*pi,18);


quiver3(...
    Rt*cos(tb),...
    Rt*sin(tb),...
    zeros(size(tb)),...
    -sin(tb),...
    cos(tb),...
    zeros(size(tb)),...
    0.5,...
    'r',...
    'LineWidth',2,...
    'MaxHeadSize',0.5,...
    'DisplayName','$B$');



%% 安培环路


tl=linspace(0,2*pi,300);


plot3(Rt*cos(tl),...
      Rt*sin(tl),...
      zeros(size(tl)),...
      'c--',...
      'LineWidth',3,...
      'DisplayName','Ampere loop');



%% 右公式框


annotation('rectangle',...
    [0.56 0.55 0.32 0.32],...
    'FaceColor',[0.93 1 0.95]);



right_formula={


'\bf 螺绕环安培环路定理'

'\oint_C \mathbf{B}\cdot d\mathbf{l}=\mu_0 I_{\rm in}'

'B(2\pi r)=\mu_0 NI'

'\Rightarrow B=\frac{\mu_0 NI}{2\pi r}'

'\cdot\;磁场集中在环内'

'\cdot\;环外 B=0'

};



for i=1:length(right_formula)


annotation('textbox',...
    [0.58 0.81-(i-1)*0.055 0.28 0.05],...
    'String',right_formula{i},...
    'Interpreter','latex',...
    'FontSize',13,...
    'EdgeColor','none');

end



title('螺绕环磁场与安培环路',...
    'FontSize',14,...
    'FontWeight','bold');


xlabel('X');
ylabel('Y');
zlabel('Z');


xlim([-7 7]);
ylim([-7 7]);
zlim([-4 6]);


legend('Interpreter','latex',...
    'Location','northwest');


camlight;
material dull;
