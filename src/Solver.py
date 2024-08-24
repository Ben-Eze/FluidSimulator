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
        self.fluid.diffuse_smoke()
        # self.fluid.convect_smoke()
        
        # self.fluid.diffuse_velocity()
        # self.fluid.convect_velocity()
    
    @staticmethod
    def diffuseEE_dx_is_dy(D, fluid_domain, nu, dx, dt, nit):
        """
        Diffuse scalar field D with the Explicit Euler scheme, diffusion 
        constant k
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

    # @staticmethod
    # def diffuseIE(D, fluid_domain, k):
    #     """
    #     Diffuse scalar field D with the Implicit Euler scheme, diffusion 
    #     constant k
    #     """
    #     return D
