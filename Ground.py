from Texture import *


class Ground(Textured):
    theta = 0.01

    def __init__(self, shader, tex1, tex2, indices, coords, normal, **params):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.lightdir = params.get("light_dir")
        self.theta = 0.01
        scale = 100

        scaled = scale * np.array(coords, np.float32)
        tex_coord = scale * np.array(((0, 0), (1, 0), (1, 1), (0, 1)), dtype=np.float32)

        uniforms = dict(
            k_d=np.array(params.get("K_d"), dtype=np.float32),
            k_s=np.array(params.get("K_s"), dtype=np.float32),
            k_a=np.array(params.get("K_a"), dtype=np.float32),
            s=16.0,
            light_dir=[0, 0, 1]
        )
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=tex_coord,
                                            normal=normal),
                    index=indices, **{**uniforms, **params})

        if tex2 is not None:
            super().__init__(mesh, diffuse_map=tex1, second_texture=tex2)
        else:
            super().__init__(mesh, diffuse_map=tex1)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index
        if uniforms.get("light_dir"):
            tmp_light = self.lightdir
            self.lightdir = [tmp_light[0] * np.cos(self.theta) + tmp_light[2] * np.sin(self.theta), tmp_light[1],
                             tmp_light[2] * np.cos(self.theta) - tmp_light[0] * np.sin(self.theta)]
            uniforms["light_dir"] = self.lightdir
        self.drawable.draw(primitives=primitives, **uniforms)

    def get_light(self):
        return self.lightdir
