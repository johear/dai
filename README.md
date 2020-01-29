# dai
Trying to keep it as close to the jetson tx2 version, so using tensorflow-gpu 1.14

Requirements:

Try the Dai-Simulation.yml file:
conda env create -f Dai-Simulation.yml

OR

conda env create -f Dai-Simulation python==3.7

conda install pip

conda install numpy (installed numpy 1.18.1)

conda install keras-gpu (installed keras-gpu 2.2.4-0, tensorflow-gpu 1.14.0, H5py, etc.) 

conda install paramiko (installed paramiko 2.4.2)

pip install pypozyx (or python -m pip install pypozyx) -->both launch the __main__.py in the pip package

pip install pybullet (installed pybullet 2.6.4)

