% Cheebyshev analog filter design  

% Settings 
wp = 0.3*pi;
ws = 0.4*pi;
atp = 0.2;
ats = 20;

% Take sampling period as 1
Td = 1;

% Scaling
Wp = 2/Td * tan(wp/2);
Ws = 2/Td * tan(ws/2);
[n, Wc] = cheb1ord(Wp, Ws, atp, ats, 's');
[b, a] = cheby1(n, atp, Wc, 's');
[bt, at] = lp2lp(b, a, Wc); % Cutoff freq to Wc

% Bilinear Transform
[bz, az] = bilinear(bt, at, 1/Td);

% Calculations
fvtool(bz, az);
zplane(bz, az);




