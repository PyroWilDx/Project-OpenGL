import OpenGL.GL as GL  # standard Python OpenGL wrapper
from PIL import Image  # load texture maps
from itertools import cycle
import numpy as np
from Core import Mesh


# -------------- OpenGL Texture Wrapper ---------------------------------------
class Texture:
    """ Helper class to create and automatically destroy textures """

    def __init__(self, tex_file, wrap_mode=GL.GL_REPEAT,
                 mag_filter=GL.GL_LINEAR, min_filter=GL.GL_LINEAR_MIPMAP_LINEAR,
                 tex_type=GL.GL_TEXTURE_2D, glid=None, tex_type1=None,
                 gen_mipmap=True, do_bind=True, wrap_r=False, delete=True,
                 do_print=True):
        self.delete = delete
        if tex_type1 is None:
            tex_type1 = tex_type
        if glid is None:
            self.glid = GL.glGenTextures(1)
        else:
            self.glid = glid
        self.type = tex_type
        try:
            # imports image as a numpy array in exactly right format
            tex = Image.open(tex_file).convert('RGBA')
            if do_bind:
                GL.glBindTexture(tex_type, self.glid)
            GL.glTexImage2D(tex_type1, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_S, wrap_mode)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_T, wrap_mode)
            if wrap_r:
                GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_R, wrap_mode)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MIN_FILTER, min_filter)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MAG_FILTER, mag_filter)
            if gen_mipmap:
                GL.glGenerateMipmap(tex_type)
            if do_print:
                print(f'Loaded texture {tex_file} ({tex.width}x{tex.height}'
                      f' wrap={str(wrap_mode).split()[0]}'
                      f' min={str(min_filter).split()[0]}'
                      f' mag={str(mag_filter).split()[0]})')
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % tex_file)

    def __del__(self):  # delete GL texture from GPU when object dies
        if self.delete:
            GL.glDeleteTextures(self.glid)


# -------------- Textured mesh decorator --------------------------------------
class Textured:
    """ Drawable mesh decorator that activates and binds OpenGL textures """

    def __init__(self, drawable, **textures):
        self.drawable = drawable
        self.textures = textures

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index
        if uniforms.get("light_dir"):
            tmp_light = uniforms["light_dir"]
            uniforms["light_dir"] = [tmp_light[0] * np.cos(0.1) + tmp_light[2] * np.sin(0.1), tmp_light[1],
                                     tmp_light[2] * np.cos(0.1) - tmp_light[0] * np.sin(0.1)]
        self.drawable.draw(primitives=primitives, **uniforms)


class TexturedPlane(Textured):
    """ Simple first textured object """

    def __init__(self, shader, tex_file, scale=1, loaded_tex=None):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        base_coords = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0))
        scaled = scale * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        if loaded_tex is None:
            self.texture = Texture(tex_file, self.wrap, *self.filter)
        else:
            self.texture = loaded_tex
        super().__init__(mesh, diffuse_map=self.texture)
