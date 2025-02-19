#version 330 core
out vec4 FragColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;
uniform vec2 windowSize;
uniform float padding;
uniform vec2 gameWindowSize;
uniform float elementWindowWidth;

int inRoundBox(vec2 topLeft, vec2 bottomRight, float radius) {
    if(gl_FragCoord.x > topLeft.x && gl_FragCoord.x < bottomRight.x && gl_FragCoord.y > topLeft.y && gl_FragCoord.y < bottomRight.y) {
        if(distance(vec2(topLeft.x + radius, topLeft.y + radius), gl_FragCoord.xy) > radius && gl_FragCoord.x < topLeft.x + radius && gl_FragCoord.y < topLeft.y + radius) {
            return 0;
        }
        if(distance(vec2(topLeft.x + radius, bottomRight.y - radius), gl_FragCoord.xy) > radius && gl_FragCoord.x < topLeft.x + radius && gl_FragCoord.y > bottomRight.y - radius) {
            return 0;
        }
        if(distance(vec2(bottomRight.x - radius, topLeft.y + radius), gl_FragCoord.xy) > radius && gl_FragCoord.x > bottomRight.x - radius && gl_FragCoord.y < topLeft.y + radius) {
            return 0;
        }
        if(distance(vec2(bottomRight.x - radius, bottomRight.y - radius), gl_FragCoord.xy) > radius && gl_FragCoord.x > bottomRight.x - radius && gl_FragCoord.y > bottomRight.y - radius) {
            return 0;
        }
        return 1;
    }
    return 0;
}

vec4 interpolate(vec4 firstColor, vec4 secondColor, float mediator) {
    return vec4(firstColor.r + (secondColor.r - firstColor.r) * mediator, firstColor.g + (secondColor.g - firstColor.g) * mediator, firstColor.b + (secondColor.b - firstColor.b) * mediator, firstColor.a + (secondColor.a - firstColor.a) * mediator);
}

int inElement(vec2 topLeft, vec2 size, vec4 color, float borderWidth, int type) {
    if(gl_FragCoord.x > topLeft.x && gl_FragCoord.x < topLeft.x + size.x && gl_FragCoord.y > topLeft.y && gl_FragCoord.y < topLeft.y + size.y) {
        FragColor = interpolate(color, vec4(0.0, 0.0, 0.0, 0.0), 0.25);
        if(gl_FragCoord.x > topLeft.x + borderWidth && gl_FragCoord.x < topLeft.x + size.x - borderWidth && gl_FragCoord.y > topLeft.y + borderWidth && gl_FragCoord.y < topLeft.y + size.y - borderWidth) {
            FragColor = color;
            return 1;
        }
    }
    if(gl_FragCoord.x - topLeft.x < gl_FragCoord.y - topLeft.y + 20.0 && gl_FragCoord.x > topLeft.x && gl_FragCoord.y < topLeft.y) {
        FragColor = interpolate(color, vec4(0.0, 0.0, 0.0, 0.0), 0.25);;
    }
    return 0;
}

float borderRadius = 20.0;

vec4 darkBackGround = vec4(0.1801, 0.158, 0.357, 1.0);
vec4 brightBackGround = vec4(0.2421, 0.214, 0.48, 1.0);
vec4 foreGround = vec4(0.125, 0.117, 0.1875, 1.0);

vec4 moveCategory = vec4(0.496, 0.351, 1.0, 1.0);

float borderWidth = 5.0;

void main() {
    vec4 gradientBackGround = interpolate(darkBackGround, brightBackGround, gl_FragCoord.y / windowSize.y);

    FragColor = texture(ourTexture, TexCoord);

    if(inRoundBox(vec2(windowSize.x - padding - gameWindowSize.x, windowSize.y - padding - gameWindowSize.y), vec2(windowSize.x - padding, windowSize.y - padding), borderRadius) == 0) {
        FragColor = vec4(0.125, 0.117, 0.1875, 1.0);
        //game
    }
    if(inRoundBox(vec2(padding, padding), vec2(padding + elementWindowWidth, windowSize.y - padding), borderRadius) == 1) {
        FragColor = gradientBackGround;
        if(gl_FragCoord.y < padding + 75.0) {
            FragColor = moveCategory;
        }
        //element
        if(inElement(vec2(padding * 2.0, windowSize.y - padding * 2.0 - 40.0), vec2(150.0, 40.0), moveCategory, borderWidth, 0) == 1) {
            
        }

    }
    if(inRoundBox(vec2(2.0 * padding + elementWindowWidth, padding), vec2(windowSize.x - 2.0 * padding - gameWindowSize.x, windowSize.y - padding), borderRadius) == 1) {
        FragColor = gradientBackGround;
        //codespace

    }
    if(inRoundBox(vec2(windowSize.x - padding - gameWindowSize.x, padding), vec2(windowSize.x - padding, windowSize.y - gameWindowSize.y - padding * 2.0), borderRadius) == 1) {
        FragColor = gradientBackGround;
        //scenario

    }
}