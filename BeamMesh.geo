// Gmsh project created on Tue Oct 13 13:32:32 2020
//+
L = 3;
h = 0.6;
l1 = 0.06;
Point(1) = {0, 0, 0, l1};
Point(2) = {L, 0, 0, l1};
Point(3) = {L, h, 0, l1};
Point(4) = {0, h, 0, l1};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
//+
Transfinite Surface {1};
