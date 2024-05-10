import OpenGL.GL as GL


class WaterFrameBuffers:
    REFLECTION_WIDTH = 1920
    REFLECTION_HEIGHT = 1080

    REFRACTION_WIDTH = 1280
    REFRACTION_HEIGHT = 720

    def __init__(self):
        self.reflection_frame_buffer = 0
        self.reflection_texture = 0
        self.reflection_depth_buffer = 0

        self.refraction_frame_buffer = 0
        self.refraction_texture = 0
        self.refraction_depth_texture = 0

        self.initialise_reflection_frame_buffer()
        self.initialise_refraction_frame_buffer()

    def clean_up(self):
        GL.glDeleteFramebuffers(self.reflection_frame_buffer, 1)
        GL.glDeleteTextures(self.reflection_texture, 1)
        GL.glDeleteRenderbuffers(self.reflection_depth_buffer, 1)

        GL.glDeleteFramebuffers(self.refraction_frame_buffer, 1)
        GL.glDeleteTextures(self.refraction_texture, 1)
        GL.glDeleteTextures(self.refraction_depth_texture, 1)

    def bind_reflection_frame_buffer(self):
        self.bind_frame_buffer(self.reflection_frame_buffer,
                               WaterFrameBuffers.REFLECTION_WIDTH,
                               WaterFrameBuffers.REFLECTION_HEIGHT)

    def bind_refraction_frame_buffer(self):
        self.bind_frame_buffer(self.refraction_frame_buffer,
                               WaterFrameBuffers.REFRACTION_WIDTH,
                               WaterFrameBuffers.REFRACTION_HEIGHT)

    def unbind_current_frame_buffer(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glViewport(0, 0, 1920, 1080)

    def get_reflection_texture(self):
        return self.reflection_texture

    def get_refraction_texture(self):
        return self.refraction_texture

    def get_refraction_depth_texture(self):
        return self.refraction_depth_texture

    def initialise_reflection_frame_buffer(self):
        self.reflection_frame_buffer = self.create_frame_buffer()
        self.reflection_texture = self.create_texture_attachment(
            WaterFrameBuffers.REFLECTION_WIDTH,
            WaterFrameBuffers.REFLECTION_HEIGHT)
        self.reflection_depth_buffer = self.create_depth_buffer_attachment(
            WaterFrameBuffers.REFLECTION_WIDTH,
            WaterFrameBuffers.REFLECTION_HEIGHT)
        self.unbind_current_frame_buffer()

    def initialise_refraction_frame_buffer(self):
        self.refraction_frame_buffer = self.create_frame_buffer()
        self.refraction_texture = self.create_texture_attachment(
            WaterFrameBuffers.REFRACTION_WIDTH,
            WaterFrameBuffers.REFRACTION_HEIGHT)
        self.refraction_depth_texture = self.create_depth_texture_attachment(
            WaterFrameBuffers.REFRACTION_WIDTH,
            WaterFrameBuffers.REFRACTION_HEIGHT)
        self.unbind_current_frame_buffer()

    def bind_frame_buffer(self, frameBuffer, width, height):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, frameBuffer)
        GL.glViewport(0, 0, width, height)

    def create_frame_buffer(self):
        frame_buffer = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, frame_buffer)
        GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0)
        return frame_buffer

    def create_texture_attachment(self, width, height):
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height,
                        0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0,
                                texture, 0)
        return texture

    def create_depth_texture_attachment(self, width, height):
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_DEPTH_COMPONENT32, width, height,
                        0, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT, None)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT,
                                texture, 0)
        return texture

    def create_depth_buffer_attachment(self, width, height):
        depth_buffer = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, depth_buffer)
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, width,
                                 height)
        GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT,
                                     GL.GL_RENDERBUFFER, depth_buffer)
        return depth_buffer
