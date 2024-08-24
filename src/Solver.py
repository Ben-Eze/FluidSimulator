################################################################################
##
##  File: Solver.py
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
##  Description:  Implements the Solver class, which contains the Fluid, 
##
################################################################################


import warnings
import numpy as np

from assets.solver_config import spec
from src.Log import Log
from src.Display import Display
from src.Fluid import Fluid
from src.Mainloop import Mainloop
from src.GUI import GUI


class Solver:
    def __init__(self) -> None:
        self.name = spec["name"]
        
        self.solver_type = spec["scheme"]["name"]
        self.dx_is_dy = spec["scheme"]["dx==dy"]
        self.nit = spec["scheme"]["nit"]
        self.dt = spec["time"]["dt"]
        self.fluid = Fluid(spec, self)
        
        self.log = Log(spec["log"])
        
        self.display = Display(spec, self)
        
        self.gui = GUI(self)
        
        self.mainloop = Mainloop(self)
        
        self.name_string = f"({self.name}) " if self.name is not None else ""
        self.log(f"Solver {self.name_string}initialised")
    
    def __del__(self):
        # self.log(f"Solver {self.name_string}finished with exit code 0")
        pass
    
    def run(self):
        self.log(f"Solver {self.name_string}running...")
        self.mainloop()
    
    def solve(self):
        self.fluid.diffuse_velocity()
        # self.fluid.enforce_continuity()
        # self.fluid.advect_velocity()
        # self.fluid.enforce_continuity()
        # self.fluid.velocity_BCs()

        self.fluid.diffuse_smoke()
        self.fluid.advect_smoke()
    
    @staticmethod
    def diffuseEE_dx_is_dy(D, fluid_domain, nu, dx, dt, nit):
        """
        Diffuse the scalar field D with the Explicit Euler scheme
        Assumption: dx = dt
        """

        k = 4 * nu * dt / dx**2
        D_new = np.copy(D)

        # iteratively progress D to satisfy the equation 
        for _ in range(nit):
            D_new[1:-1, 1:-1][fluid_domain] = (
                (D[1:-1, 1:-1][fluid_domain] 
                + 0.25*k*(D_new[2:, 1:-1][fluid_domain] 
                        + D_new[:-2, 1:-1][fluid_domain] 
                        + D_new[1:-1, 2:][fluid_domain] 
                        + D_new[1:-1, :-2][fluid_domain])) 
                / (1 + k))
        return D_new

    @staticmethod
    def diffuseIE_dx_is_dy(D, nu, dx, dt):
        """
        Diffuse the scalar field D with the Explicit Euler scheme
        Assumption: dx = dt
        """
        k = 4 * nu * dt / dx**2
        M = (D[2:, 1:-1] + D[:-2, 1:-1] + D[1:-1, 2:] + D[1:-1, :-2]) / 4

        D[1:-1, 1:-1] = D[1:-1, 1:-1] * (1 - k) + k * M

        return D

    @staticmethod
    def advect(D, fluid_domain, u, v, dx, dy, IX, IY, dt):
        """
        Advect scalar field D in accordance with the velocity field (u, v)
        """

        # IX_prev, IY_prev are the (index) coordinates where we are advecting 
        # D from
        IX_prev = (IX - u * dt / dx)
        IY_prev = (IY - v * dt / dy)

        ny, nx = IX.shape
        x0 = np.clip(np.floor(IX_prev), 0, nx-1).astype(int)
        y0 = np.clip(np.floor(IY_prev), 0, ny-1).astype(int)
        x1 = np.clip(x0 + 1, 0, nx-1)
        y1 = np.clip(y0 + 1, 0, ny-1)
        frac_x = IX_prev%1
        frac_y = IY_prev%1

        D00 = D[y0, x0]
        D01 = D[y0, x1]
        D10 = D[y1, x0]
        D11 = D[y1, x1]

        D0f = (1-frac_x)*D00 + frac_x*D01
        D1f = (1-frac_x)*D10 + frac_x*D11
        Dff = D.copy()
        Dff[fluid_domain] = ((1-frac_y)*D0f + frac_y*D1f)[fluid_domain]

        return Dff
    
    @staticmethod
    def div(v_x, v_y):
        # what there should be a dx, dy term...?
        return .5 * (v_x[1:-1, 2:] - v_x[1:-1, :-2] + v_y[2:, 1:-1] - v_y[:-2, 1:-1])

    @staticmethod
    def extract_divfree(u, v, f, dx, dy, nit, where_inner_fluid):
        div_v = Solver.div(u, v)

        for it in range(nit):
            f[1:-1, 1:-1] = (  (f[1:-1, 2:] + f[1:-1, :-2]) * dy**2
                            + (f[2:, 1:-1] + f[:-2, 1:-1]) * dx**2
                            - div_v) / 2 / (dy**2 + dx**2)
        
        u_cf = .5 * (f[1:-1, 2:] - f[1:-1, :-2])
        v_cf = .5 * (f[2:, 1:-1] - f[:-2, 1:-1])

        u_df = u.copy()
        v_df = v.copy()
        u_df[1:-1, 1:-1][where_inner_fluid] -= u_cf[where_inner_fluid]
        v_df[1:-1, 1:-1][where_inner_fluid] -= v_cf[where_inner_fluid]

        return f, u_df, v_df