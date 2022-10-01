#!/usr/bin/env python
import numpy as np
from manim import *
from manim.opengl import OpenGLSurface


class GuassElimination(ThreeDScene):
    rotation_matrix_X = [[1, 0, 0],
                        [0, np.cos(np.pi/2), np.sin(np.pi/2)],
                        [0, -np.sin(np.pi/2), np.cos(np.pi/2)]]

    rotation_matrix_Y = [[np.cos(np.pi/2), 0, np.sin(np.pi/2)],
                        [0, 1, np.sin(np.pi/2)],
                        [-np.sin(np.pi/2), 0, np.cos(np.pi/2)]]

    rotation_matrix_Z = [[np.cos(np.pi/2), -np.sin(np.pi/2), 0],
                        [np.sin(np.pi/2), np.cos(np.pi/2), 0],
                        [0, 0, 1]]    

    matrix = np.array([[4, -4,  -1, -10],
                       [4,  12, -5,  14],
                       [4,  5,   6,  -15]])
    planes = []

    def construct(self):
        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        self.begin_ambient_camera_rotation(.1)

        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN})
        self.add(axes)

        colors = (BLUE, RED, GREEN)
        uv_range = (-3, 0)
        for row_index in range(self.matrix.shape[0]):
            def uv_func(u, v):
                uv = (self.matrix[row_index][3] + (-1*self.matrix[row_index][0])*u + (-1*self.matrix[row_index][1])*v)/self.matrix[row_index][2]
                point = np.array([u,    #x component
                                  v,    #y component
                                  uv if uv > uv_range[0] and uv < uv_range[1] else None])  #z component
                return point
            plane = OpenGLSurface(uv_func, color=colors[row_index], u_range=[-3, 1], v_range=[-1, 3])
            self.planes.append(plane)
        
        self.add(*self.planes)
        
        
        self.interactive_embed()


class Test(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-20 * DEGREES)

        axes = ThreeDAxes(                                                
                x_range=[0, 3, 1],
                y_range=[0, 3, 1],
                z_range=[-1, 1, 1] 
            )                  
        axes.fill_shader_wrapper.depth_test = True
        axes.stroke_shader_wrapper.depth_test = True
        def func(x, y):
            return np.cos(x) * np.sin(y)

        surface = axes.plot_surface(    
            function=func,          
            u_range = (0, 3),       
            v_range = (0, 3),                                
            colorscale = ['#482173', '#2e6f8e', '#29af7f', '#bddf26']
        )                                                            

        self.add(axes, surface)
        self.interactive_embed()

class Example(Scene):
    def construct(self):
        # any mobject works
        text = Text('blah', color=BLUE)
        self.add(text)
        text.shift(UP)
        # self.interactive_embed()
