from tkinter import SEL, Scale
from typing import Tuple
import numpy as np
from xcffib import NONE
from manim import *
from manim.opengl import OpenGLSurface
from ndarray_listener import ndl


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


class ObservableMatrix(np.ndarray):
    def __new__(self, input_array, onupdate_func = None):
        self.onupdate_func = onupdate_func
        return np.asarray(input_array).view(self)

    def __getitem__(self, key):
        self.prev_matrix = self.copy()
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if self.onupdate_func:
            self.onupdate_func()
        return None
        
class GuassEliminationVectors(ThreeDScene):
    vector = np.array([[-10],
                       [ 14],
                       [-15]])

    matrix_row_vectors = []

    rotation_matrix_Y = [[np.cos(np.pi/2), 0, np.sin(np.pi/2)],
                        [0, 1, np.sin(np.pi/2)],
                        [-np.sin(np.pi/2), 0, np.cos(np.pi/2)]]

    def construct(self):
        self.matrix = ObservableMatrix(np.array([[4.0, -4.0,  -1.0],
                                                 [4.0,  12.0, -5.0],
                                                 [4.0,  5.0,   6.0]]), self._update_row_vectors)

        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        self.begin_ambient_camera_rotation(.1)

        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN})
        self.add(axes)
        
        self.matrix_row_vectors = self._create_vector_mobjects(self.matrix)
        self.add(*self.matrix_row_vectors)

        matrix_string = MarkupText(str(self.matrix))
        self.add(matrix_string)
        
        self.wait(2)

        # self.prev_matrix = self.matrix.copy()
        self.matrix[0][0] = 1e-8

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

    def _update_row_vectors(self):
        animations = []
        for row_index in range(self.matrix.shape[0]):
            old_row_vector = self.matrix.prev_matrix[row_index]
            update_matrix = np.identity(3)
            update_matrix[0][0] = self.matrix[row_index][0]/old_row_vector[0]
            update_matrix[1][1] = self.matrix[row_index][1]/old_row_vector[1]
            update_matrix[2][2] = self.matrix[row_index][2]/old_row_vector[2]
            animations.append(ApplyMatrix(update_matrix, self.matrix_row_vectors[row_index]))
        self.play(*animations)
