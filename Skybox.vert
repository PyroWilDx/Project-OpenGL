#version 330 core

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

in vec3 position;

out vec3 tex_coords;

void main() {
    vec4 p = projection * mat4(mat3(view)) * model * vec4(position, 1.0);
    gl_Position = vec4(p.x, p.y, p.w, p.w);

    tex_coords = vec3(position.x, position.y, position.z);
}
