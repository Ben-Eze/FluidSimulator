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
import warnings


# def convect(D, u, v, dx, dy, dt, IX, IY, domain):
#     """
#     Convect scalar field D in accordance with the velocity field (u, v)
#     """

#     # IX_prev, IY_prev are the (index) coordinates where we are convecting D 
#     # from
#     x = (IX - u * dt / dx)
#     y = (IY - v * dt / dy)

#     nx, ny = IX.shape()
#     x0 = np.clip(np.floor(x), 0, nx-1).astype(int)
#     y0 = np.clip(np.floor(y), 0, ny-1).astype(int)
#     x1 = np.clip(x0 + 1, 0, nx-1)
#     y1 = np.clip(y0 + 1, 0, ny-1)
#     frac_x = x%1
#     frac_y = y%1

#     D00 = D[y0, x0]
#     D01 = D[y0, x1]
#     D10 = D[y1, x0]
#     D11 = D[y1, x1]

#     D0f = (1-frac_x)*D00 + frac_x*D01
#     D1f = (1-frac_x)*D10 + frac_x*D11
#     Dff = D.copy()
#     Dff[domain] = ((1-frac_y)*D0f + frac_y*D1f)[domain]

#     return Dff

class Fluid:
    def __init__(self, spec, solver) -> None:
        fluid_spec = spec["fluid"]
        self.name = fluid_spec["name"] if fluid_spec["name"] is not None \
            else "unknown_fluid"
        self.solver = solver
    
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
        self.where_wall = np.where(self.walls)
        self.where_fluid = np.where(1 - self.walls)
        self.where_inner_fluid = np.where(1 - self.walls[1:-1, 1:-1])

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

        self.diffuse = None
        self.set_diffusion_solver()
        
        print(f"Fluid ({self.name}) initialised")
    
    def set_diffusion_solver(self):
        if (self.solver.solver_type == "ImplicitEuler" 
        and self.solver.dx_is_dy):
            warnings.warn("IE,dx==dy not yet implemented")
        
        elif (self.solver.solver_type == "ImplicitEuler" 
        and not self.solver.dx_is_dy):
            warnings.warn("IE,dx!=dy not yet implemented")

        elif (self.solver.solver_type == "ExplicitEuler" 
        and self.solver.dx_is_dy):
            self.diffuse = lambda D: self.solver.diffuseEE_dx_is_dy(
                D, self.where_inner_fluid, self.nu, self.dx, 
                self.solver.dt, self.solver.nit
            )

        elif (self.solver.solver_type == "ExplicitEuler" 
        and self.solver.dx_is_dy):
            warnings.warn("EE,dx!=dy not yet implemented")
        else:
            warnings.warn(f"Solver '{self.solver.solver_type}' not recognised")

    def diffuse_smoke(self):
        self.d[self.where_fluid] = self.diffuse(self.d)[self.where_fluid]
    
    # def convect_smoke(self):
    #     self.d[self.where_fluid] = convect(
    #         self.d, self.u, self.v, self.IX, self.IY, self.nx, self.ny
    #     )[self.where_fluid]
