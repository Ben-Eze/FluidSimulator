################################################################################
##
##  File: Display.py
##
##  The MIT License
##
##  Copyright (c) 2006 Division of Applied Mathematics, Brown University (USA),
##  Department of Aeronautics, Imperial College London (UK), and Scientific
##  Computing and Imaging Institute, University of Utah (USA).
##
##  Permission is hereby granted, free of charge, to any person obtaining a
##  copy of this software and associated documentation files (the "Software"),
##  to deal in the Software without restriction, including without limitation
##  the rights to use, copy, modify, merge, publish, distribute, sublicense,
##  and/or sell copies of the Software, and to permit persons to whom the
##  Software is furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included
##  in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
##  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
##  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
##  DEALINGS IN THE SOFTWARE.
##
##  Description:  Implements the Display object which handles visualising the 
##                fluid and recording
##
################################################################################


import ctypes
import numpy as np
import pygame as pg


class Display:
    def __init__(self, config):
        pg.init()
        ctypes.windll.user32.SetProcessDPIAware()   # sorts out screen bug
        
        max_w = config["display"]["max_width"]
        max_h = config["display"]["max_height"]
        self.dims = np.array([max_w, max_h])    # make more advanced

        self.window = pg.display.set_mode(self.dims)
        # particle_surf = pg.Surface(self.dims, pg.SRCALPHA, 32)    # implement later

        self.Nx = int(config["domain"]["width"] / config["domain"]["base_size"])
        self.Ny = int(config["domain"]["height"] / config["domain"]["base_size"])
        self.pxarray = np.zeros((self.Ny, self.Nx, 3))

        self.background_colour = (0, 0, 0)

    def __call__(self):
        self.window.fill(self.background_colour)
        pg.display.update()

    def blit_pxarray(self, pxarray, colourkey=None):
        surf = pg.surfarray.make_surface(pxarray.swapaxes(0, 1))
        surf = pg.transform.scale(surf, self.dims)

        if colourkey is not None:
            surf.set_colorkey(colourkey)
        
        self.window.blit(surf, (0, 0))

    # TODO: copy functions from graphics.py