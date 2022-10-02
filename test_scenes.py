from tkinter import Scale
from typing import Tuple
import numpy as np
from manim import *
from manim.opengl import OpenGLSurface
from manim.utils.opengl import scale_matrix


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

    matrix = np.array([[4, -4,  -1],
                       [4,  12, -5],
                       [4,  5,   6]])
    vector = np.array([[-10],
                       [14],
                       [-15]])
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
                uv = (self.vector[row_index][0] + (-1*self.matrix[row_index][0])*u + (-1*self.matrix[row_index][1])*v)/self.matrix[row_index][2]
                point = np.array([u,    #x component
                                  v,    #y component
                                  uv if uv > uv_range[0] and uv < uv_range[1] else None])  #z component
                return point
            plane = OpenGLSurface(uv_func, color=colors[row_index], u_range=[-3, 1], v_range=[-1, 3])
            self.planes.append(plane)
        
        self.add(*self.planes)
        
        
        self.interactive_embed()

class GuassEliminationVectors(ThreeDScene):


    matrix = np.array([[4, -4,  -1],
                       [4,  12, -5],
                       [4,  5,   6]])
    vector = np.array([[-10],
                       [14],
                       [-15]])
    matrix_row_vectors = []

    def construct(self):
        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        self.begin_ambient_camera_rotation(.1)

        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN})
        self.add(axes)
        
        self.matrix_row_vectors = self._create_vector_mobjects(self.matrix)
        self.add(*self.matrix_row_vectors)
        
        self.wait(2)

        self._scale_matrix_row(0.25, 0)
        # self.play(self.matrix_row_vectors[0].animate.apply_matrix(2, about_point=[0,0,0]))
        self._pivot_matrix_row(0, 1)
        self.interactive_embed()

    def _create_vector_mobjects(self, matrix):
        vectors = []
        colors = (BLUE, RED, GREEN)
        for row_index in range(matrix.shape[0]):
            vector = Arrow3D(start=[0,0,0], end=matrix[row_index], color=colors[row_index])
            vectors.append(vector)
        return vectors

    def _scale_matrix_row(self, scale_factor, row_number):
        self.matrix[row_number] = self.matrix[row_number] * scale_factor

        scale_matrix = np.identity(3) * scale_factor 
        self.play(self.matrix_row_vectors[row_number].animate.apply_matrix(scale_matrix))

    def _pivot_matrix_row(self, base_rowcoloumn: int, target_row_number: int):
        new_row_vector = self.matrix[target_row_number] + (-1*self.matrix[target_row_number][base_rowcoloumn])

        pivot_matrix = np.identity(3)
        pivot_matrix[0][0] = new_row_vector[0]/self.matrix[target_row_number][0]
        pivot_matrix[1][1] = new_row_vector[1]/self.matrix[target_row_number][1]
        pivot_matrix[2][2] = new_row_vector[2]/self.matrix[target_row_number][2]

        self.matrix[target_row_number] = new_row_vector

        self.play(self.matrix_row_vectors[target_row_number].animate.apply_matrix(pivot_matrix))
