#version 330

in vec4 color;
in vec4 normal;
in vec3 vertexPos;
in mat4 viewMatrix;

uniform vec3 u_lightDir;
uniform vec3 KS;

out vec4 frag_color;

void main () {
	vec3 N;
	vec3 L;
	vec3 V;
	vec3 la;
	vec3 ld;
	vec3 ls;
	vec3 h;
	vec3 diff;
	vec3 amb;
	vec3 spec;
	vec3 fin;
	float pro;
	float mymax;
	float kdr;
	float kdg;
	float kdb;
	float kar;
	float kag;
	float kab;
	float ksr;
	float ksg;
	float ksb;
	////////////////////////////////////////////
	la=vec3(1,1,1);
	//la=normalize(la);

	kar=color[0]*0.1;
	kag=color[1]*0.1;
	kab=color[2]*0.1;
	amb=vec3(la[0]*kar,la[1]*kag,la[2]*kab);
	///////////////////////////////////////////
	kdr=color[0];
	kdg=color[1];
	kdb=color[2];

	ld=vec3(1,1,1);
	//ld=normalize(ld);
	
	L=normalize(vec3(u_lightDir[0],u_lightDir[1],u_lightDir[2]));
	N=normalize(vec3(normal[0],normal[1],normal[2]));

	if (dot(L,N)>0)
	{
		mymax=dot(L,N);
	}else
	{
		mymax=0;
	}
	
	diff=vec3(ld[0]*mymax*kdr,ld[1]*mymax*kdg,ld[2]*mymax*kdb);
	/////////////////////////////////////////////////////////
	ksr=color[0]*KS[0];
	ksg=color[1]*KS[1];
	ksb=color[2]*KS[2];

	ls=vec3(1,1,1);
	//ls=normalize(ls);

	V=normalize(vec3(0-vertexPos[0],0-vertexPos[1],0-vertexPos[2]));

	h=normalize(vec3(V[0]+L[0],V[1]+L[1],V[2]+L[2]));
	pro=dot(N,h);
	
	spec=vec3(ls[0]*pro*ksr,ls[1]*pro*ksg,ls[2]*pro*ksb);
	////////////////////////////////////////////////////////////
	
	fin=diff+spec+amb;
	frag_color = vec4(fin,1.0);

	
}
