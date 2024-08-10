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
    def __init__(self, config, solver):
        pg.init()
        ctypes.windll.user32.SetProcessDPIAware()   # sorts out screen bug
        
        max_w = config["display"]["max_width"]
        max_h = config["display"]["max_height"]
        self.dims = np.array([max_w, max_h])    # make more advanced

        self.window = pg.display.set_mode(self.dims, flags=pg.RESIZABLE)
        # particle_surf = pg.Surface(self.dims, pg.SRCALPHA, 32)    # implement later

        self.Nx = int(config["domain"]["width"] / config["domain"]["base_size"])
        self.Ny = int(config["domain"]["height"] / config["domain"]["base_size"])
        self.pxarray = np.zeros((self.Ny, self.Nx, 3), dtype=float)
        
        self.sf = None
        self.blit_offset = None
        self.domain_dims = None
        self.update_transformation()

        self.background_colour = (0, 0, 0)
        self.fluid_colour = (0, 0, 20)

        self.fluid = solver.fluid

    def __call__(self):
        self.window.fill(self.background_colour)
        self.update_pxarray()
        self.blit_pxarray()
        pg.display.update()
    
    def update_transformation(self, event=None):
        if event is not None:
            self.dims = np.array([event.__dict__["x"], event.__dict__["y"]])

        AR_px = self.pxarray.shape[1] / self.pxarray.shape[0]
        AR_wind = self.dims[0] / self.dims[1]

        self.sf = self.dims[0] / self.pxarray.shape[1] if AR_px > AR_wind \
             else self.dims[1] / self.pxarray.shape[0]
        
        self.domain_dims = np.array(self.pxarray.shape[1::-1])*self.sf
        
        self.blit_offset = (self.dims - self.domain_dims) / 2

    
    def update_pxarray(self):
        # in reality will be replaced with individual functions
        self.pxarray[..., 0] = self.fluid_colour[0]
        self.pxarray[..., 1] = self.fluid_colour[1]
        self.pxarray[..., 2] = self.fluid_colour[2]

        self.pxarray[..., 0] += 255 * self.fluid.d
        self.pxarray[..., 1] += 255 * self.fluid.d
        self.pxarray[..., 2] += 255 * self.fluid.d

        self.pxarray = np.clip(self.pxarray, 0, 255)


    def blit_pxarray(self, colourkey=None):
        surf = pg.surfarray.make_surface(self.pxarray.swapaxes(0, 1))
        surf = pg.transform.scale(surf, self.domain_dims.round())

        if colourkey is not None:
            surf.set_colorkey(colourkey)
        
        self.window.blit(surf, self.blit_offset)

    # TODO: copy functions from graphics.py