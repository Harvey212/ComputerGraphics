import math
import random
import cv2
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



##################################################
class ray:
    def __init__(self,ori,dirr):
        self.ori=ori #screen source
        self.dir=unitvec(dirr) #the direction from screen source to screen pixel
    def getdir(self):
        return self.dir
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
lightsource=creatvec(-10,10,0)
lightintense=creatvec(1,1,1)
colorlist=[]
colorlist.append(creatvec(0.8,0.3,0.3))
colorlist.append(creatvec(0.3,0.8,0.3))
colorlist.append(creatvec(0.3,0.3,0.8))
colorlist.append(creatvec(0.8,0.8,0.3))
colorlist.append(creatvec(0.3,0.8,0.8))
colorlist.append(creatvec(0.8,0.3,0.8))
colorlist.append(creatvec(0.8,0.8,0.8))
colorlist.append(creatvec(0.3,0.3,0.3))
fresnel=True
max_step=5
##########################################################
class hit_record:
    def __init__(self):
        self.t=0
        self.p=0
        self.nv=0
        self.kd=creatvec(1,1,1)
        self.w_ri=0
        self.w_ti=0
        self.gamma=-1

    def gethit_record(self):
        temp=[]
        temp.append(self.t)
        temp.append(self.p)
        temp.append(self.nv)
        temp.append(self.kd)
        temp.append(self.w_ri)
        temp.append(self.w_ti)
        temp.append(self.gamma)

        return temp

    def adjust_record(self,tt,pp,nvv,kd,w_ri,w_ti,gamma):
        self.t=tt 
        self.p=pp
        self.nv=nvv
        self.kd=kd
        self.w_ri=w_ri
        self.w_ti=w_ti
        self.gamma=gamma


class sphere:
    def __init__(self,center,rad,kd=creatvec(1,1,1),w_ri=0,w_ti=0,gamma=-1):
        self.center=center
        self.rad=rad
        self.kd=kd
        self.w_ri=w_ri
        self.w_ti=w_ti
        self.gamma=gamma

    def hit(self,rayy):
        ori=rayy.getori()
        ocvec=minusvec(ori,self.center)
        CC=dot(ocvec,ocvec)-self.rad**2
        #
        d=rayy.getdir()
        BB=2*dot(d,ocvec)
        #
        AA=1

        judge=False
        t=0
        p=0
        N=0

        delta=BB**2-4*AA*CC

        if delta>=0:
            later=(math.sqrt((delta)))/(2*AA)
            before=-BB/(2*AA)

            t1=before-later
            t2=before+later

            t=t1

            if t>0:
                judge=True
                p=rayy.point_at_parameter(t)
                N=self.calNormalVec(p)

        my_record=hit_record()
        my_record.adjust_record(t,p,N,self.kd,self.w_ri,self.w_ti,self.gamma)

        return judge,my_record

    def calNormalVec(self,p):
        return unitvec(minusvec(p, self.center))

def shading(record,hitable_list):

    hit_record=record.gethit_record()

    p=hit_record[1]
    L=calLightVec(p)

    myray=ray(p,L)

    judge=False
    for k in range(len(hitable_list)):
        if judge==False:
            mysphere=hitable_list[k]
            judge,myrecord=mysphere.hit(myray)

    fin=[]
    if judge==False:
        N=hit_record[2]
        I=creatvec(1,1,1) #light intensity
        kd=hit_record[3]
        vv=vecscale(I,max(0,dot(N,L)))
        fin=calkdvec(kd,vv)


    else:
        fin=creatvec(0,0,0)

    return fin 

def calkdvec(kd,vec):
    xx=vec[0]*kd[0]
    yy=vec[1]*kd[1]
    zz=vec[2]*kd[2]
    temp=[]
    temp.append(xx)
    temp.append(yy)
    temp.append(zz)

    return temp




def calLightVec(p):
    return unitvec(minusvec(lightsource, p))


def background(rayy):
    #for background color
    unit_direction=rayy.getdir()
    t=(unit_direction[1]+1)*0.5

    tem1=vecscale([1,1,1],(1-t))
    tem2=vecscale([0.5,0.7,1],t)
    fin=addvec(tem1,tem2)

    return fin

def calcos(v1,v2):
    v1len=math.sqrt(dot(v1,v1))
    v2len=math.sqrt(dot(v2,v2))
    return dot(v1,v2)/(v1len*v2len)

def trace(rayy,hitable_list,depth):
    fin=[]
    if depth>max_step:
        fin=background(rayy)
    else:
        intersect=-1
        closest=math.inf
        best_record=0
        #hit_reclist=[]

        for i in range(len(hitable_list)):
            mysphere=hitable_list[i]
            judge,myrec=mysphere.hit(rayy)
            if judge==True:
                tt=(myrec.gethit_record())[0]
                if tt<closest:
                    best_record=myrec
                    closest=tt
                    intersect=1

        if intersect!=-1:
            shadecolor=shading(best_record,hitable_list)
            ##############################
            pp=(best_record.gethit_record())[1]
            nn=(best_record.gethit_record())[2]
            rayin=rayy.getdir()
            Rin=vecscale(rayin,-1)
            Rout=minusvec(vecscale(nn,2*dot(nn,Rin)),Rin)
            reflectRay=ray(pp,Rout)
            reflectColor=trace(reflectRay,hitable_list,(depth+1))



            #rayin
            cos=calcos(Rin,nn)



            w_ri=(best_record.gethit_record())[4]
            w_ti=(best_record.gethit_record())[5]
            gammat=(best_record.gethit_record())[6]



            if (fresnel) and (gammat!=-1):
                r0=((gammat-1)/(gammat+1))**2
                rthetha=r0+(1-r0)*math.pow((1-cos),5)
                w_ri=(w_ri+w_ti)*rthetha
                w_ti=(w_ri+w_ti)*(1-rthetha)



            loca=vecscale(shadecolor,(1-w_ri))
            rf=vecscale(reflectColor,w_ri)
            fin=addvec(loca,rf)

            ###########################################
            

            if cos>0:
                #goin
                gamma=1/gammat
            else:
                #goout
                gamma=gammat

            if gamma>0:
                temp1=addvec(rayin,vecscale(nn,cos))
                bef=vecscale(temp1,gamma)

                after=vecscale(nn,math.sqrt((1-gamma*(1-(dot(rayin,nn))**2))))

                refracdir=minusvec(bef,after)

                r3=ray(pp,refracdir)
                refracColor=trace(r3,hitable_list,(depth+1))

                w1=vecscale(fin,(1-w_ti))
                w2=vecscale(refracColor,w_ti)
                fin=addvec(w1,w2)
                
            #################################



        else:
            fin=background(rayy)




    return fin

###############################################################
def generategamma():
    return (random.random()+1)

def main():
    ##############################################################
    f = open(f"test.ppm", "w")
    f.write("P3\n")
    f.write(f"{width} {height}\n255\n")
    ############################################

    hitable_list=[]
    hitable_list.append(sphere(creatvec(0,-100.5,-2),100))
    hitable_list.append(sphere(creatvec(0,0,-2),0.5,creatvec(1,1,1),0,0.9,generategamma()))
    hitable_list.append(sphere(creatvec(1,0,-1.75),0.5,creatvec(1,1,1),0.9,0,generategamma()))
   
    hitable_list.append(sphere(creatvec(-1,0,-2.25),0.5,creatvec(1,0.7,0.3),0,0,generategamma()))

    for i in range(48):
        xr=random.random()*6-3
        zr=random.random()*3-1.5
        cindex=random.randint(0,7)
        rand_reflec=random.random()
        hitable_list.append(sphere(creatvec(xr,-0.4,zr-2),0.1,colorlist[cindex],rand_reflec,0))


    ##############################################
    for j in range(height,0,-1):
        for i in range(width):
            u=float(i/width)
            v=float(j/height)
            tem=addvec(vecscale(horizontal,u),vecscale(vertical,v))
            uvcenter=addvec(lower_left_corner,tem)
            r1=ray(origin,minusvec(uvcenter,origin))
            c1=trace(r1,hitable_list,0)
            printcolor(c1,f)
#############################################
    f.close() 


main()

i = cv2.imread('test.ppm')
cv2.imwrite('test.jpg',i)