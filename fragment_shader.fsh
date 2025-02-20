#version 330 core
out vec4 FragColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

uniform int scene;

uniform vec2 windowSize;
uniform float padding;
uniform float barWidth;
uniform float barPadding;
uniform vec2 gameWindowSize;
uniform float elementWindowWidth;
uniform vec4 currentCategory;
uniform float elementsListHeight;
uniform float elementsBarPercent;
uniform float categoryHeight;
uniform int displayArea;
uniform int isText;

uniform vec2 blockPos;
uniform vec2 blockSize;
uniform vec4 blockColor;
uniform int blockFormat;

uniform float menuOuterOffset;
uniform float menuOuterWidth;
uniform float menuOuterRadius;

float borderRadius = 10.0;

vec4 darkBackGround = vec4(0.1801, 0.158, 0.357, 1.0);
vec4 brightBackGround = vec4(0.2421, 0.214, 0.48, 1.0);
vec4 foreGround = vec4(0.125, 0.117, 0.1875, 1.0);

vec4 moveCategory = vec4(0.496, 0.351, 1.0, 1.0);

float borderWidth = 4.0;

float triangleHeight = 20.0;

float threeHalfs = 1.5;

vec4 tempGrass = vec4(0.263, 0.631, 0.345, 1.0);

float barRadius = (barWidth - barPadding * 2.0) / 2.0;

int inRoundBox(vec2 topLeft, vec2 bottomRight, float radius) {
    if(gl_FragCoord.x > topLeft.x && gl_FragCoord.x < bottomRight.x && gl_FragCoord.y > topLeft.y && gl_FragCoord.y < bottomRight.y) {
        if (distance(vec2(topLeft.x + radius, topLeft.y + radius), gl_FragCoord.xy) > radius && gl_FragCoord.x < topLeft.x + radius && gl_FragCoord.y < topLeft.y + radius) {
            return 0;
        }
        if (distance(vec2(topLeft.x + radius, bottomRight.y - radius), gl_FragCoord.xy) > radius && gl_FragCoord.x < topLeft.x + radius && gl_FragCoord.y > bottomRight.y - radius) {
            return 0;
        }
        if (distance(vec2(bottomRight.x - radius, topLeft.y + radius), gl_FragCoord.xy) > radius && gl_FragCoord.x > bottomRight.x - radius && gl_FragCoord.y < topLeft.y + radius) {
            return 0;
        }
        if (distance(vec2(bottomRight.x - radius, bottomRight.y - radius), gl_FragCoord.xy) > radius && gl_FragCoord.x > bottomRight.x - radius && gl_FragCoord.y > bottomRight.y - radius) {
            return 0;
        }
        return 1;
    }
    return 0;
}

vec4 interpolate(vec4 firstColor, vec4 secondColor, float mediator) {
    mediator = max(0.0, min(1.0, mediator));
    return vec4(firstColor.r + (secondColor.r - firstColor.r) * mediator, firstColor.g + (secondColor.g - firstColor.g) * mediator, firstColor.b + (secondColor.b - firstColor.b) * mediator, firstColor.a + (secondColor.a - firstColor.a) * mediator);
}

int inElement(vec2 topLeft, vec2 size, vec4 color, float borderWidth, int type) {
    vec4 interpol = interpolate(color, vec4(0.0, 0.0, 0.0, 0.0), 0.25);

    int inside = 0;
    if (gl_FragCoord.x > topLeft.x && gl_FragCoord.x < topLeft.x + size.x && gl_FragCoord.y > topLeft.y && gl_FragCoord.y < topLeft.y + size.y && gl_FragCoord.x - topLeft.x > gl_FragCoord.y - topLeft.y - size.y + triangleHeight) {
        FragColor = interpol;

        if (gl_FragCoord.x > topLeft.x + borderWidth && gl_FragCoord.x < topLeft.x + size.x - borderWidth && gl_FragCoord.y > topLeft.y + borderWidth && gl_FragCoord.y < topLeft.y + size.y - borderWidth && gl_FragCoord.x - topLeft.x > gl_FragCoord.y - topLeft.y - size.y + triangleHeight + borderWidth * threeHalfs) {
            FragColor = color;
        }
        inside = 1;
    }
    if (gl_FragCoord.x - topLeft.x <= gl_FragCoord.y - topLeft.y + triangleHeight && gl_FragCoord.x > topLeft.x && gl_FragCoord.y < topLeft.y + borderWidth) {
        FragColor = interpol;
        
        if (gl_FragCoord.x - topLeft.x <= gl_FragCoord.y - topLeft.y + triangleHeight - borderWidth * threeHalfs && gl_FragCoord.x > topLeft.x && gl_FragCoord.y < topLeft.y + borderWidth && gl_FragCoord.x > topLeft.x + borderWidth) {
            FragColor = color;
        }
        inside = 1;
    }
    return inside;
}

void drawBar(vec2 topLeft, float height, float viewSpam, float totalSpam, float viewSpamOffset) {
    if (inRoundBox(topLeft, vec2(topLeft.x + barWidth - barPadding * 2.0, topLeft.y + height), barRadius) == 1) {
        FragColor = foreGround;
        float holdHeight = viewSpam / totalSpam * height;
        float verticalHoldPos = (1.0 - viewSpamOffset) * (height - holdHeight);
        if (inRoundBox(vec2(topLeft.x, topLeft.y + verticalHoldPos), vec2(topLeft.x + barWidth - barPadding * 2.0, topLeft.y + holdHeight + verticalHoldPos), barRadius) == 1) {
            FragColor = moveCategory;
        }
    }
}

vec4 blendPixels(vec4 pixel1, vec4 pixel2) {
    float alpha1 = pixel1.a;
    vec3 color1 = pixel1.rgb;

    float alpha2 = pixel2.a;
    vec3 color2 = pixel2.rgb;

    vec3 blendedColor = (alpha1 * color1) + ((1.0 - alpha1) * color2);

    float blendedAlpha = alpha1 + (1.0 - alpha1) * alpha2;

    return vec4(blendedColor, blendedAlpha);
}

void main() {
    vec4 gradientBackGround = interpolate(darkBackGround, brightBackGround, gl_FragCoord.y / windowSize.y);
    FragColor = interpolate(texture(ourTexture, TexCoord), foreGround, 0.5);
    if (scene == 0) {
        if (inRoundBox(vec2(menuOuterOffset, menuOuterOffset), vec2(windowSize.x - menuOuterOffset, windowSize.y - menuOuterOffset), menuOuterRadius) == 1) {
            FragColor = brightBackGround;
            if (inRoundBox(vec2(menuOuterOffset + menuOuterWidth, menuOuterOffset + menuOuterWidth), vec2(windowSize.x - menuOuterOffset - menuOuterWidth, windowSize.y - menuOuterOffset - menuOuterWidth), menuOuterRadius - menuOuterWidth) == 1) {
                FragColor = texture(ourTexture, TexCoord);
            }
        }
    } else if (scene == 1) {
        if (inRoundBox(vec2(windowSize.x - padding - gameWindowSize.x, windowSize.y - padding - gameWindowSize.y), vec2(windowSize.x - padding, windowSize.y - padding), borderRadius) == 0) {
            FragColor = foreGround;
            //game
        }
        if (inRoundBox(vec2(padding, padding), vec2(padding + elementWindowWidth, windowSize.y - padding), borderRadius) == 1) {
            FragColor = gradientBackGround;
            //elements

            if (displayArea == 3) {
                if (isText == 1) {
                    float relevance = (texture(ourTexture, TexCoord).r + texture(ourTexture, TexCoord).g + texture(ourTexture, TexCoord).b) / 3.0;
                    if (relevance == 0.0) {
                        discard;
                    } else {
                        FragColor = blendPixels(vec4(1.0, 1.0, 1.0, relevance), FragColor);
                    }
                } else if (isText == 2) {
                    float relevance = (texture(ourTexture, TexCoord).r + texture(ourTexture, TexCoord).g + texture(ourTexture, TexCoord).b) / 3.0;
                    float radius = min(blockSize.y, blockSize.x);
                    if (inRoundBox(vec2(blockPos.x, blockPos.y - blockSize.y / 2.0), vec2(blockPos.x + blockSize.x, blockPos.y + blockSize.y / 2.0), radius / 2.0) == 1) {
                        FragColor = blendPixels(vec4(1.0, 1.0, 1.0, relevance), FragColor);
                    } else {
                        discard;
                    }
                } else {
                    if (inElement(blockPos, blockSize, blockColor, borderWidth, 0) == 1) {
                        
                    } else {
                        discard;
                    }
                }
            }

            //bar
            if (gl_FragCoord.x > elementWindowWidth + padding - barWidth) {
                FragColor = gradientBackGround;
            }
        
            if (gl_FragCoord.y < padding + categoryHeight) {
                FragColor = moveCategory;
            }

            drawBar(vec2(elementWindowWidth + padding - barWidth + barPadding, categoryHeight + padding + barPadding), windowSize.y - padding * 2.0 - categoryHeight - barPadding * 2.0, windowSize.y - padding * 2.0 - categoryHeight, elementsListHeight, elementsBarPercent);

            /*if (inRoundBox(vec2(elementWindowWidth + padding - barWidth + barPadding, categoryHeight + padding + barPadding), vec2(elementWindowWidth + padding - barPadding, windowSize.y - padding - barPadding), (barWidth - barPadding * 2.0) / 2.0) == 1) {
                FragColor = foreGround;
                float barHeight = (windowSize.y - padding * 2.0 - categoryHeight) / elementsListHeight;
                float verticalBarPos = 100.0;
                if (inRoundBox(vec2(elementWindowWidth + padding - barWidth + barPadding, categoryHeight + padding + barPadding + verticalBarPos), vec2(elementWindowWidth + padding - barPadding, categoryHeight + padding + barPadding + barHeight * windowSize.y - padding * 2.0 - categoryHeight - barPadding * 2.0 + verticalBarPos), (barWidth - barPadding * 2.0) / 2.0) == 1) {
                    FragColor = currentCategory;
                }
            }*/

        }
        if (inRoundBox(vec2(2.0 * padding + elementWindowWidth, padding), vec2(windowSize.x - 2.0 * padding - gameWindowSize.x, windowSize.y - padding), borderRadius) == 1) {
            FragColor = gradientBackGround;
            //codespace

        }
        if (inRoundBox(vec2(windowSize.x - padding - gameWindowSize.x, padding), vec2(windowSize.x - padding, windowSize.y - gameWindowSize.y - padding * 2.0), borderRadius) == 1) {
            FragColor = gradientBackGround;
            //scenario

        }
    }

    if (displayArea == 1) {
        FragColor = texture(ourTexture, TexCoord);
    }
}