#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D second_texture;
in vec2 frag_tex_coords;
out vec4 out_color;

in vec3 w_position, w_normal;

uniform vec3 light_dir;

uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

uniform vec3 w_camera_position;

in float visibility;
const vec4 fog_color = vec4(0.8, 0.8, 0.8, 1.0);

void main() {
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    vec4 color1 = texture(diffuse_map, frag_tex_coords);
    vec4 color2 = texture(second_texture, frag_tex_coords);

    vec4 texture_color = mix(color1, color2, color2.a);
    vec4 illumination_color = vec4(k_a, 1) + vec4(diffuse_color, 1) + vec4(specular_color, 1);

    out_color = texture_color * illumination_color;
    out_color = mix(fog_color, out_color, visibility);
}
