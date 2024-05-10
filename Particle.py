from Core import *
from Utils import *
from Texture import TexturedPlane


class Particle(Node):
    def __init__(self, tex_file_name, tex_file_ext,
                 frame_count, frame_duration,
                 position, scale_factor, velocity,
                 parent_node, trackball,
                 loaded_tex_list=None):
        super().__init__(transform=translate(position))
        self.static_particle = StaticParticle(tex_file_name=tex_file_name,
                                              tex_file_ext=tex_file_ext,
                                              frame_count=frame_count,
                                              frame_duration=frame_duration,
                                              scale_factor=scale_factor,
                                              loaded_tex_list=loaded_tex_list)
        self.add(self.static_particle)

        self.position = vec(position)
        self.velocity = vec(velocity)

        self.parent_node = parent_node
        self.trackball = trackball

    def draw(self, model=identity(), **other_uniforms):
        if self.static_particle.died:
            self.parent_node.remove(self)
            return

        self.position = self.position + (self.velocity * Utils.dt)
        self.transform = translate(self.position)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glDisable(GL.GL_DEPTH_TEST)
        super().draw(model=model, **other_uniforms)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)


class StaticParticle(TexturedPlane):
    def __init__(self, tex_file_name, tex_file_ext,
                 frame_count, frame_duration, scale_factor,
                 loaded_tex_list=None):
        if loaded_tex_list is None:
            super().__init__(shader=Shader("Particle.vert", "Particle.frag"),
                             tex_file=tex_file_name + "_1." + tex_file_ext,
                             scale=scale_factor)
        else:
            super().__init__(shader=Shader("Particle.vert", "Particle.frag"),
                             tex_file=None,
                             loaded_tex=loaded_tex_list[0],
                             scale=scale_factor)

        self.current_frame = 0
        self.frame_count = frame_count
        self.frame_duration = frame_duration
        self.t = 0
        self.died = False

        self.tex_list = []
        if loaded_tex_list is None:
            self.tex_list.append(self.texture)
            for i in range(2, self.frame_count + 1):
                self.tex_list.append(Texture(f"{tex_file_name}_{i}.{tex_file_ext}",
                                             self.wrap, *self.filter))
        else:
            self.tex_list.extend(loaded_tex_list)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        self.t += Utils.dt
        if self.t >= self.frame_duration:
            self.current_frame += 1
            self.t = self.t - self.frame_duration

            if self.current_frame >= self.frame_count:
                # self.parent_node.remove(self)
                # return
                self.current_frame = 0
                self.died = True

        curr_tex = self.tex_list[self.current_frame]
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(curr_tex.type, curr_tex.glid)
        uniforms['diffuse_map'] = 0
        self.drawable.draw(primitives=primitives, **uniforms)
