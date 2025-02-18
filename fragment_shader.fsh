#version 330 core
out vec4 FragColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;
uniform int colorMode;

void main() {
    FragColor = texture(ourTexture, TexCoord);
    if(gl_FragCoord.x >= 300.0) {
        discard;//FragColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
}