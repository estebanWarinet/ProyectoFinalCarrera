# -*- coding: utf-8 -*-
import numpy as np
import math
import csv
    
def mapp(X,q,p):
    # System of non-linear equations that maintains the divergence-free condition
    # Sitema de ecuaciones no lineales que mantienen la condicion de libre divergencia
    # |p_x p_y p_z| |k_x|   |0|
    # |q_x q_y q_z| |k_y| = |0|
    # |k_x k_y k_z| |k_z|   |1|
    # X vector columna, q y p Vectores filas
    fx=np.zeros((3,1))
    fx[0,0]=1
    K=np.zeros((3,3))
    K[0,:]=X[:]
    K[1,:]=q[:]
    K[2,:]=p[:]
    F=fx.transpose()-np.dot(K,X)
    return F.transpose()

def RandSampleSphere(N):
    # Esta funcion genera cordenadas uniformemente distribuidas
    # de forma aleatoria dentro de una esfera de radio unitario, 
    # tiene como fin mantener la condicion de libre divergencia.
    # Satisface la ecuacion 3 del paper de Aboshosha
    np.random.seed(None) # Para inicializar los ramdom con el tiempo
    t0z=2*math.pi*np.random.rand(N,1) # vector de numeros aleatorio de N filas por 1 columna
    z=np.sin(t0z)
    t=2*math.pi*np.random.rand(N,1)# vector de numeros aleatorio de N filas por 1 columna
    r=np.sqrt(1-np.power(z,2))
    x=r*np.cos(t)
    y=r*np.sin(t)
    XYZ=np.zeros((N,3))
    XYZ[:,0]=x[:,0]
    XYZ[:,1]=y[:,0]
    XYZ[:,2]=z[:,0]
    return XYZ