################################################################################
##
##  File: gui.py
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
##  Description:  This file contains helper functions for a range of purposes,
##                from receiving mouse and keyboard input to displaying pixel
##                values
##
################################################################################


import numpy as np
import pygame as pg


class GUI:
    def __init__(self, solver):
        self.mouse = Mouse()
        self.solver = solver
        self.fluid = solver.fluid
        self.display = solver.display
    
    def __call__(self, events):
        self.mouse.init(events)
        self.fluid_interaction()

    def fluid_interaction(self):
        if self.mouse.state == 2:
            self.mouse.pos_prev = self.mouse.pos.copy()

        if self.mouse.press:
            for mouse_pos in self.mouse.pos_stack:
                mouse_index = (
                    (mouse_pos - self.display.blit_offset)/self.display.sf
                )[::-1].astype(int)
                
                if (0 <= mouse_index[1] < self.fluid.Nx
                    and 0 <= mouse_index[0] < self.fluid.Ny
                    and not self.fluid.walls[mouse_index[0], mouse_index[1]]
                ):
                    # TODO: toggle velocity and smoke interaction (ie should be 
                    # able to do one without the other)
                    velocity = (self.mouse.pos - self.mouse.pos_prev) / self.solver.dt
                    # dividing by pos_stack ensures constant smoke addition per 
                    # time step
                    # dividing by base_size^2 ensures constant smoke addition 
                    # per unit area
                    self.fluid.d[mouse_index[0], mouse_index[1]] += (
                        0.1/len(self.mouse.pos_stack)/(self.fluid.base_size**2)
                    )

                    # the velocity field is also affected by dragging the mouse
                    self.fluid.u[mouse_index[0], mouse_index[1]] = velocity[0]
                    self.fluid.v[mouse_index[0], mouse_index[1]] = velocity[1]


class Mouse:
    def __init__(self):
        self.pos = None
        self.pos_prev = None
        self.pos_stack = []
        self.press = 0

        self.state = 0
        #  0: not pressed
        # -1: just unpressed
        #  1: held down
        #  2: just pressed
    
    def init(self, events):
        self.get_state()
        self.get_pos_stack(events)
        self.get_pos()

    def get_state(self):
        self.press = pg.mouse.get_pressed()[0]
        if self.press:
            if self.state == 2:
                self.state = 1
            elif self.state != 1:
                self.state = 2
        else:
            if self.state == -1:
                self.state = 0
            elif self.state != 0:
                self.state = -1

    def get_pos(self, array=True):
        if self.pos is not None:
            self.pos_prev = self.pos.copy()

        self.pos = np.array(pg.mouse.get_pos(), dtype=float) if array \
                       else pg.mouse.get_pos()
    
    def get_pos_stack(self, events, array=True):
        self.pos_stack = []

        for event in events:
            if event.type == pg.MOUSEMOTION:
                pos = event.__dict__["pos"]
                self.pos_stack.append(np.array(pos) if array else pos)
                
        if not self.pos_stack:  # if not moving
            pos = pg.mouse.get_pos()
            self.pos_stack.append(np.array(pos) if array else pos)