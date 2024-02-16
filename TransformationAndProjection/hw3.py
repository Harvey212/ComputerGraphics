import sys, os
from math import pi as PI
from math import sin, cos
import math 


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import glfw
import numpy as np

from PIL import Image



def vec3(xx,yy,zz):
	temp=[]
	temp.append(xx)
	temp.append(yy)
	temp.append(zz)

	return temp

def vec4(xx,yy,zz,dd):
	temp=[]
	temp.append(xx)
	temp.append(yy)
	temp.append(zz)
	temp.append(dd)

	return temp

########################################

class RenderWindow:
	def __init__(self):
		self.STEP2 = True
		self.STEP3 = True

		#########################################################
		glfw.init()
		self.width, self.height = 640, 480
		self.win =glfw.create_window(self.width, self.height, "HW-SWGL-trans", None, None)
		glfw.set_key_callback(self.win, self.on_key)
		glfw.make_context_current(self.win)
		
		glClearColor(0, 0, 0, 0)
		glClearDepth(1.0)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)

		self.exitNow = False
		self.transformMat=np.identity(4)
		self.ViewMat = np.identity(4)
		self.ProjectionMat = np.identity(4)

		self.winWidth = 1280
		self.winHeight = 720
		
		self.tho = 3.14159/4.0
		self.theta = 3.14159/4.0

		self.tetrahedron_verts=[]
		for k in range(4):
			self.tetrahedron_verts.append(vec3(0,0,0))

		self.default_tetrahedron_vertices=[]
		self.default_tetrahedron_vertices.append(vec3(1,0,0))
		self.default_tetrahedron_vertices.append(vec3(0,1,0))
		self.default_tetrahedron_vertices.append(vec3(0,0,1))
		self.default_tetrahedron_vertices.append(vec3(0,0,0))

		self.tetrahedron_verts=self.default_tetrahedron_vertices
		self.addcube=False
		self.addtetra=False
		

	def on_key(self, win, key, scancode, action, mods):
		if action == glfw.PRESS:
			if key == glfw.KEY_ESCAPE:
				self.exitNow = True 

			if (key==glfw.KEY_Q):
				glfw.set_window_title(self.win, "translate +x")
				self.transformMat=np.matmul(self.swTranslate(1, 0, 0), self.transformMat)	

			if (key==glfw.KEY_A):
				glfw.set_window_title(self.win, "translate -x")
				self.transformMat=np.matmul(self.swTranslate(-1, 0, 0), self.transformMat)

			if (key==glfw.KEY_W):
				glfw.set_window_title(self.win, "translate +y")
				self.transformMat=np.matmul(self.swTranslate(0, 1, 0), self.transformMat)

			if (key==glfw.KEY_S):
				glfw.set_window_title(self.win, "translate -y")
				self.transformMat=np.matmul(self.swTranslate(0, -1, 0), self.transformMat)

			if (key==glfw.KEY_E):
				glfw.set_window_title(self.win, "translate +z")
				self.transformMat=np.matmul(self.swTranslate(0, 0, 1), self.transformMat)

			if (key==glfw.KEY_D):
				glfw.set_window_title(self.win, "translate -z")
				self.transformMat=np.matmul(self.swTranslate(0, 0, -1), self.transformMat)

			if (key==glfw.KEY_R):
				glfw.set_window_title(self.win, "rotate +x")
				self.transformMat=np.matmul(self.swRotateX(self.tho), self.transformMat)	

			if (key==glfw.KEY_F):
				glfw.set_window_title(self.win, "rotate -x")
				self.transformMat=np.matmul(self.swRotateX(-self.tho), self.transformMat)

			if (key==glfw.KEY_T):
				glfw.set_window_title(self.win, "rotate +y")
				self.transformMat=np.matmul(self.swRotateY(self.tho), self.transformMat)

			if (key==glfw.KEY_G):
				glfw.set_window_title(self.win, "rotate -y")
				self.transformMat=np.matmul(self.swRotateY(-self.tho), self.transformMat)

			if (key==glfw.KEY_Y):
				glfw.set_window_title(self.win, "rotate +z")
				self.transformMat=np.matmul(self.swRotateZ(self.tho), self.transformMat)

			if (key==glfw.KEY_H):
				glfw.set_window_title(self.win, "rotate -z")
				self.transformMat=np.matmul(self.swRotateZ(-self.tho), self.transformMat)

			if (key==glfw.KEY_U):
				glfw.set_window_title(self.win, "scale +x")
				self.transformMat=np.matmul(self.swScale(2,1,1), self.transformMat)

			if (key==glfw.KEY_J):
				glfw.set_window_title(self.win, "scale -x")
				self.transformMat=np.matmul(self.swScale(1/2,1,1), self.transformMat)

			if (key==glfw.KEY_I):
				glfw.set_window_title(self.win, "scale +y")
				self.transformMat=np.matmul(self.swScale(1,2,1), self.transformMat)

			if (key==glfw.KEY_K):
				glfw.set_window_title(self.win, "scale -y")
				self.transformMat=np.matmul(self.swScale(1,1/2,1), self.transformMat)

			if (key==glfw.KEY_O):
				glfw.set_window_title(self.win, "scale +z")
				self.transformMat=np.matmul(self.swScale(1,1,2), self.transformMat)

			if (key==glfw.KEY_L):
				glfw.set_window_title(self.win, "scale -z")
				self.transformMat=np.matmul(self.swScale(1,1,1/2), self.transformMat)
				
			#####################################################
			if (key==glfw.KEY_F1): #you have to press fn and f1 at the same time
				glfw.set_window_title(self.win, "F1: add a tetrahedron")
				self.addtetra=True

			if (key==glfw.KEY_F2):
				glfw.set_window_title(self.win, "F2: add a cube or somthing")
				self.addcube=True

			if (key==glfw.KEY_9):
				self.theta+=3.14159/90

			if (key==glfw.KEY_0):
				self.theta+=(-3.14159/90)

			if (key==glfw.KEY_MINUS):
				self.transformMat=np.identity(4)

			#############################################################

			if (key==glfw.KEY_F5):
				glfw.set_window_title(self.win, "F5: SAVE")
				self.ScreenShot()

			if (key==glfw.KEY_F6):
				glfw.set_window_title(self.win, "F6: LOAD")
				#load scene

			

	def normal(self,vv):
		norm=math.sqrt((vv[0])**2+(vv[1])**2+(vv[2])**2)
		fin=np.true_divide(vv, norm)
		
		return fin


	def swScale(self,x,y,z):
		Scale = np.identity(4)
		Scale[0][0]=x
		Scale[1][1]=y
		Scale[2][2]=z

		return Scale

	def swRotate(self,angle,x,y,z):
		Rotate = np.identity(4)
		Rotate[0][0]=cos(angle)+pow(x,2)*(1-cos(angle))
		Rotate[0][1]=x*y*(1-cos(angle))-z*sin(angle)
		Rotate[0][2]=x*z*(1-cos(angle))+y*sin(angle)
		Rotate[1][0]=y*x*(1-cos(angle))+z*sin(angle)
		Rotate[1][1]=cos(angle)+pow(y,2)*(1-cos(angle))
		Rotate[1][2]=y*z*(1-cos(angle))-x*sin(angle)
		
		Rotate[2][0]=z*x*(1-cos(angle))-y*sin(angle)
		Rotate[2][1]=z*y*(1-cos(angle))+x*sin(angle)
		Rotate[2][2]=cos(angle)+pow(z,2)*(1-cos(angle))
		

		return Rotate

	def swRotateZ(self,angle):
		Rotate = np.identity(4)
		Rotate[0][0]=cos(angle)
		Rotate[0][1]=-sin(angle)
		Rotate[1][0]=sin(angle)
		Rotate[1][1]=cos(angle)

		return Rotate

	def swRotateY(self,angle):
		Rotate = np.identity(4)

		Rotate[0][0]=cos(angle)
		Rotate[0][2]=sin(angle)
		Rotate[2][0]=-sin(angle)
		Rotate[2][2]=cos(angle)

		return Rotate

	def swRotateX(self,angle):
		Rotate = np.identity(4)
		Rotate[1][1]=cos(angle)
		Rotate[1][2]=-sin(angle)
		Rotate[2][1]=sin(angle)
		Rotate[2][2]=cos(angle)


		return Rotate

	def swTranslate(self,x,y,z):
		Translate = np.identity(4)
		#Translate[3][0] = x
		#//todo: y z
		Translate[0][3] = x
		Translate[1][3] = y
		Translate[2][3] = z

		return Translate


	def drawgrid(self):
		size=10
		glBegin(GL_LINES)

		glColor3f(0.3, 0.3, 0.3)
		for i in range(1,10):
			
			self.drawp(i,-size,0)
			self.drawp(i,size,0)
			self.drawp(-i, -size, 0)
			self.drawp(-i, size, 0)

			self.drawp(-size, i, 0)
			self.drawp(size, i, 0)
			self.drawp(-size, -i, 0)
			self.drawp(size, -i, 0)
		
		glEnd()

		glBegin(GL_LINES)
		glColor3f(1, 0, 0)
		self.drawp(0, 0, 0)
		self.drawp(size, 0, 0)
		
		glColor3f(0.4, 0, 0)
		self.drawp(0, 0, 0)
		self.drawp(-size, 0, 0)
		

		glColor3f(0, 1, 0)
		self.drawp(0, 0, 0)
		self.drawp(0, size, 0)

		glColor3f(0, 0.4, 0)
		self.drawp(0, 0, 0)
		self.drawp(0, -size, 0)

		glColor3f(0, 0, 1)
		self.drawp(0, 0, 0)
		self.drawp(0, 0, size)

		glEnd()

	def drawp(self,p1,p2,p3):
		#self.ProjectionMat
		#np.array([p1, p2, p3, 1])
		#self.ViewMat

		tt=np.matmul(self.ProjectionMat,self.ViewMat)
		tt=np.matmul(tt,np.array([p1, p2, p3, 1])).transpose()
		glVertex3f(tt[0],tt[1],tt[2])

	def Draw_Tetrahedron(self):
		#vec3 color(1, 1, 0)
		#glColor3f(1, 1, 0)
		glBegin(GL_TRIANGLES)

		self.swTriangle(vec3(1, 0, 0), self.tetrahedron_verts[0], self.tetrahedron_verts[1], self.tetrahedron_verts[2], self.transformMat)
		self.swTriangle(vec3(0, 0, 1), self.tetrahedron_verts[3], self.tetrahedron_verts[0], self.tetrahedron_verts[1], self.transformMat)
		self.swTriangle(vec3(0, 1, 0), self.tetrahedron_verts[2], self.tetrahedron_verts[3], self.tetrahedron_verts[0], self.transformMat)
		self.swTriangle(vec3(1, 1, 0), self.tetrahedron_verts[1], self.tetrahedron_verts[2], self.tetrahedron_verts[3], self.transformMat)

		glEnd()


	def addtetrahedron(self):
		#(1,0,0)
		#(0,1,0)
		#(0,0,1)
		#(0,0,0)
		glBegin(GL_TRIANGLES)
		glColor3f(1, 0, 0)
		glVertex3f(1,0,0)
		glVertex3f(0,1,0)
		glVertex3f(0,0,0)

		glColor3f(0, 0, 1)
		glVertex3f(0,0,0)
		glVertex3f(1,0,0)
		glVertex3f(0,1,0)

		glColor3f(0, 1, 0)
		glVertex3f(0,0,1)
		glVertex3f(0,0,0)
		glVertex3f(1,0,0)

		glColor3f(1, 1, 0)
		glVertex3f(0,1,0)
		glVertex3f(0,0,1)
		glVertex3f(0,0,0)

		glEnd()




	def drawcube(self):
		glBegin(GL_QUADS);
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(-0.5, -0.5, 0.5)
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f( 0.5, -0.5, 0.5)
		glVertex3f( 0.5, 0.5, 0.5)
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(-0.5, 0.5, 0.5)

		glVertex3f(-0.5, -0.5, -0.5)
		glVertex3f(-0.5, 0.5, -0.5)
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f( 0.5, 0.5, -0.5)
		glVertex3f( 0.5, -0.5, -0.5)

		glColor3f(0.0, 1.0, 0.0)
		glVertex3f(-0.5, -0.5, 0.5)
		glVertex3f(-0.5, 0.5, 0.5)
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f(-0.5, 0.5, -0.5)
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(-0.5, -0.5, -0.5)
	
		glVertex3f( 0.5, -0.5, -0.5)
		glVertex3f( 0.5, 0.5, -0.5)
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f( 0.5, 0.5, 0.5)
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f( 0.5, -0.5, 0.5)

		glColor3f(0.0, 0.0, 1.0)
		glVertex3f(-0.5, 0.5, 0.5)
		glVertex3f( 0.5, 0.5, 0.5)
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f( 0.5, 0.5, -0.5)
		glVertex3f(-0.5, 0.5, -0.5)
		
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(-0.5, -0.5, 0.5)
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f(-0.5, -0.5, -0.5)
		glVertex3f( 0.5, -0.5, -0.5)
		glVertex3f( 0.5, -0.5, 0.5)
		glEnd()



	def swTriangle(self,color,in_v1,in_v2,in_v3,Modelmatrix):
		
		v1=vec4(in_v1[0], in_v1[1], in_v1[2], 1)
		v2=vec4(in_v2[0], in_v2[1], in_v2[2], 1)
		v3=vec4(in_v3[0], in_v3[1], in_v3[2], 1)

		##########################################
		v1 = np.matmul(Modelmatrix,np.array(v1))
		v2 = np.matmul(Modelmatrix,np.array(v2))
		v3 = np.matmul(Modelmatrix,np.array(v3))

		#step2: remove glLookAt, compute view matrix
		v1 = np.matmul(self.ViewMat,v1)
		v2 = np.matmul(self.ViewMat,v2)
		v3 = np.matmul(self.ViewMat,v3)

		#step3: remove glProjection, compute project matrix
		#v1 =  Projection * View * Modelmatrix * v1;
		#prespective division
		v1=np.matmul(self.ProjectionMat,v1).transpose()
		v2=np.matmul(self.ProjectionMat,v2).transpose()
		v3=np.matmul(self.ProjectionMat,v3).transpose()
		##########################################
		

		glColor3f(color[0], color[1], color[2])
		glVertex3f(v1[0], v1[1], v1[2])
		glVertex3f(v2[0], v2[1], v2[2])
		glVertex3f(v3[0], v3[1], v3[2])


	def swLookAt(self,eyex,eyey,eyez,atx,aty,atz,upx,upy,upz):

		fx=atx-eyex
		fy=aty-eyey
		fz=atz-eyez

		f=[]
		f.append(fx)
		f.append(fy)
		f.append(fz)

		f=np.array(f)

		f=self.normal(f)

		up=[]
		up.append(upx)
		up.append(upy)
		up.append(upz)

		up=np.array(up)

		up=self.normal(up)

		s=np.cross(f, up)

		s=self.normal(s)
		u=np.cross(s, f)

		M=np.identity(4)
		T=np.identity(4)

		M[0][0]=s[0]
		M[0][1]=s[1]
		M[0][2]=s[2]

		M[1][0]=u[0]
		M[1][1]=u[1]
		M[1][2]=u[2]

		M[2][0]=-f[0]
		M[2][1]=-f[1]
		M[2][2]=-f[2]

		T[0][3]=-eyex
		T[1][3]=-eyey
		T[2][3]=-eyez

		mylookat=np.matmul(M,T).transpose()

		return mylookat

	

	def run(self):
		t = 0.0
		while not glfw.window_should_close(self.win) and not self.exitNow:
			currT = GLUT.glutGet(GLUT_ELAPSED_TIME)

			if currT - t > 0.1:
				t = currT
				self.display()
				glfw.swap_buffers(self.win)
				glfw.poll_events()


		glfw.terminate()


	def cot(self,x):
		w1=sin(x)
		w2=cos(x)

		return (w2/w1)

	def tan(self,x):
		w1=sin(x)
		w2=cos(x)

		return (w1/w2) 


	def swPerspective(self,fovy,aspect,near,far):
		per=np.zeros((4,4))

		#fovx=2*math.atan((aspect*self.tan(fovy/2)))
		f=math.tan(math.radians(fovy)/2)

		per[0][0]=1/(f*aspect)
		per[1][1]=1/f
		per[2][2]=(near+far)/(near-far)
		per[2][3]=(2*near*far)/(near-far)
		per[3][2]=-1

		per=per.transpose()
		
		return per


	def addnew(self):
		if self.addcube:
			self.drawcube()
			
		if self.addtetra:
			self.addtetrahedron()

	def ScreenShot(self):
		glReadBuffer(GL_FRONT)
		pixels = glReadPixels(0,0,self.width,self.height,GL_RGB,GL_UNSIGNED_BYTE)
		#print(pixels)
		image = Image.frombytes("RGB", (self.width,self.height), pixels)
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		image.save("mypic.jpg")




	def display(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if self.STEP2:
			glMatrixMode(GL_MODELVIEW)
			glLoadMatrixf(self.swLookAt(10 * cos(self.theta), -10 * sin(self.theta), 10, 0, 0, 0, 0, 0, 1)) 
			####################
			#glLoadIdentity()
			#gluLookAt(10*cos(self.theta), -10*sin(self.theta), 10, 0, 0, 0, 0, 0, 1)
			######################
			#self.ViewMat=self.swLookAt(10 * cos(self.theta), -10 * sin(self.theta), 10, 0, 0, 0, 0, 0, 1)

		if self.STEP3:
			glMatrixMode(GL_PROJECTION)
			glLoadMatrixf(self.swPerspective(60, 1, 0.1, 50))
			##################### 
			#glLoadIdentity()
			#glOrtho(0, self.winWidth, 0, self.winHeight, -2.0, 2.0)
			#gluPerspective(60, 1, 0.1, 50)
			################	
			#self.ProjectionMat=self.swPerspective(60, 1, 0.1, 50)	


		self.drawgrid()
		self.Draw_Tetrahedron()
		self.addnew()


def main():
	rw = RenderWindow()
	rw.run()
if __name__ == "__main__":
	print('Press Esc: exit')
	print('Press Q: translate +x')
	print('Press A: translate -x')
	print('Press W: translate +y')
	print('Press S: translate -y')
	print('Press E: translate +z')
	print('Press D: translate -z')
	print('Press R: rotate +x')
	print('Press F: rotate -x')
	print('Press T: rotate +y')
	print('Press G: rotate -y')
	print('Press Y: rotate +z')
	print('Press H: rotate -z')
	print('Press U: scale +x')
	print('Press J: scale -x')
	print('Press I: scale +y')
	print('Press K: scale -y')
	print('Press O: scale +z')
	print('Press L: scale -z')
	print('Press F1: add a tetrahedron')
	print('Press F2: add a cube or somthing')
	print('Press 9: theta+=3.14159/90')
	print('Press 0: theta+=-3.14159/90')
	print('Press -: reset transformation')
	print('Press F5: save image')
	main()