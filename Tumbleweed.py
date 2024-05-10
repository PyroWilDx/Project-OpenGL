from Core import *
import random as rd


class Tumbleweed(Node):
    @staticmethod
    def generate(x, y0, y1, z, parent):
        y = rd.randint(y0, y1)
        scale_factor = rd.random() * 0.2 + 0.26
        tumbleweed = Tumbleweed(position=(x, y, z),
                                scale_factor=scale_factor,
                                rotation_factor=180,
                                living_time=10,
                                parent=parent)
        return tumbleweed

    def __init__(self, position, scale_factor, rotation_factor, living_time, parent):
        super().__init__(transform=translate(position) @ scale(scale_factor, scale_factor, scale_factor))

        tumbleweed = load(file='models/Sphere.obj',
                          shader=Shader("Textured.vert", "Textured.frag"),
                          tex_file="textures/Tumbleweed.png",
                          delete_tex=False,
                          do_print=False)

        self.living_time = living_time
        self.t = glfw.get_time()

        self.parent = parent

        translate_keys = {self.t: vec(0, 0, 0),
                          self.t + living_time: vec(0, 6 * living_time, 0)}
        axis = (1, 0, 0)
        rotate_keys = {}
        for i in range(0, living_time + 1):
            rotate_keys[self.t + i] = quaternion_from_axis_angle(axis, -i * rotation_factor)
        scale_keys = {self.t: 1,
                      self.t + living_time - 0.42: 1,
                      self.t + living_time: 0}
        keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
        keynode.add(*tumbleweed)

        self.add(keynode)

    def draw(self, model=identity(), **other_uniforms):
        if glfw.get_time() - self.t > self.living_time:
            self.parent.remove(self)
            return
        super().draw(model, **other_uniforms)
