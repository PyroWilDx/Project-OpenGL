#version 330 core

// global color
uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec3 normal;

// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;

uniform vec4 plane;

void main() {
    // initialize interpolated colors at vertices
    fragment_color = color + normal + global_color;

    // tell OpenGL how to transform the vertex to clip coordinates
    vec4 w_position4 = model * vec4(position, 1.0);
    gl_Position = projection * view * w_position4;

    gl_ClipDistance[0] = dot(w_position4, plane);
}
