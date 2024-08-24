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
        self.fluid = Fluid(spec)
        self.log = Log(spec["log"])
        self.display = Display(spec, self)
        self.gui = GUI(self)
        self.name_string = f"({self.name}) " if self.name is not None else ""
        self.mainloop = Mainloop(self)
        
        self.log(f"Solver {self.name_string}initialised")
    
    def __del__(self):
        # self.log(f"Solver {self.name_string}finished with exit code 0")
        pass
    
    def run(self):
        self.log(f"Solver {self.name_string}running...")
        self.mainloop()
    
    def solve(self):
        self.fluid.diffuse_smoke(k=1, nit=5)
        # self.fluid.diffuse_velocity()
        # self.fluid.convect_smoke()
        # self.fluid.convect_velocity()
