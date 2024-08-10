################################################################################
##
##  File: Fluid.py
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
##  Description:  Implements the Fluid class, which contains parameters for the 
##                fluid (eg. velocity, density)
##
################################################################################


import numpy as np


class Fluid:
    def __init__(self, spec) -> None:
        fluid_spec = spec["fluid"]
        self.name = fluid_spec["name"] if fluid_spec["name"] is not None \
            else "unknown_fluid"
    
        # Domain
        self.x_max = spec["domain"]["width"]
        self.y_max = spec["domain"]["height"]
        self.base_size = spec["domain"]["base_size"]

        self.Nx = int(np.ceil(self.x_max / self.base_size))
        self.Ny = int(np.ceil(self.y_max / self.base_size))
        self.IX, self.IY = np.meshgrid(np.arange(self.Nx), np.arange(self.Ny))

        self.x_lin = np.linspace(0, self.x_max, self.Nx, endpoint=False)
        self.y_lin = np.linspace(0, self.y_max, self.Ny, endpoint=False)
        self.X, self.Y = np.meshgrid(self.x_lin, self.y_lin)

        self.dx = self.x_max / self.Nx
        self.dy = self.y_max / self.Ny

        self.walls = np.zeros((self.Ny, self.Nx))

        # Initial conditions
        self.u = np.zeros((self.Ny, self.Nx))
        self.U = np.zeros((self.Ny, self.Nx))

        self.v = np.zeros((self.Ny, self.Nx))
        self.V = np.zeros((self.Ny, self.Nx))

        self.p = np.zeros((self.Ny, self.Nx))

        self.d = np.zeros((self.Ny, self.Nx))
        
        # Properties
        self.rho = fluid_spec["density"]
        self.nu = fluid_spec["viscosity"]
        
        print(f"Fluid ({self.name}) initialised")
