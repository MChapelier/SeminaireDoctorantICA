# SeminaireDoctorantICA

Here are several Python files to show what can be done with Python in solid mechanics. They are destined to be shown at the Institut Clement Ader PhD seminar (Toulouse, France), and designed to be understandable for people who have never seen Python code.

They can be divided into 3 small projects :

1) Python as a calculator / as a basic engineering tool
Basic use of Matplotlib and Numpy libraries are shown. It is not taking advantage of Python greatest features, but it introduces helpful functions with a concrete example.
Basic_use_Cantilever_beam.py

2) A (little of) object-oriented programming
How to create a class and functions in another file. Small FE code for T3 meshes and nodal forces.
Objects_and_functions_Cantilever_beam.py
class_and_functions.py
BeamMesh.msh

3) Getting help from stackoverflow and github users to improve one's projects / learn new tricks
I once wondered if it was possible to modify geometries "by hand", to modify a plot by clicking on the figure. Someone had already had that question answered on Stackoverflow. After some modifications to adapt it to an INSA practical course, here is the result.
DragPoint_PlotSpline.py

Another file, BeamMesh.geo, can be used to generate other meshes or other geometries with GMSH, a free meshing software.




