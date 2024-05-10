from Core import *
from Texture import *
from Transform import *
from Utils import *


class RotatingSkyBox(Node):
    def __init__(self, shader, tex_files, viewer):
        self.base_rotation = rotate(axis=(1, 0, 0), angle=90)

        super().__init__(transform=self.base_rotation)

        self.angle_y = 0
        self.add(SkyBox(shader=shader, tex_files=tex_files, viewer=viewer))

    def draw(self, model=identity(), **other_uniforms):
        super().draw(model=model, **other_uniforms)
        self.angle_y += 0.4 * Utils.dt
        self.transform = self.base_rotation @ rotate(axis=(0, 1, 0), angle=self.angle_y)


class SkyBox(Textured):
    def __init__(self, shader, tex_files, viewer):
        self.lightdir = [-1, 0, -1]
        skybox_map = TexturedMap(tex_files)
        skybox_verts = np.array([(-1, 1, -1),
                                 (-1, -1, -1),
                                 (1, -1, -1),
                                 (1, -1, -1),
                                 (1, 1, -1),
                                 (-1, 1, -1),
                                 (1, -1, -1),
                                 (1, -1, 1),
                                 (1, 1, 1),
                                 (1, 1, 1),
                                 (1, 1, -1),
                                 (1, -1, -1),
                                 (-1, -1, 1),
                                 (-1, -1, -1),
                                 (-1, 1, -1),
                                 (-1, 1, -1),
                                 (-1, 1, 1),
                                 (-1, -1, 1),
                                 (-1, -1, 1),
                                 (-1, 1, 1),
                                 (1, 1, 1),
                                 (1, 1, 1),
                                 (1, -1, 1),
                                 (-1, -1, 1),
                                 (-1, 1, -1),
                                 (1, 1, -1),
                                 (1, 1, 1),
                                 (1, 1, 1),
                                 (-1, 1, 1),
                                 (-1, 1, -1),
                                 (-1, -1, -1),
                                 (-1, -1, 1),
                                 (1, -1, -1),
                                 (1, -1, -1),
                                 (-1, -1, 1),
                                 (1, -1, 1)],
                                np.float32)
        skybox_mesh = Mesh(shader, attributes=dict(position=skybox_verts))
        self.viewer = viewer
        super().__init__(drawable=skybox_mesh, skybox=skybox_map)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        GL.glDisable(GL.GL_DEPTH_TEST)

        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index

        if uniforms.get("light_dir"):
            tmp_light = self.lightdir
            self.lightdir = [
                tmp_light[0] * np.cos(self.viewer.ground.theta) + tmp_light[2] * np.sin(self.viewer.ground.theta),
                tmp_light[1],
                tmp_light[2] * np.cos(self.viewer.ground.theta) - tmp_light[0] * np.sin(self.viewer.ground.theta)]
            uniforms["light_dir"] = self.lightdir

        self.drawable.draw(primitives=primitives, **uniforms)

        GL.glEnable(GL.GL_DEPTH_TEST)


class TexturedMap:
    def __init__(self, tex_files):
        self.glid = GL.glGenTextures(1)
        self.type = GL.GL_TEXTURE_CUBE_MAP

        GL.glBindTexture(self.type, self.glid)

        i = 0
        for tex_file in tex_files:
            Texture(tex_file=tex_file,
                    wrap_mode=GL.GL_CLAMP_TO_EDGE,
                    min_filter=GL.GL_LINEAR,
                    mag_filter=GL.GL_LINEAR,
                    tex_type=self.type,
                    glid=self.glid,
                    tex_type1=GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                    gen_mipmap=False,
                    do_bind=False,
                    wrap_r=True,
                    delete=False)
            i += 1

        GL.glBindTexture(self.type, 0)

    def __del__(self):
        GL.glDeleteTextures(self.glid)
