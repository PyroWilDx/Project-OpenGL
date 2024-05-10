from Core import Node, load


class Cylinder(Node):
    """ Very simple cylinder based on provided load function """

    def __init__(self, shader, tex_file=None, pre_tex=None):
        super().__init__()
        if tex_file is not None:
            self.add(*load('models/Cylinder.obj', shader=shader, tex_file=tex_file, pre_tex=pre_tex))
        else:
            self.add(*load('models/Cylinder.obj', shader=shader))
