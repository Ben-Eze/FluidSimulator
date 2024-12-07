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
    def __init__(self, gui_spec, solver):
        self.mouse = Mouse()
        self.solver = solver
        self.fluid = solver.fluid
        self.display = solver.display

        self.smoke_strength = gui_spec["smoke_strength"]
        self.brush_size = gui_spec["brush_size"]
        self.origin_brush = None
        self.set_origin_brush()
    
    def __call__(self, events):
        self.mouse.init(events)
        self.fluid_interaction()
    
    def set_origin_brush(self):
        rad = int(self.brush_size / self.display.sf)
        linspace = np.arange(-rad, rad) + 0.5
        X, Y = np.meshgrid(linspace, linspace)
        in_brush = X*X + Y*Y <= rad**2
        origin_brush = np.where(in_brush)
        self.origin_brush = origin_brush[0] - rad, origin_brush[1] - rad
    
    def move_brush(self, pos):
        brush = self.origin_brush[0] + pos[0], self.origin_brush[1] + pos[1]
        where_in = np.where(
            (0 <= brush[0]) & (brush[0] < self.fluid.Ny) 
          & (0 <= brush[1]) & (brush[1] < self.fluid.Nx)
        )
        return brush[0][where_in], brush[1][where_in]

    def fluid_interaction(self):
        # if self.mouse.state == 2:
        #     self.mouse.pos_prev = self.mouse.pos.copy()

        if self.mouse.l_press or self.mouse.r_press:
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
                    delta_pos = self.mouse.pos - self.mouse.pos_prev
                    brush_pos = self.move_brush(mouse_index)
                    
                    self.add_smoke(brush_pos)
                    self.push_fluid(brush_pos, delta_pos)

                    
    def add_smoke(self, brush_pos):
        # dividing by pos_stack ensures constant smoke addition per 
        # time step
        # dividing by base_size^2 ensures constant smoke addition 
        # per unit area
        if self.mouse.l_press:
            self.fluid.d[brush_pos] += (self.smoke_strength/
                        (len(self.mouse.pos_stack) * self.fluid.base_size**2))
    
    def push_fluid(self, brush_pos, delta_pos):
        self.fluid.u[brush_pos] = (delta_pos[0] * self.fluid.dx 
                                 / self.solver.dt)
        self.fluid.v[brush_pos] = (delta_pos[1] * self.fluid.dy 
                                 / self.solver.dt)


class Mouse:
    def __init__(self):
        self.pos = None
        self.pos_prev = None
        self.pos_stack = []
        self.l_press = 0
        self.mid_press = 0
        self.r_press = 0

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
        self.l_press, self.mid_press, self.r_press = pg.mouse.get_pressed()
        if self.l_press:
            if self.state == 2:
                self.state = 1
            elif self.state != 1:
                self.state = 2
        else:
            if self.state == -1:
                self.state = 0
            elif self.state != 0:
                self.state = -1

    def get_pos(self):
        if self.pos is not None:
            self.pos_prev = self.pos.copy()

        self.pos = np.array(pg.mouse.get_pos(), dtype=float)
    
    def get_pos_stack(self, events):
        self.pos_stack = []

        for event in events:
            if event.type == pg.MOUSEMOTION:
                pos = event.__dict__["pos"]
                self.pos_stack.append(np.array(pos))
                
        if not self.pos_stack:  # if not moving
            pos = pg.mouse.get_pos()
            self.pos_stack.append(np.array(pos))