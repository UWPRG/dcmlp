import numpy as np
from pytrr import GroTrrReader
import pandas as pd
from sklearn import utils
from tqdm import trange

def get_energy(colvar, frames):
    with open('../WTE_1/COLVAR', 'r') as c:
        c = c.readlines()
    c = [l.rstrip('\n') for l in c]
    energy = []
    for e in c[1:frames+1]:
    #     print(e.split())
        energy.append(e.split()[1])
    energy = [float(e)*0.239006 for e in energy]
    energy = np.array(energy)
    return energy

def make_npz(traj, colvar, frames, npzfile, nmols):
    fxyz = []
    xyz = []
    with GroTrrReader(traj) as trrfile:
        for frame in trrfile:
            frame_data = trrfile.get_data()
            fxyz.append(frame_data['f'])
            xyz.append(frame_data['x'])
            if len(xyz) > frames:
                break
    fxyz = np.array(xyz)
    xyz = np.array(fxyz)

    fxyz = np.multiply(fxyz,0.0239006)
    xyz = np.multiply(xyz,10)


    with open(colvar, 'r') as col:
        col = col.readlines()
    col = [l.rstrip('\n') for l in col]

    energy = get_energy(colvar, frames)
    w_name = np.array(b'water_trr_xyz')
    w_theory = np.array(b'')
    w_type = np.array(b'd')
    w_z = np.array([8,1,1]*nmols, dtype='uint8')
    np.savez(npzfile, E=energy, R=xyz, F=fxyz, theory=w_theory, type=w_type, z=w_z)
