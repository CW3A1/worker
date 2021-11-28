
from time import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from modules.classes import HeatOptions
from modules.gen import postToDB, uploadToUguu


def heatEquation(heat_options: HeatOptions):
    L_X = heat_options.L_X # X-length of plate
    L_Y = heat_options.L_Y # Y-length of plate
    DX = DY = H = heat_options.H # Step size
    ALPHA = heat_options.ALPHA # Thermal diffusivity in mm2/s
    T = heat_options.T # Total time in seconds
    BOUNDARY_CONDITION = heat_options.BOUNDARY_CONDITION # see line 31 to 36 for more info 
    DT = 0.5/(ALPHA*(10**(-6))/DX**2+1/DY**2) # Von Neumann stability condition
    T_L = int(np.floor(T/DT)) # Amount of discrete time intervals
    yv, xv = np.mgrid[0:L_X:DX, 0:L_Y:DY] # Create meshgrid
    u = np.zeros((T_L, len(xv), len(xv[0]))) # Construct multidimensional array to store meshgrid data over time
    u[0] = np.exp(-yv)+xv # Set initial condition
    for l in range(1, T_L): # Calculate meshgrid data over time progressively
        u[l] = u[l-1] + (np.roll(u[l-1], -1, 0) + np.roll(u[l-1], 1, 0) + np.roll(u[l-1], -1, 1) + np.roll(u[l-1], 1, 1) - 4*u[l-1])*ALPHA*(10**(-6))*DT/H**2 # forward Euler method
        if BOUNDARY_CONDITION == "NO_FLUX":
            u[l][0], u[l][-1] = (4*u[l][1]-u[l][2])/3, (4*u[l][-2]-u[l][-3])/3 # du(x, 0, t)/dx = 0 and du(x, L_Y, t)/dx = 0
            u[l][:, 0], u[l][:, -1] = (4*u[l][:, 1]-u[l][:, 2])/3, (4*u[l][:, -2]-u[l][:, -3])/3 # du(0, y, t)/dx = 0 and du(L_X, y, t)/dx = 0
        else:
            u[l][0], u[l][-1] = u[l-1][0], u[l-1][-1] # u(x, 0, t) = u(x, 0, 0) and u(x, L_Y, t) = u(x, L_Y, 0)
            u[l][:, 0], u[l][:, -1] = (4*u[l][:, 1]-u[l][:, 2])/3, (4*u[l][:, -2]-u[l][:, -3])/3 # du(0, y, t)/dx = 0 and du(L_X, y, t)/dx = 0
    return (xv, yv, u)

def animateHeat(xv, yv, u, heat_options: HeatOptions):
    L_X, L_Y, T, FPS = heat_options.L_X, heat_options.L_Y, heat_options.T, heat_options.FPS
    a = [i[0] for i in np.array_split(u, int(np.floor(T*FPS)))] if len(u) > int(np.floor(T*FPS)) else u # Split u in order to skip frames
    FPS = FPS if len(u)!=len(a) else int(np.floor(len(u)/T)) # Recalibrate FPS
    def update_plot(i, plots):
        plots[0].remove()
        plots[0] = ax.plot_surface(xv, yv, a[i], cmap="hot")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', xlabel="x", ylabel="y", zlabel="T")
    ax.set_xlim(0, L_X)
    ax.set_ylim(0, L_Y)
    ax.set_zlim(float(1.2*np.min(u[0])), float(1.2*np.max(u[0])))
    plots = [ax.plot_surface(xv, yv, a[0])]
    ani = animation.FuncAnimation(fig, update_plot, fargs=(plots,), frames=len(a))
    f = f"/tmp/{time()}.gif"
    ani.save(f, fps=FPS)
    return f

def calcAnimUp(task_id: str, heat_options: HeatOptions):
    try:
        (xv, yv, u) = heatEquation(heat_options)
        filename = animateHeat(xv, yv, u, heat_options)
        link = uploadToUguu(filename)
    except:
        link = {"link": "error"}
    finally:
        postToDB(task_id, link)
