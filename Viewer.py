#!/usr/bin/env python3

from Skybox import *
from Ground import *
from Water import *
from Player import *
from Tree import *


def main():
    viewer = Viewer()

    # SkyBox Start ======================
    skybox_shader = Shader("Skybox.vert", "Skybox.frag")
    skybox = RotatingSkyBox(shader=skybox_shader,
                            tex_files=["textures/skybox/Right.png",
                                       "textures/skybox/Left.png",
                                       "textures/skybox/Top.png",
                                       "textures/skybox/Bottom.png",
                                       "textures/skybox/Front.png",
                                       "textures/skybox/Back.png"],
                            viewer=viewer)
    viewer.add(skybox)

    def vectoriser(p1, p2):
        return p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]

    def mult_pos(pos, mul):
        ret = []
        for i in range(len(pos)):
            ret.append(pos[i] * mul)
        return ret

    # Ground Start ======================
    N = 150

    ground_shader = Shader("Ground.vert", "Ground.frag")

    ground_t = [[[[i / N, j / N, rd.random() / 300], N * i + j, [0, 0, 0]] for j in range(N)] for i in range(N)]

    debut_ravin = rd.randint(N // 10, N - N // 10)
    for i in range(N):
        for k in range(-N // 20 + rd.randint(-N // 50, N // 50), N // 20 + rd.randint(-N // 100, N // 100)):
            ground_t[debut_ravin + k][i][0][2] = min(-0.1 + k ** 2 * 0.001, 0) + rd.random() / 100

    start_water_x_unscaled = debut_ravin
    start_water_x = start_water_x_unscaled - N // 20 - 6
    end_water_x = debut_ravin + N // 20 + 6
    viewer.set_water_x(start_water_x * 100.0 / 150.0, end_water_x * 100.0 / 150.0)

    for i in range(N):
        for j in range(N):
            ground_t[i][j][0][2] = (ground_t[i - 1][j][0][2] + ground_t[i][j - 1][0][2] + ground_t[(i + 1) % N][j][0][
                2] + ground_t[i][(j + 1) % N][0][2] + ground_t[i][j][0][2]) / 3 + rd.normalvariate(0, 0.1) / 100
            if i == 0 or j == N - 1 or j == 0 or i == N - 1:
                ground_t[i][j][0][2] = -0.01

    for _ in range(3):
        x_mont = rd.randint(N // 5, N - N // 5)
        while abs(x_mont - debut_ravin) < N // 20 + 23.2:
            x_mont = rd.randint(N // 5, N - N // 5)
        y_mont = rd.randint(N // 5, N - N // 5)
        for i in range(-N // 5 + 1, N // 5):
            for j in range(-N // 5 + 1, N // 5):
                if ground_t[i][j][0][2] >= -0.2:
                    ground_t[x_mont + i][y_mont + j][0][2] += max(0, (
                            0.5 - (i ** 2 + j ** 2) ** (1 / 2) / (N // 5)) + 0.05 * rd.random())

    ground_indices = []
    coords = []
    normal = []
    for i in range(N):
        for j in range(N):
            coords.append(ground_t[i][j][0])

    for i in range(N):
        for j in range(N):
            if (i != N - 1) and (j != N - 1):
                ground_t[i][j][2] += np.cross(vectoriser(ground_t[i][j][0], ground_t[i + 1][j][0]),
                                              vectoriser(ground_t[i][j][0], ground_t[i][j + 1][0]))
            if (i != 0) and (j != N - 1):
                ground_t[i][j][2] += np.cross(vectoriser(ground_t[i][j][0], ground_t[i][j + 1][0]),
                                              vectoriser(ground_t[i][j][0], ground_t[i - 1][j][0]))
            if (i != 0) and (j != 0):
                ground_t[i][j][2] += np.cross(vectoriser(ground_t[i][j][0], ground_t[i - 1][j][0]),
                                              vectoriser(ground_t[i][j][0], ground_t[i][j - 1][0]))
            if (i != N - 1) and (j != 0):
                ground_t[i][j][2] += np.cross(vectoriser(ground_t[i][j][0], ground_t[i][j - 1][0]),
                                              vectoriser(ground_t[i][j][0], ground_t[i + 1][j][0]))
            normal.append(ground_t[i][j][2])

    ground_tex = Texture("textures/GroundCanyon.png", wrap_mode=GL.GL_REPEAT)

    for i in range(N - 1):
        for j in range(N - 1):
            ground_indices.append(ground_t[i][j][1])
            ground_indices.append(ground_t[i + 1][j][1])
            ground_indices.append(ground_t[i + 1][j + 1][1])
            ground_indices.append(ground_t[i][j][1])
            ground_indices.append(ground_t[i + 1][j + 1][1])
            ground_indices.append(ground_t[i][j + 1][1])

    ground = Ground(ground_shader, tex1=ground_tex, tex2=None,
                    indices=ground_indices, coords=coords, normal=normal,
                    light_dir=[-1, 0, -1], K_d=(.6, .7, .8), K_a=(0.1, 0.1, 0.1), K_s=(0.1, 0.1, 0.1),
                    s=100)
    viewer.add(ground)

    # Water Start ======================
    water_shader = Shader("Water.vert", "Water.frag")

    water_size = 4.88
    water_scale = 20
    offset = 0.082

    water_z = -0.01

    water_coords = [(offset, offset, water_z),
                    (water_size, offset, water_z),
                    (water_size, water_size, water_z),
                    (offset, water_size, water_z)]
    water_indices = [0, 1, 2, 0, 2, 3]
    water_indices = np.array(water_indices, np.uint32)

    water_wraps = next(cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                              GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE]))
    water_filters = next(cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                                (GL.GL_LINEAR, GL.GL_LINEAR),
                                (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)]))
    water_tex = Texture("textures/Water.png", water_wraps, *water_filters)

    water = Water(water_shader, tex1=water_tex, tex2=None,
                  indices=water_indices, coords=water_coords, normal=normal,
                  light_dir=(0, 0, 0), K_d=(0, 0, 0), K_a=(0, 0, 0), s=0)

    scaled_water = Node(transform=scale(water_scale, water_scale, water_scale))
    scaled_water.add(water)

    viewer.add(scaled_water)

    # Tree Start ======================
    tex = Texture(tex_file="textures/TreeTrunk.jpg",
                  delete=False,
                  do_print=True)
    trunk_shader = Shader("Textured.vert", "Textured.frag")
    cyl = Cylinder(trunk_shader, "textures/TreeTrunk.jpg", pre_tex=tex)
    for _ in range(6):
        tree_position = mult_pos(ground_t[rd.randint(10, N - 10)][rd.randint(10, N - 10)][0], 100)
        while viewer.is_x_in_water(tree_position[0]):
            tree_position = mult_pos(ground_t[rd.randint(10, N - 10)][rd.randint(10, N - 10)][0], 100)
        viewer.add(Tree(position=tree_position,
                        tex=tex,
                        cyl=cyl))

    # Player Start ======================
    player = Player(position=(-4, 0, 1), viewer=viewer)
    viewer.add(player)

    # Affichage des Commandes ======================
    print("\n============ Commandes ============")
    print("- Déplacement : WASD / ZQSD (Selon le langage du clavier).")
    print("- Accélérer le déplacement : C (Maintenir la touche).")
    print("- Voler vers le haut : Espace.")
    print("- Voler vers le vas : Left Shift.")
    print("- Zoom in/out : Scroller la souris.")
    print("- Rotation de la caméra : Bouger la souris avec le clique gauche appuyé.")
    print("- Activer/Désactiver la fumée : F.")
    print("- Décélerer cycle jour/nuit : B.")
    print("- Accélerer cycle jour/nuit : N.")
    print("- Arrêter cycle jour/nuit : H.")
    print("- Reprendre cycle jour/nuit : J.")
    print("- Mode polygone : P.")
    print("- Quitter : Escape.")
    print("===================================\n")

    # Run
    viewer.run(player=player, water=water, ground=ground)


if __name__ == '__main__':
    main()
