#version 330 core

uniform samplerCube skybox;
uniform vec3 light_dir;

in vec3 tex_coords;
out vec4 out_color;

void main() {
    out_color = texture(skybox, tex_coords)* min(max(dot(light_dir, vec3(0, 0, -1)), 0.2), 0.8);
}
