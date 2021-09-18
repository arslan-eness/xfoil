# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 19:31:09 2021

@author: ENES
"""
import os
import subprocess
import matplotlib.pyplot as plt
import random
import numpy as np


class _airfoil():
    def __init__(self,points):
        self.points = points
        self.data = get_xfoil(self.points)
        self.cl=self.data[1]
        self.cd=self.data[2]
        self.cl_cd = self.cl/self.cd
        
        
    def slope_airfoil(self):
        self.slope =np.empty_like(self.points)
        cnt=0
        while cnt<len(self.points)-1:
            self.slope[cnt] = (self.points[cnt+1,1]-self.points[cnt,1])/((self.points[cnt+1,0]-self.points[cnt,0]))
            cnt+=1
        self.slope = np.delete(self.slope,0,1)
        return self.slope
        

def compare_airfoils(airfoil,airfoil_new):
    fig,ax= plt.subplots()
    ax.plot(airfoil.points[:,0],airfoil.points[:,1],"y",linewidth=5)
    ax.plot(airfoil_new.points[:,0],airfoil_new.points[:,1],"r")
        
#crossover
def cross_over(x1,x2):
    f,e   = sorted([random.randint(1,len(x1)),random.randint(1,len(x1))])
    y1 = np.empty_like(x1)
    y2 = np.empty_like(x2)
    
    y1[:f,:] = x1[:f,:]
    y1[f:e,:] = x2[f:e,:]
    y1[e:,:] = x1[e:,:]

    y2[:f,:] = x2[:f,:]
    y2[f:e,:] = x1[f:e,:]
    y2[e:,:] = x2[e:,:]
    
    return y1,y2      
        

def get_xfoil(airfoil):  
    
        
    if os.path.exists("C:/Users/ENES/Desktop/xfoil/new_command.txt"):
          os.remove("C:/Users/ENES/Desktop/xfoil/new_command.txt")
    if os.path.exists("C:/Users/ENES/Desktop/xfoil/newfoil_polar.txt"):
          os.remove("C:/Users/ENES/Desktop/xfoil/newfoil_polar.txt")
    np.savetxt("C:/Users/ENES/Desktop/xfoil/new_airfoil.txt",airfoil,delimiter='\t',fmt="%10.6f")
    airf_command = open("new_command.in", "w")
    airf_command.write("load new_airfoil.txt\n")
    airf_command.write("new_airfoil\n\n")
    airf_command.write("oper\n")
    airf_command.write("visc 1e5\n")
    airf_command.write("pacc\n")
    airf_command.write("newfoil_polar.txt\n\n")
    airf_command.write("iter 100\n")
    airf_command.write("alfa 0\n")
    airf_command.write("\n\n\n")
    airf_command.write("quit\n")
    airf_command.close()
         
    
    try:
        subprocess.run("xfoil.exe < new_command.in",shell=True,check=True,timeout=0.5)
    except subprocess.TimeoutExpired:
        subprocess.run('taskkill /f /im "xfoil.exe"',shell = True)
        
    polar_data = np.loadtxt("C:/Users/ENES/Desktop/xfoil/newfoil_polar.txt",skiprows=12)
    
    if len(polar_data)==0:
        print("polar data is not available")
        polar_data=np.array([0, 0, 0, 0, 0, 0, 0 ])
    else:
        print("data calculated")    
         
    return polar_data
         


def install_nacas():
    points_naca={"n2412":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca2412.txt",skiprows=1),
                 "n2415":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca2415.txt",skiprows=1),
                 "n2418":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca2418.txt",skiprows=1),
                 "n2421":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca2421.txt",skiprows=1),
                 "n4412":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca4412.txt",skiprows=1),
                 "n4415":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca4415.txt",skiprows=1), 
                 "n4418":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca4418.txt",skiprows=1),  
                 "n4421":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca4421.txt",skiprows=1),    
                 "n6412":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca6412.txt",skiprows=1),  
                 "n2424":np.loadtxt("C:/Users/ENES/Desktop/xfoil/first pop/naca2424.txt",skiprows=1)
    
    }
    
    naca_s={"naca2412":_airfoil(points_naca.get("n2412")),
            "naca2415":_airfoil(points_naca.get("n2415")),
            "naca2418":_airfoil(points_naca.get("n2418")),
            "naca2421":_airfoil(points_naca.get("n2421")),
            "naca4412":_airfoil(points_naca.get("n4412")),
            "naca4415":_airfoil(points_naca.get("n4415")),
            "naca4418":_airfoil(points_naca.get("n4418")),
            "naca4421":_airfoil(points_naca.get("n4421")),
            "naca6412":_airfoil(points_naca.get("n6412")),
            "naca2424":_airfoil(points_naca.get("n2424"))
            }

    return naca_s


def first_pop(npop,n_first_parent,child_size):
    naca_s = install_nacas()
    first_pop= {}
    for (i,j) in list(enumerate(naca_s.keys(),start=1)):
        first_pop[i] = naca_s[j]
    n_x2=0
    n_x1=0
    cnt=1
    while True:
        if cnt>=child_size:
            break
        if n_x1 == n_x2:
            (n_x1,n_x2) = (random.randint(1,n_first_parent),random.randint(1,n_first_parent))
        else:
            (x1, x2) = (first_pop[n_x1].points,first_pop[n_x2].points)
            (y1,y2) = cross_over(x1, x2)
            child_1 = _airfoil(y1)
            child_2 = _airfoil(y2)
            first_pop[cnt+n_first_parent] = child_1
            cnt+=1
            first_pop[(cnt)+n_first_parent] = child_2
            cnt+=1
        
    indices=np.empty([len(first_pop),2])
        
    for (i,j) in list(enumerate(first_pop.keys())):
        indices[i,:] =[j,first_pop[j].cl_cd]   
    
    for i in range(len(indices)):
        if np.isnan(indices[i,1]):
             indices[i,1]=-10
    
    sorte_d=indices[np.argsort(indices[:,1])]
    sorte_d =sorte_d[::-1]
    
    #eliminated_ind = sorte_d[npop:,:]
    selected_ind = sorte_d[:npop,:]
    
    #for i,j in eliminated_ind:
        #del first_pop[i]
        
    current_pop = {}    
    for (i,j) in list(enumerate(selected_ind[:,0],start=1)):
        current_pop[i] = first_pop[j]
    print("The best member of 0 pop: Cl={} Cd={} Cl/Cd = {}"
          .format(current_pop[1].cl,current_pop[1].cd,current_pop[1].cl_cd))    
    return current_pop

  
def ga(current_pop,npop,child_size):
    cnt=1
    ind_x2=0
    ind_x1=0
    while True: 
        if cnt >= child_size:
            break
        if ind_x1 == ind_x2:
            (ind_x1 , ind_x2) = (random.randint(1,npop),random.randint(1,npop))
        else:
            (x1, x2) = (current_pop[ind_x1].points,current_pop[ind_x2].points)
            (y1,y2) = cross_over(x1, x2)
            child_1 = _airfoil(y1)
            child_2 = _airfoil(y2)
            current_pop[cnt+npop] = child_1
            cnt+=1
            current_pop[(cnt)+npop] = child_2
            cnt+=1        
    
    indices=np.empty([len(current_pop),2])
    
    
    for (i,j) in list(enumerate(current_pop.keys())):
        indices[i,:] =[j,current_pop[j].cl_cd]
        
        
        
    for i in range(len(indices)):
        if np.isnan(indices[i,1]):
              indices[i,1]=-10
              
    sorte_d=indices[np.argsort(indices[:,1])]
    sorte_d =sorte_d[::-1]          
     
    selected_ind = sorte_d[:npop,:]
    
    
    next_pop = {}
    for (i,j) in list(enumerate(selected_ind[:,0],start=1)):
        next_pop[i] = current_pop[j]
        
    return next_pop
    










# child1=np.empty_like(parent1)

# child1[:f,:]=parent1[:f,:]

# child1[f:e,:]=parent2[f:e,:]

# child1[e:,:]=parent1[e:,:]



    



# airfoil = np.loadtxt("naca2412.txt",skiprows=1)
# airfoil_new=np.empty_like(airfoil)

# #a=random.uniform(-0.1,0.1)

# row=len(airfoil)
# column = len(airfoil[0])

# #for j in list(range(column)):
# for i in list(range(row)):
#     a=random.uniform(-0.005,0.0005)
#     airfoil_new[i,:]=airfoil[i,:]+a
        
# airfoil_new[row-1,:]=airfoil_new[0,:]
# airfoil_new[row-1,1]=-airfoil_new[0,1]
    



    












 