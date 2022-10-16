from manim import *
from manim.opengl import OpenGLSurface
from observable_matrix import ObservableMatrix
from typing import Tuple

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

    matrix_row_planes = []

    def construct(self):
        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        # self.begin_ambient_camera_rotation(.1)

        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN})
        self.add(axes)
        self.matrix = ObservableMatrix(np.array([[4.0, -4.0,  -1.0, -10.0],
                                                 [4.0,  12.0, -5.0, 14.0],
                                                 [4.0,  5.0,   6.0, -15.0]]), self._on_update)

        def uv_func2(u, v):
            point = np.array([u,    #x component
                              v,    #y component
                              0 if (u > 1.1 or u < -1.1) or (v > 1.1 or v < -1.1) else None])  #z component
            return point
        plane = OpenGLSurface(uv_func2, color=PURPLE, u_range=[-1.2, 1.2], v_range=[-1.2, 1.2])
        self.add(plane)

        colors = (BLUE, RED, GREEN)
        uv_range = (-3, 0)
        for row_index in range(self.matrix.shape[0]):
            def uv_func(u, v):
                uv = (self.matrix[row_index][3] + (-1*self.matrix[row_index][0])*u + (-1*self.matrix[row_index][1])*v)/self.matrix[row_index][2]
                point = np.array([u,    #x component
                                  v,    #y component
                                  uv])  #z component
                return point
            plane = OpenGLSurface(uv_func, color=colors[row_index], u_range=[-1, 1], v_range=[-1, 1])
            self.matrix_row_planes.append(plane)
        self.add(*self.matrix_row_planes)

        self.matrix_string = MarkupText(str(self.matrix))
        self.matrix_string.rotate(np.pi/2, [1,0,0])
        # self.add(self.matrix_string)

        # self._scale_matrix_row(0.25, 0)
        # print(self.matrix)
        # print("==================")
        # self.wait(2)
        # self._pivot_matrix_row((0,0), 1)
        # print(self.matrix)
        # print("==================")
        # self.wait(2)
        # self._pivot_matrix_row((0,0), 2)
        # print(self.matrix)
        # print("==================")

        # self._scale_matrix_row((1.0/16.0), 1)
        # print(self.matrix)
        # print("==================")
        # self.wait(2)
        # self._pivot_matrix_row((1,1), 0)
        # print(self.matrix)
        # print("==================")
        # self.wait(2)
        # self._pivot_matrix_row(0, 2)
        # print(self.matrix)
        # print("==================")
        self.interactive_embed()

    def _scale_matrix_row(self, scale_factor, row_number):
        self.matrix[row_number] = self.matrix[row_number] * scale_factor
        # scale_matrix = np.identity(3) * scale_factor 
        # self.play(self.matrix_row_planes[row_number].animate.apply_matrix(scale_matrix))

    def _pivot_matrix_row(self, base_rowcoloumn: Tuple[int, int], target_row_number: int):
        new_row_vector = self.matrix[target_row_number] + (self.matrix[base_rowcoloumn[0]] * (-1*self.matrix[target_row_number][base_rowcoloumn[1]]))
        self.matrix[target_row_number] = new_row_vector
        # pivot_matrix = np.identity(3)
        # pivot_matrix[0][0] = new_row_vector[0]/self.matrix[target_row_number][0]
        # pivot_matrix[1][1] = new_row_vector[1]/self.matrix[target_row_number][1]
        # pivot_matrix[2][2] = new_row_vector[2]/self.matrix[target_row_number][2]
        # self.matrix[target_row_number] = new_row_vector
        # self.play(ApplyMatrix(pivot_matrix), self.matrix_row_planes[target_row_number], about_point=[0,0,0])
        # self.play(self.matrix_row_planes[target_row_number].animate.apply_matrix(pivot_matrix))

    def _on_update(self):
        self._update_matrix_string()
        self._update_row_planes()


    def _update_row_planes(self):   #animating planes on pivot operation fails?
        self.remove(*self.matrix_row_planes)
        colors = (BLUE, RED, GREEN)
        for row_index in range(self.matrix.shape[0]):
            def uv_func(u, v):
                uv = (self.matrix[row_index][3] + (-1*self.matrix[row_index][0])*u + (-1*self.matrix[row_index][1])*v)/self.matrix[row_index][2]
                point = np.array([u,    #x component
                                  v,    #y component
                                  uv])  #z component
                return point
            plane = OpenGLSurface(uv_func, color=colors[row_index], u_range=[-1, 1], v_range=[-1, 1])
            self.matrix_row_planes.append(plane)
        self.add(*self.matrix_row_planes)

    def _update_matrix_string(self):
        self.remove(self.matrix_string)
        self.matrix_string = MarkupText(str(self.matrix))
        self.matrix_string.rotate(np.pi/2, [1,0,0])
        self.add(self.matrix_string)
