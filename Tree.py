from Core import Shader
from Transform import *
from Animation import *
import random as rd
import math


class Tree(Node):
    def __init__(self, position, just_trunk=False, tex=None, cyl=None):
        super().__init__(transform=translate(position))

        trunk = Trunk(cyl=cyl)
        self.add(trunk)

        if just_trunk:
            return

        root_branch_n = rd.randint(2, 8)
        min_z = 0.0
        max_z = 6.0
        step_z = (max_z - min_z) / root_branch_n
        curr_z = step_z
        for _ in range(0, root_branch_n):
            base_rotation = rd.randint(0, 360)
            depth = rd.randint(2, 8)
            branch = Node(transform=
                          translate(0, 0, curr_z) @
                          rotate(axis=(0, 0, 1), angle=base_rotation))
            branch.add(Branch(d=depth, max_d=depth, texture=tex, cyl=cyl))
            self.add(branch)

            curr_z += step_z


class Trunk(Node):
    def __init__(self, cyl=None):
        super().__init__()

        base_scale = 0.2
        child_scale = 0.8

        trunk0 = Node(transform=
                      scale(base_scale, base_scale, 1.6) @
                      rotate(axis=(1, 0, 0), angle=90))
        trunk0.add(cyl)
        self.add(trunk0)

        trunk1 = Node(transform=
                      translate(0, 1.6, 0) @
                      scale(child_scale, 1, child_scale))
        trunk1.add(cyl)
        trunk0.add(trunk1)

        trunk2 = Node(transform=
                      translate(0, 1.6, 0) @
                      scale(child_scale, 1, child_scale))
        trunk2.add(cyl)
        trunk1.add(trunk2)


class Branch(Node):
    NEW_BRANCH_PROBABILITY = 0.2

    def __init__(self, d, max_d, texture=None, cyl=None):
        super().__init__()

        trslt_value = 1.92
        if d == max_d:
            trslt_value /= 2

        ag = rd.randint(-6, 30)
        r_x = 1
        r_z = 1
        r_x, _, r_z = normalized(vec(r_x, 0, r_z))

        trslt_value = abs(trslt_value * math.cos(math.radians(ag / 2.2)))

        branch = Node(transform=
                      translate(r_x * -math.sin(math.radians(ag)),
                                trslt_value,
                                r_z * math.sin(math.radians(ag))) @
                      rotate(axis=(r_x, 0, r_z), angle=ag))
        scaled = Node(transform=
                      scale(0.1 * pow(0.92, max_d - d), 1, 0.1 * pow(0.92, max_d - d)))
        scaled.add(cyl)
        branch.add(scaled)
        self.add(branch)

        if d != 1:
            branch.add(Branch(d=d - 1, max_d=max_d, texture=texture, cyl=cyl))
            if rd.random() < Branch.NEW_BRANCH_PROBABILITY:
                new_angle = rd.randint(42, 142)
                if rd.random() < 1 / 2.:
                    new_angle = -new_angle
                new_branch = Node(transform=
                                  rotate(axis=(0, 0, 1), angle=new_angle))
                new_branch.add(Branch(d=d - 1, max_d=d - 1, texture=texture, cyl=cyl))
                branch.add(new_branch)
