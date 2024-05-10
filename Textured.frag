#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D second_texture;
in vec2 frag_tex_coords;
out vec4 out_color;

in float visibility;
const vec4 fog_color = vec4(0.8, 0.8, 0.8, 1.0);

void main() {
    vec4 color1 = texture(diffuse_map, frag_tex_coords);
    vec4 color2 = texture(second_texture, frag_tex_coords);

    vec4 texture_color = mix(color1, color2, color2.a);

    out_color = texture_color;
    out_color = mix(fog_color, out_color, visibility);
}
