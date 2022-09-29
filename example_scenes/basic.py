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
    def construct(self):
        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN})
        def plane1_uvfunc(u, v):
            uv = (-10 - 4*u + 4*v)/-1
            point = np.array([u, v, uv if uv < 0 and uv > -3 else None])
            return point
        plane1 = OpenGLSurface(plane1_uvfunc, color=BLUE, u_range=[-3, 1], v_range=[-1, 3])

        def plane2_uvfunc(u, v):
            uv = (14 - 4*u - 12*v)/-5
            point = np.array([u, v, uv if uv < 0 and uv > -3 else None])
            return point
        plane2 = OpenGLSurface(plane2_uvfunc, color=GREEN, u_range=[-3, 1], v_range=[-1, 3])

        def plane3_uvfunc(u, v):
            uv = (-15 - 4*u - 5*v)/6
            point = np.array([u, v, uv if uv < 0 and uv > -3 else None])
            return point
        plane3 = OpenGLSurface(plane3_uvfunc, color=RED, u_range=[-3, 1], v_range=[-1, 3])
        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        self.add(axes, plane1, plane2, plane3)
        self.begin_ambient_camera_rotation(.1)
        self.wait(1)
        # self.play(plane1.animate.apply_matrix(self.rotation_matrix_Y))
        # self.wait(1)
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
