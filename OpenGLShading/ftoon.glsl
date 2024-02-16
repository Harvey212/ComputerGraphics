#version 330

in vec4 color;
in vec4 normal;
in mat4 viewMatrix;
in vec3 posInView;

uniform vec3 u_lightDir;

out vec4 frag_color;

void main () {
	
	vec3 N;
	vec3 L;
	vec3 toon;
	float intensity;
	float threshold1;
	float threshold2;
	float threshold3;
	float decay_coefficient1;
	float decay_coefficient2;
	float decay_coefficient3;

	threshold1=0.7;
	threshold2=0.5;
	threshold3=0.2;
	decay_coefficient1=0.9;
	decay_coefficient2=0.7;
	decay_coefficient3=0.4;

	L=normalize(vec3(u_lightDir[0],u_lightDir[1],u_lightDir[2]));
	N=normalize(vec3(normal[0],normal[1],normal[2]));

	intensity=dot(L,N);

	if(intensity>threshold1)
	{	
		toon=vec3(color[0],color[1],color[2]);
	}else if(intensity>threshold2)
	{
		toon=vec3(color[0]*decay_coefficient1,color[1]*decay_coefficient1,color[2]*decay_coefficient1);
	}else if(intensity>threshold3)
	{
		toon=vec3(color[0]*decay_coefficient2,color[1]*decay_coefficient2,color[2]*decay_coefficient2);
	}else{
		toon=vec3(color[0]*decay_coefficient3,color[1]*decay_coefficient3,color[2]*decay_coefficient3);
	}

	
	
	frag_color=vec4(toon,1.0);
}
