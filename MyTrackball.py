from Transform import *


class MyTrackball:
    MIN_DISTANCE = 1
    MAX_DISTANCE = 120

    def __init__(self):
        self.player = None
        self.yaw = -90
        self.pitch = 0
        self.zoom = 56
        self.orientation = True

        self.additional_z = 0

    def set_player(self, value):
        self.player = value
        self.player.set_trackball(self)
        self.player.update_face_side_foot(self.yaw, self.pitch)

    def get_position(self):
        result = self.player.position - \
                 (6 * self.player.face) + \
                 (0.8 * self.player.side) + \
                 (0.6 * self.player.foot)
        result[2] += self.additional_z
        return result

    def view_matrix(self):
        self_position = self.get_position()
        roll = self.player.foot[2]
        if not self.orientation:
            roll = -roll
        return lookat(self_position,
                      self_position + self.player.face,
                      vec(self.player.foot[0], self.player.foot[1], roll))

    def projection_matrix(self, win_size):
        w = win_size[0]
        h = win_size[1]
        if w == 0:
            w = 160
        if h == 0:
            h = 90
        return perspective(self.zoom,
                           w / h,
                           0.01,
                           424242)

    def on_mouse_move(self, x_diff, y_diff):
        speed = 0.1
        self.yaw += x_diff * speed
        self.pitch += y_diff * speed

        self.pitch = max(self.pitch, -90)
        self.pitch = min(self.pitch, 90)

        self.player.update_face_side_foot(self.yaw, self.pitch)

    def on_mouse_scroll(self, z_diff):
        self.zoom -= z_diff
        self.zoom = max(self.zoom, MyTrackball.MIN_DISTANCE)
        self.zoom = min(self.zoom, MyTrackball.MAX_DISTANCE)

    def invert_pitch(self):
        self.pitch = -self.pitch
        self.player.update_face_side_foot(self.yaw, self.pitch)

    def invert_orientation(self):
        self.orientation = not self.orientation

    def set_additional_z(self, value):
        self.additional_z = value

    def unset_additional_z(self):
        self.additional_z = 0
