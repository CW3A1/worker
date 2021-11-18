from os import remove

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from requests import post
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from modules.gen import *
from modules.classes import HeatOptions

def heatEquation(heat_options: HeatOptions):
    # Free constants
    L_X = heat_options.L_X
    L_Y = heat_options.L_Y # Length of plate
    DX = DY = H = heat_options.H # Step size
    ALPHA = heat_options.ALPHA # Thermal diffusivity in mm2/s
    T = heat_options.T # Total time in seconds
    FPS = heat_options.FPS # Frames per second
    BOUNDARY_CONDITION = heat_options.BOUNDARY_CONDITION # NO_FLUX or CONSTANT_Y

    # Dependent constants
    DT = 0.5/(ALPHA*(10**(-6))/DX**2+1/DY**2) # Von Neumann stability condition
    T_L = int(np.floor(T/DT)) # Amount of discrete time intervals

    # Create meshgrid
    xv, yv = np.mgrid[0:L_X:DX, 0:L_Y:DY]
    xv, yv = xv.T, yv.T

    # Construct multidimensional array to store meshgrid data over time and set initial condition
    u = np.zeros((T_L, len(xv), len(xv[0])))
    u[0] = np.exp(-yv)+xv

    # Calculate meshgrid data over time progressively
    for l in range(1, T_L):
        u[l] = u[l-1] + (np.roll(u[l-1], -1, 0) + np.roll(u[l-1], 1, 0) + np.roll(u[l-1], -1, 1) + np.roll(u[l-1], 1, 1) - 4*u[l-1])*ALPHA*(10**(-6))*DT/H**2 # forward Euler method
        if BOUNDARY_CONDITION == "NO_FLUX":
            u[l][0], u[l][-1] = (4*u[l][1]-u[l][2])/3, (4*u[l][-2]-u[l][-3])/3 # du/dy = 0
            u[l] = u[l].T
            u[l][0], u[l][-1] = (4*u[l][1]-u[l][2])/3, (4*u[l][-2]-u[l][-3])/3 # dx/dy = 0
            u[l] = u[l].T
        else:
            u[l][0], u[l][-1] = u[l-1][0], u[l-1][-1] # Boundary conditions: u(x, 0, t) = u(x, 0, 0) and u(x, L_Y, t) = u(x, L_Y, 0)
            u[l] = u[l].T
            u[l][0], u[l][-1] = (4*u[l][1]-u[l][2])/3, (4*u[l][-2]-u[l][-3])/3 # dx/dy = 0
            u[l] = u[l].T
    animateHeat(xv, yv, u, T, FPS)
    return upload()

def animateHeat(xv, yv, u, T, FPS):
    # Animate heat diffusion
    a = [i[0] for i in np.array_split(u, int(np.floor(T*FPS)))] if len(u) > int(np.floor(T*FPS)) else u # Split u in order to skip frames
    FPS = FPS if len(u)!=len(a) else int(np.floor(len(u)/T)) # Recalibrate FPS
    def update_plot(i, plots):
        plots[0].remove()
        plots[0] = ax.plot_surface(xv, yv, a[i], cmap="hot")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', xlabel="y-as", ylabel="x-as", zlabel="T")
    ax.set_zlim(float(1.2*np.min(u[0])), float(1.2*np.max(u[0])))
    plots = [ax.plot_surface(xv, yv, a[0])]
    ani = animation.FuncAnimation(fig, update_plot, fargs=(plots,), frames=len(a))
    ani.save("diffusion2D.gif", fps=FPS)

def upload():
    # Upload to Catbox.moe
    filename = "diffusion2D.gif"
    file_host_url = "https://catbox.moe/user/api.php"
    file = open(filename, 'rb')
    try:
        data = {
                'reqtype': 'fileupload',
                'userhash': '',
                'fileToUpload': (file.name, file, "image/gif")
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        r = post(file_host_url, data=monitor, headers={'Content-Type': monitor.content_type})
        r = {"link": r.text}
    except:
        r = {"link": "error"}
    finally:
        file.close()
    remove("diffusion2D.gif")
    return r
