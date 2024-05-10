#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 position;
in vec2 tex_coord;
in vec2 tex_coord2;

out vec2 frag_tex_coords;
out vec2 frag_tex_coords2;

uniform vec4 plane;

out float visibility;

// Augmenter pour baisser la visibilité du joueur
const float density = 0.0076;

// Augmenter pour baisser la transition entre visibilité / non-visibilité
const float gradient = 1.6;

void main() {
    vec4 w_position4 = model * vec4(position, 1.0);
    vec4 position_relative_to_camera = view * w_position4;
    gl_Position = projection * position_relative_to_camera;

    gl_ClipDistance[0] = dot(w_position4, plane);

    frag_tex_coords = tex_coord;
    frag_tex_coords2 = tex_coord2;

    float distance = length(position_relative_to_camera.xyz);
    visibility = exp(-pow(distance * density, gradient));
    visibility = clamp(visibility, 0, 1.0);
}
