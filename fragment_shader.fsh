#version 330
out vec4 fragColor;
void main() {
    fragColor = vec4(0.0, 0.0, 0.0, 0.0);
    if(gl_FragCoord.x > 400.0) {
        fragColor = vec4(0.0, 0.0, 1.0, 1.0);
    }
}