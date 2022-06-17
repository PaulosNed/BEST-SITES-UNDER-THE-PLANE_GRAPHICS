# version 330 core

in vec2 outTexCoord;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, outTexCoord);
}
