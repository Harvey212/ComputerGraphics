import math
####################################################
width = 200
height = 100
##################################################
#tool
#create vector
def creatvec(x,y,z):
    vec=[]
    vec.append(x)
    vec.append(y)
    vec.append(z)
    return vec
#create unit vector
def unitvec(vec):
    tem=(vec[0])**2+(vec[1])**2+(vec[2])**2
    norm=math.sqrt(tem)
    return vecscale(vec,1/norm)
#scale the vector
def vecscale(vec,scale):
    return [x*scale for x in vec]
#add 2 vector
def addvec(v1,v2):
    return [a+b for a,b in zip(v1, v2)]
#minus 2 vector
def minusvec(v1,v2):
    return [a-b for a, b in zip(v1, v2)]
#vector dot product
def dot(v1,v2):
    return sum([a*b for a,b in zip(v1, v2)])
#print color
def printcolor(colour,f):
    R=int(colour[0]*255)
    G=int(colour[1]*255)
    B=int(colour[2]*255)

    f.write(f"{R} {G} {B}\n")

def openfile(name):
    f = open(f"{name}.ppm", "w")
    f.write("P3\n")
    f.write(f"{width} {height}\n255\n")

    return f

##################################################
class ray:
    def __init__(self,ori,dirr):
        self.ori=ori #screen source
        self.dir=dirr #the direction from screen source to screen pixel
    def getdir(self):
        return unitvec(self.dir)
    def getori(self):
        return self.ori
    #to calculate where the ray could reach given variable t 
    #p=self.ori+t*vec(self.dir)
    def point_at_parameter(self,t): 
        return addvec(self.ori,vecscale(self.dir,t))

######################################################
#basic setting
origin=creatvec(0,0,0) #screen source
lower_left_corner=creatvec(-2,-1,-1) #left screen corner
horizontal=creatvec(4,0,0) #screen horizontal vector
vertical=creatvec(0,2,0) #screen vertical vector

#ball setting
center=creatvec(0,0,-1)
rad=0.5

center2=creatvec(1,0,-1)
rad2=0.3
##########################################################
#calculate normal vector
#it is the vector between ball center and the point where "the" ray touch the surface of the ball 
def calNormalVec(rayy,tt):
    return unitvec(minusvec(rayy.point_at_parameter(tt), center))

def calNormalVec2(rayy,tt):
    return unitvec(minusvec(rayy.point_at_parameter(tt), center2))
#calculate the vector between light source and the point where "the" ray touch the surface of the ball 
def calLightVec(rayy,tt,source):
    return unitvec(minusvec(source, rayy.point_at_parameter(tt)))


###############################################################
#color model
def colormodel1():
    return creatvec(1,0,0)

def colormodel2(rayy,tt):
    N=calNormalVec(rayy,tt)
    return creatvec((N[0]+1)*0.5,(N[1]+1)*0.5,(N[2]+1)*0.5)

def colormodel3(rayy,tt,source):
    L=calLightVec(rayy,tt,source)
    N=calNormalVec(rayy,tt)
    I=creatvec(1,1,1) #light intensity
    return vecscale(I,max(0,dot(N,L)))

def colorbonus():
    return creatvec(1,0,0)

def background(rayy):
    #for background color
    unit_direction=rayy.getdir()
    t=(unit_direction[1]+1)*0.5

    tem1=vecscale([1,1,1],(1-t))
    tem2=vecscale([0.5,0.7,1],t)
    fin=addvec(tem1,tem2)

    return fin
################################################################
def hit_sphere(rayy):
    #
    ocvec=minusvec(origin,center)
    CC=dot(ocvec,ocvec)-rad**2
    #
    d=rayy.getdir()
    BB=2*dot(d,ocvec)
    #
    AA=1

    judge=False
    t=0

    delta=BB**2-4*AA*CC

    if delta>=0:
        later=(math.sqrt((delta)))/(2*AA)
        before=-BB/(2*AA)

        t1=before-later
        t2=before+later

        t=t1

        if t>0:
            judge=True

    return judge, t
######################################################
def hit_sphere2(rayy):
    #
    ocvec=minusvec(origin,center2)
    CC=dot(ocvec,ocvec)-rad2**2
    #
    d=rayy.getdir()
    BB=2*dot(d,ocvec)
    #
    AA=1

    judge=False
    t=0

    delta=BB**2-4*AA*CC

    if delta>=0:
        later=(math.sqrt((delta)))/(2*AA)
        before=-BB/(2*AA)

        t1=before-later
        t2=before+later

        t=t1

        if t>0:
            judge=True

    return judge, t

#####################################################
def color(rayy,model):
    if model!='bonus':
        if model=='skybox':
            fin=background(rayy)
        else:
            #to see if ray hit sphere
            judge, tt=hit_sphere(rayy)
            if judge:
                ##if hit, decide which color
                if model=='red':
                    fin=colormodel1()

                if model=='normal':
                    fin=colormodel2(rayy,tt)

                if model=='shadingLeft':
                    source=creatvec(-1,1,0) #light source
                    fin=colormodel3(rayy,tt,source)

                if model=='shadingMiddle':
                    source=creatvec(0,0,0)
                    fin=colormodel3(rayy,tt,source)

                if model=='shadingRight':
                    source=creatvec(1,1,0)
                    fin=colormodel3(rayy,tt,source)
            else:
                #for background color
                fin=background(rayy)
    else:
        judge, tt=hit_sphere(rayy)
        judge2, tt2=hit_sphere2(rayy)
        if (judge==False) and (judge2==False):
            fin=background(rayy)
        else:
            source=creatvec(0,0,0) #light source
            if judge==True:
                fin=colormodel3(rayy,tt,source)
            else:
                fin=colorbonus()
    return fin


##############################################################
#to decide every pixel of the screen
def mywindow(f,model):
    for j in range(height,0,-1):
        for i in range(width):
            u=float(i/width)
            v=float(j/height)
            tem=addvec(vecscale(horizontal,u),vecscale(vertical,v))
            uvcenter=addvec(lower_left_corner,tem)
            r1=ray(origin,minusvec(uvcenter,origin))
            c1=color(r1,model)
            printcolor(c1,f)
    
    f.close()
    print(f"{model} is generated.\n")     

def main():
    models=['skybox','red','normal','shadingLeft','shadingMiddle','shadingRight','bonus']

    for k in range(len(models)):
        model=models[k]
        f=openfile(model)
        mywindow(f,model)

main()