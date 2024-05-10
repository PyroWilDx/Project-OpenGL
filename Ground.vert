#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 position;
in vec2 tex_coord;
in vec2 tex_coord2;

out vec2 frag_tex_coords;
out vec2 frag_tex_coords2;

in vec3 normal;
out vec3 w_position, w_normal;

uniform vec4 plane;

out float visibility;
const float density = 0.0076;
const float gradient = 1.6;

void main() {
    vec4 w_position4 = model * vec4(position, 1.0);
    vec4 position_relative_to_camera = view * w_position4;
    gl_Position = projection * position_relative_to_camera;

    gl_ClipDistance[0] = dot(w_position4, plane);

    frag_tex_coords = position.xy;
    frag_tex_coords2 = position.xy;

    w_position = w_position4.xyz / w_position4.w;

    mat3 nit_matrix = transpose(inverse(mat3(model)));
    w_normal = normalize(nit_matrix * normal);

    float distance = length(position_relative_to_camera.xyz);
    visibility = exp(-pow(distance * density, gradient));
    visibility = clamp(visibility, 0, 1.0);
}
