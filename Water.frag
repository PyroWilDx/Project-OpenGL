#version 330 core

in vec2 frag_tex_coords;
out vec4 out_color;

in vec4 clip_space;

uniform sampler2D reflection_texture;
uniform sampler2D refraction_texture;
uniform sampler2D dudv;
uniform sampler2D normal_map;

uniform float move_factor;

const float wave_strength = 0.01;

in vec3 to_camera_vector;
const float reflect_strength = 1.0;

in vec3 from_light_vector;
const float shine_damper = 20.0;
const float reflectivity = 0.6;

in float visibility;
const vec4 fog_color = vec4(0.8, 0.8, 0.8, 1.0);

void main() {
    vec2 ndc = (clip_space.xy / clip_space.w) / 2.0 + 0.5;
    vec2 reflect_tex_coords = vec2(ndc.x, -ndc.y);
    vec2 refract_tex_coords = vec2(ndc.x, ndc.y);

    //    vec2 distortion1 = (texture(dudv, vec2(frag_tex_coords.x + move_factor, frag_tex_coords.y)).rg * 2.0 - 1.0) * wave_strength;
    //    vec2 distortion2 = (texture(dudv, vec2(-frag_tex_coords.x + move_factor, frag_tex_coords.y + move_factor)).rg * 2.0 - 1.0) * wave_strength;
    //    vec2 total_distortion = distortion1 + distortion2;

    vec2 distorted_tex_coords = texture(dudv, vec2(frag_tex_coords.x + move_factor, frag_tex_coords.y)).rg * 0.1;
    distorted_tex_coords = frag_tex_coords + vec2(distorted_tex_coords.x, distorted_tex_coords.y + move_factor);
    vec2 total_distortion = (texture(dudv, distorted_tex_coords).rg * 2.0 - 1.0) * wave_strength;

    reflect_tex_coords += total_distortion;
    reflect_tex_coords.x = clamp(reflect_tex_coords.x, 0.001, 0.999);
    reflect_tex_coords.y = clamp(reflect_tex_coords.y, -0.999, -0.001);

    refract_tex_coords += total_distortion;
    refract_tex_coords = clamp(refract_tex_coords, 0.001, 0.999);

    vec4 reflect_color = texture(reflection_texture, reflect_tex_coords);
    vec4 refract_color = texture(refraction_texture, refract_tex_coords);

    vec3 view_vector = normalize(to_camera_vector);
    float refractive_factor = dot(view_vector, vec3(0, 1.0, 0));
    refractive_factor = pow(refractive_factor, reflect_strength);

    vec4 normal_map_color = texture(normal_map, distorted_tex_coords);
    vec3 normal = vec3(normal_map_color.r * 2.0 - 1.0, normal_map_color.b, normal_map_color.g * 2.0 - 1.0);
    normal = normalize(normal);

    vec3 reflected_light = reflect(normalize(from_light_vector), normal);
    float specular = max(dot(reflected_light, view_vector), 0);
    specular = pow(specular, shine_damper);
    vec3 specular_highlights = vec3(1.0, 1.0, 1.0) * specular * reflectivity;

    out_color = mix(reflect_color, refract_color, 0.5);
    out_color = mix(out_color, vec4(0, 0.36, 0.56, 1.0), 0.2) + vec4(specular_highlights, 0);
    out_color = mix(fog_color, out_color, visibility);
}
