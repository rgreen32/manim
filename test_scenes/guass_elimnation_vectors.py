from manim import *
from manim.opengl import OpenGLSurface
from typing import Tuple
from observable_matrix import ObservableMatrix


class GuassEliminationVectors(ThreeDScene):
    vector = np.array([[-10],
                       [ 14],
                       [-15]])

    matrix_row_vectors = []

    rotation_matrix_Y = [[np.cos(np.pi/2), 0, np.sin(np.pi/2)],
                        [0, 1, np.sin(np.pi/2)],
                        [-np.sin(np.pi/2), 0, np.cos(np.pi/2)]]

    def construct(self):
        self.matrix = ObservableMatrix(np.array([[1, 1,  1],
                                                 [1,  -1, 1],
                                                 [-1,  -1, -1]]), self._update_row_vectors)

        self.renderer.camera.light_source.move_to(3*UP) # changes the source of the light
        self.set_camera_orientation(phi=75 * DEGREES, theta=40 * DEGREES, center_point=[1.0, 1.0, 1.0])
        # self.begin_ambient_camera_rotation(.1)

        axes = ThreeDAxes(x_axis_config={"color": BLUE}, y_axis_config={"color": RED}, z_axis_config={"color": GREEN}) #Axis tick markers are inaccurate
        self.add(axes)
        
        self.matrix_row_vectors = self._create_vector_mobjects(self.matrix)
        self.add(*self.matrix_row_vectors)

        matrix_string = MarkupText(str(self.matrix))
        matrix_string.angle = np.pi/2
        matrix_string.rotate(np.pi/2, [1,0,0])
        # def tesd(m, dt):
        #     rate=0.2
        #     x = rate*dt
        #     matrix_string.angle += x
        #     # 
        #     tes = self.camera.get_position()
        #     tes2 = tes - 1.5
        #     print(tes2)
        #     matrix_string.move_to(tes2)
        # matrix_string.add_updater(tesd)
        self.add(matrix_string)

        # self.wait(2)
        # matrix_string.move_to([1,1,1])

        self.interactive_embed()

    def _create_vector_mobjects(self, matrix):
        vectors = []
        colors = (BLUE, RED, GREEN)
        for row_index in range(matrix.shape[0]):
            # vector = Arrow3D(start=[0,0,0], end=matrix[row_index], color=colors[row_index])
            vector = Line3D(start=[0,0,0], end=matrix[row_index], color=colors[row_index])
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
        for row_index in range(self.matrix.shape[0]): #get rid of this for-loop
            old_row_vector = self.matrix.prev_matrix[row_index].copy()
            update_matrix = np.identity(3)
            update_matrix[0][0] = self.matrix[row_index][0]/old_row_vector[0]
            update_matrix[1][1] = self.matrix[row_index][1]/old_row_vector[1]
            update_matrix[2][2] = self.matrix[row_index][2]/old_row_vector[2]
            animations.append(ApplyMatrix(update_matrix, self.matrix_row_vectors[row_index], about_point=[0,0,0]))
        self.play(*animations)
