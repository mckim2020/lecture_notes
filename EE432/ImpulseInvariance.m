% Cheebyshev analog filter design  

% Settings 
wp = 0.3*pi;
ws = 0.4*pi;
atp = 0.2;
ats = 20;

% Take sampling period as 1
Td = 1;

% Scaling
Wp = wp / Td; % Pass Band 
Ws = ws / Td; % Stop Band 
 
[n, Wc] = cheb1ord(Wp, Ws, atp, ats, 's');
[b, a] = cheby1(n, atp, Wc, 's');
[bt, at] = lp2lp(b, a, Wc); % Cutoff freq manipulation (for analog filter)

% Impulse Invariance Transform
[bz, az] = impinvar(bt, at, 1/Td);
zplane(bz, az);

% Calculations
fvtool(bz, az);
zplane(bz, az);




