from Core import *
from Texture import *
from Transform import *
from Utils import *


class Water(Textured):
    WAVE_SPEED = 0.026

    def __init__(self, shader, tex1, tex2, indices, coords, normal, **params):
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.lightdir = params.get("light_dir")

        self.height = coords[0][2]

        scaled = np.array(coords, np.float32)
        tex_coord = np.array(((0, 0), (1, 0), (1, 1), (0, 1)), dtype=np.float32)

        uniforms = dict(
            k_d=np.array([0.6, 0.7, 0.8], dtype=np.float32),
            k_s=np.array([1, 1, 1], dtype=np.float32),
            k_a=np.array([0, 0, 0], dtype=np.float32),
            s=16.0,
        )

        self.t = 0

        self.shader = shader
        self.atts = dict(position=scaled,
                         tex_coord=tex_coord,
                         normal=normal)

        self.indices = indices
        self.uniforms = uniforms
        self.params = params

        self.mesh = Mesh(shader, attributes=self.atts,
                         index=indices, **{**uniforms, **params})

        self.fbos = None
        self.dudv = Texture("textures/WaterDudv.png")
        self.normal_map = Texture("textures/WaterNormalMap.png")

        if tex2 is not None:
            super().__init__(self.mesh, diffuse_map=tex1, second_texture=tex2)
        else:
            super().__init__(self.mesh, diffuse_map=tex1)

    def set_fbos(self, value):
        self.fbos = value

    def get_height(self):
        return self.height

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        self.t += Water.WAVE_SPEED * Utils.dt
        self.t %= 1

        uniforms['move_factor'] = self.t

        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.fbos.get_reflection_texture())
        uniforms['reflection_texture'] = 0

        GL.glActiveTexture(GL.GL_TEXTURE1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.fbos.get_refraction_texture())
        uniforms['refraction_texture'] = 1

        GL.glActiveTexture(GL.GL_TEXTURE2)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.dudv.glid)
        uniforms['dudv'] = 2

        GL.glActiveTexture(GL.GL_TEXTURE3)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.normal_map.glid)
        uniforms['normal_map'] = 3

        self.drawable.draw(primitives=primitives, **uniforms)
