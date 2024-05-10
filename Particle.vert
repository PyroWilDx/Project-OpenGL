#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
in vec3 position;

out vec2 frag_tex_coords;

void main() {
    mat4 no_rotation_model = model;

    no_rotation_model[0][0] = view[0][0];
    no_rotation_model[0][1] = view[1][0];
    no_rotation_model[0][2] = view[2][0];

    no_rotation_model[1][0] = view[0][1];
    no_rotation_model[1][1] = view[1][1];
    no_rotation_model[1][2] = view[2][1];

    no_rotation_model[2][0] = view[0][2];
    no_rotation_model[2][1] = view[1][2];
    no_rotation_model[2][2] = view[2][2];

    gl_Position = projection * view * no_rotation_model * vec4(position, 1);
    frag_tex_coords = position.xy;
}
