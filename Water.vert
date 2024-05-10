#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 position;

out vec2 frag_tex_coords;

out vec4 clip_space;

const float tiling = 0.72;

uniform vec3 w_camera_position;
out vec3 to_camera_vector;

out vec3 from_light_vector;

out float visibility;
const float density = 0.0076;
const float gradient = 1.6;

void main() {
    vec4 w_position4 = model * vec4(position, 1.0);
    vec4 position_relative_to_camera = view * w_position4;
    clip_space = projection * position_relative_to_camera;
    gl_Position = clip_space;

    frag_tex_coords = vec2(position.x / 2.0 + 0.5, position.y / 2.0 + 0.5) * tiling;

    to_camera_vector = w_camera_position - w_position4.xyz;
    from_light_vector = w_position4.xyz - vec3(0, 0, 0);

    float distance = length(position_relative_to_camera.xyz);
    visibility = exp(-pow(distance * density, gradient));
    visibility = clamp(visibility, 0, 1.0);
}
