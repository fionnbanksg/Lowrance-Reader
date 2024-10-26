%% CALIBRATION FILE USED FOR HDS7 ECHO SOUNDER

%% To adjust parameters, change data inside braces

%% BEGIN CALIBRATION FILE
freq <120e3> ##operating frequency (hz)
zer <180> ##receiver impedance (ohm)
zet <2500> ##transducer equiv impedance (ohm)
alpha <0.0035> ##absorption coefficient (dm/m)
c <1500> ##speed of sound in water (m/s)
g <15.42> ##calib xdcr gain
pt <300> ##transmission power (W)
spline <calibration/splines/spline_data_20m.mat>