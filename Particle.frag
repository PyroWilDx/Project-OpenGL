#version 330 core

uniform sampler2D diffuse_map;
in vec2 frag_tex_coords;
out vec4 out_color;

void main() {
    vec4 tex_color = texture(diffuse_map, frag_tex_coords);
    if (tex_color.r == 0 && tex_color.g == 0 && tex_color.b == 0) {
        tex_color.a = 0;
    } else {
        tex_color.a = 1;
    }
    out_color = tex_color;
}
