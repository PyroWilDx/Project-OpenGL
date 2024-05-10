from Core import Shader, load
from Cylinder import Cylinder
from Animation import *
from Utils import *
from Transform import *
from Texture import *
from Particle import Particle
import random as rd


class Player(Node):
    def __init__(self, position, viewer):
        super().__init__(transform=translate(position))

        corps_shader = Shader("Cylinder.vert", "Cylinder.frag")
        self.corps = Node(transform=scale(0.1, 0.1, 0.1))
        self.corps.add(*load('models/Ovale.obj', corps_shader))

        self.helice = Helice(position=(0, -0.42, 0))

        self.add(self.corps)
        self.add(self.helice)

        self.position = vec(position)
        self.rotation_matrix = rotate(axis=(0, 0, 0), angle=0)

        self.face = vec(0, 0, 0)
        self.side = vec(0, 0, 0)
        self.foot = vec(0, 0, 0)

        self.trackball = None

        self.viewer = viewer

        smoke_wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                             GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        smoke_filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                               (GL.GL_LINEAR, GL.GL_LINEAR),
                               (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        smoke_wrap, smoke_filter = next(smoke_wraps), next(smoke_filters)
        self.smoke_tex_list = []
        self.smoke_frame_count = 40
        for i in range(1, self.smoke_frame_count + 1):
            self.smoke_tex_list.append(Texture(f"textures/smoke/Smoke_{i}.png",
                                               smoke_wrap, *smoke_filter))
        self.make_smoke = True

    def set_trackball(self, value):
        self.trackball = value

    def invert_make_smoke(self):
        self.make_smoke = not self.make_smoke

    def update_transform(self):
        self.transform = translate(self.position) @ self.rotation_matrix

    def move(self, win):
        moved = False

        speed_factor = min(self.trackball.zoom / 2, 10)
        speed = speed_factor * Utils.dt
        if glfw.get_key(win, glfw.KEY_C):
            speed *= 3.6

        if glfw.get_key(win, glfw.KEY_A):
            self.position -= self.side * speed
            moved = True
        if glfw.get_key(win, glfw.KEY_D):
            self.position += self.side * speed
            moved = True
        if glfw.get_key(win, glfw.KEY_W):
            self.position += self.face * speed
            moved = True
        if glfw.get_key(win, glfw.KEY_S):
            self.position -= self.face * speed
            moved = True
        if glfw.get_key(win, glfw.KEY_SPACE):
            self.position[2] += speed / 2
            moved = True
        elif glfw.get_key(win, glfw.KEY_LEFT_SHIFT):
            self.position[2] -= speed / 2
            moved = True

        if moved:
            self.helice.angle += 220 * Utils.dt
            self.rotate(self.trackball.yaw, self.trackball.pitch)
            self.update_transform()

            if self.make_smoke:
                # for _ in range(0, rd.randint(2, 10)):
                for _ in range(0, rd.randint(1, 1)):
                    smoke_position = self.position - 3.56 * self.face - 0.06 * self.side - 0.26 * self.foot
                    # itv = 0.6
                    # smoke_position[0] += rd.random() * itv - itv / 2
                    # smoke_position[1] += rd.random() * itv - itv / 2
                    # smoke_position[2] += rd.random() * itv - itv / 2
                    self.viewer.add(Particle(tex_file_name=None,
                                             tex_file_ext=None,
                                             frame_count=self.smoke_frame_count,
                                             frame_duration=0.06,
                                             position=smoke_position,
                                             scale_factor=1,
                                             velocity=(0, 0, 0.6),
                                             parent_node=self.viewer,
                                             trackball=self.trackball,
                                             loaded_tex_list=self.smoke_tex_list))

    def rotate(self, camera_yaw, camera_pitch):
        self.rotation_matrix = rotate(axis=(0, 0, 1), angle=-camera_yaw - 90)
        self.rotation_matrix @= rotate(axis=(1, 0, 0), angle=camera_pitch)
        self.update_transform()

    def update_face_side_foot(self, camera_yaw, camera_pitch):
        yaw_rad = np.radians(camera_yaw)
        pitch_rad = np.radians(camera_pitch)
        self.face = normalized(vec(np.cos(yaw_rad) * np.cos(pitch_rad),
                                   -np.sin(yaw_rad) * np.cos(pitch_rad),
                                   np.sin(pitch_rad)))
        self.side = normalized(np.cross(self.face, vec(0, 0, 1.0)))
        self.foot = normalized(np.cross(self.side, self.face))


class Helice(Node):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(transform=translate(position))
        self.position = position
        self.axis = (0, 1, 0)
        self.angle = 0

        helice_shader = Shader("Cylinder.vert", "Cylinder.frag")

        helice1_cl = Cylinder(helice_shader)
        helice2_cl = Cylinder(helice_shader)

        helice1 = Node(transform=scale(0.1, 0.1, 1))
        helice1.add(helice1_cl)
        helice2 = Node(transform=scale(1, 0.1, 0.1) @ rotate(axis=(0, 1, 0), angle=90.0))
        helice2.add(helice2_cl)

        self.add(helice1)
        self.add(helice2)

    def draw(self, model=identity(), **other_uniforms):
        super().draw(model=model, **other_uniforms)
        self.angle += 32 * Utils.dt
        self.transform = translate(self.position) @ rotate(self.axis, self.angle)
