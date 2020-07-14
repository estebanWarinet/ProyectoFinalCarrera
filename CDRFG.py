import numpy as np
import math
import csv

from scipy import signal
import matplotlib.pyplot as plt


########################################################

def RandSampleSphere(N):
    # Esta funcion genera cordenadas uniformemente distribuidas
    # de forma aleatoria dentro de una esfera de radio unitario, 
    # tiene como fin mantener la condicion de libre divergencia.
    # Satisface la ecuacion 3 del paper de Aboshosha
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


def CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Lwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,X,Y,Z):

    # Consistent DRFG Function By Aboshosha et al. (2015)
    # INPUT Parameters
    # h0u Reference height for the mean velocity
    # Uh Mean velocity at h0u
    # alphau Power low exponent of the mean velocity
    # h0I Reference height for the turbulent intensity
    # Iuh Longitudinal turbulent intensity at h0I
    # Ivh Transverse turbulent intensity at h0I
    # Iwh Vertical turbulent intensity at h0I
    # dIu Power low exponent of the longitudinal turbulent intensity
    # dIv Power low exponent of the longitudinal turbulent intensity
    # dIw Power low exponent of the longitudinal turbulent intensity
    # h0L Reference height for the length scale
    # Luh Longitudinal length scale at h0L
    # Lvh Transverse length scale at h0L
    # Lwh Vertical length scale at h0L
    # dLu Power low exponent of the longitudinal length scale
    # dLv Power low exponent of the longitudinal length scale
    # dLw Power low exponent of the longitudinal length scale
    # Cxyz Coherency decay constants in x, y and z directions [1  3] matrix
    # DGamma Characteristic length used to maintain the coherency
    # nf Number of random frequencies in one segment
    # nm Number of frequency segments
    # fmax Maximum frequency
    # dt Time step
    # nt Number of time steps
    # M Matrix of the inflow coordinates [x y z]

    # OUTPUT Parameters
    # Three files (i.e. inletdata_U, inletdata_V and inletdata_W) that have the
    # generated velocity - compatible with STAR CCM+
    
    ##==========================================================================
    ##================== Inicializaci�n de variables ===========================
    ##==========================================================================
    
    ## Extraccion de las coordenadas. En el caso Ejemplo X e Y son 0
    #X=M[:,0]
    #Y=M[:,1] 
    #Z=M[:,2] # x and y coordinates vector at the inflow plane

    nd=Z.shape[0] # Generar numero de puntos. Termina siendo el numero de filas de M
    
    ## Infomacion de la frecuencia
    # nm es el numero de segmentos de frecuencia
    fmin=(fmax/nm)/2 # Frecuencia Minima Averiguar porque se calcula asi
    df=(fmax-fmin)/(nm-1) # Paso de frecuencia
    fm=np.arange(fmin,fmax+df,df) # Vector de frecuencia

    ## Informacion temporal
    lim_tt=(nt*dt)-dt # Limite de tiempo
    tt=np.arange(0,lim_tt+dt,dt) # Vector de tiempo
    
    ## Abrir los archivos y acomodarlos de la forma que se requiere para STAR CCM+
    fid2 = open('TablaVelocidades.csv','w')
    #Escribo las cabezeras de los archivos (primer fila)
    csvHead='X,Y,Z,'
    fid2.write(csvHead)

    for i in range(tt.shape[0]):
        cadena='ux(m/s)[t='+str(tt[i])+'], '+'vx(m/s)[t='+str(tt[i])+'], '+'wx(m/s)[t='+str(tt[i])+'], '
        fid2.write(cadena)


    ## Calcular la velocidad promedio dado que
    # Uh es la velocidad promedio a una altura de referencia
    # h0u es la altura de referencia
    # Z es la altura del inlet
    # alphau es un exponente de la velocidad media
    Uav=Uh*np.power(Z/h0u,alphau)
    
    ## Intensidad de la turbulencia donde
    #h0I es la altura de referencia para la intesidad
    #Iuh,Ivh, Iwh son las intensidades longitudinal, transversal
    # y vertical de turbulencia a la altura H0I respectivamente.
    # dIu, dIv, dIw exponentes de intesidad longitudinal, transversal y vertical
    Iu=Iuh*np.power(Z/h0I,dIu) 
    Iv=Ivh*np.power(Z/h0I,dIv)
    Iw=Iwh*np.power(Z/h0I,dIw)
    
    ## Perfiles de escala de longitud
    # h0L es la altura de referencia para la escala de longitud
    # Luh, Lvh, Lwh son las escalas de longitud en direccion
    # longitudinal, transversal y vertical a una altura  h0L
    # dLu, dLv, dLw exponentes de intesidad longitudinal, transversal y vertical
    Lu=Luh*np.power(Z/h0L,dLu) 
    Lv=Lvh*np.power(Z/h0L,dLv)
    Lw=Lwh*np.power(Z/h0L,dLw) 
        
    ## Generate Wn (nf x nm) matrix, wn has 2.pi.fm mean and rms=2.pi.df
    # Para el paso 1 de la corrección. e obtiene una expresión para la función de coherencia 
    # resultante de la técnica DRFG (ecuación (1)) que utiliza la nueva definición de L mj (ecuación (7)).
    # Genera una matriz de nf x nm con media 0 y desviacion estandar 1
    # Se generan los elementos para el calculo de los campos de velocidad, vendria a ser el
    # 2*pi*f_m,n dentro de los cosenos y senos. Es el paso de frecuencia. No se que es rms
    # nm es el numero de segmentos de frecuencia, nf Número de frecuencias aleatorias en un segmento.
    wn=np.random.randn(nf,nm)*2*np.pi*df
    for nmi in range(nm):
        wn[:,nmi]=wn[:,nmi]-np.mean(wn[:,nmi])
        wn[:,nmi]=wn[:,nmi]/np.std(wn[:,nmi])*2*np.pi*df
        wn[:,nmi]=wn[:,nmi]+fm[nmi]*2*np.pi


    ##==========================================================================
    ## Creo las matrices del espectro
    # nm es el numero de segmentos, nd cantidad de puntos
    Su=np.zeros((nm,nd))
    Sv=np.zeros((nm,nd))
    Sw=np.zeros((nm,nd))
    
    ## Investigar de donde salen estos numeros    
    fms=np.arange(-0.5,0.5+0.05,0.05)*df
    nfsm=fms.shape[0]/2+0.5 
    nfs=fms.shape[0] 
    
    ## Espectros de la turbulencia según los define Von Karma
    # fm vector de frecuencias
    # Uav Vetor de velocidad promedio a diferentes alturas
    # Iu, Iv, Iw son las intensidades longitudinal, transversal y vertical
    # Lu, Lv, Lw son los perfiles escalas de longitud en direccion
    for i in range(nd):
        for j in range (nm):
            fmjs=fm[j]+fms
            if (j==1):
                fmjs=fm[j]+fms[int(nfsm):int(nfs)]
            Su[j,i]=np.mean(4*((Iu[i]*Uav[i])**2)*(Lu[i]/Uav[i])/np.power(1+70.8*np.power(fmjs*Lu[i]/Uav[i],2),(5/6))) #Revisar division
            Sv[j,i]=np.mean(4*((Iv[i]*Uav[i])**2)*(Lv[i]/Uav[i])*(1+188.4*np.power(2*fmjs*Lv[i]/Uav[i],2))/np.power(1+70.8*np.power(2*fmjs*Lv[i]/Uav[i],2),(11/6)))
            Sw[j,i]=np.mean(4*((Iw[i]*Uav[i])**2)*(Lw[i]/Uav[i])*(1+188.4*np.power(2*fmjs*Lw[i]/Uav[i],2))/np.power(1+70.8*np.power(2*fmjs*Lw[i]/Uav[i],2),(11/6)))
    
    ## Velocidad longitudinal media utilizada para identificar la escala L
    # Uav Vetor de velocidad promedio a diferentes alturas
    UavLs=np.mean(Uav) # No se utiliza para nada

    ##============================ Generate of P,Q,K Matrices====================================
    # nm es el numero de segmentos de frecuencia, nf Número de frecuencias aleatorias en un segmento.
    # Matriz (nf x 3 x nm) Estos, por cada segmento de frecuencia se tiene una matriz de (nf x 3), es decir
    # que por cada frecuencia dentro del segmento se tiene un valor para cada direccion. 
    K=np.zeros((nf,3,nm))
    r=np.random.randn(nf,3,nm) #Matriz nf filas, 3 columnas, nm capaz random con distribucion aleatoria media 0 desviacion 1
    #P=r/abs(r)*np.sqrt(1/nf*np.power(r,2)/(1+np.power(r,2)))
    P=np.sign(r)*np.sqrt(1/nf*np.power(r,2)/(1+np.power(r,2))) # p eq (6)
    #Q=r/abs(r)*np.sqrt(1/nf*1**2/(1+np.power(r,2)))
    Q=np.sign(r)*np.sqrt(1/nf*1**2/(1+np.power(r,2))) # q eq (6)

    Ls=np.zeros((nm,3,nd)) # parametro de la longitud de escala eq(7)


    for nmi in range(nm):
        # Ecuacion 7. Calculod de L con ecuacion 11
        # Lu perfil de escala longitudinal, fm vector de frecuencias
        # DGamma Longitud caracteristica utilizada para mantener la coherencia
        # Cxyz Constante de decaimiento de la coherencia en x, y, z [1  3] matrix
        for nyi in range(nd):
            Beta=10*DGamma/Lu[nyi] # Ese 10 corresponde a la constante de decaimiento, igual a Cxyz
            
            if (Beta>6):
                Gammai=2.1
            else: 
                Gammai=3.7*np.power(Beta,-0.3)
            
            Ls[nmi,:,nyi]=Uav[nyi]/fm[nmi]/Cxyz/Gammai # Esto es Uav/(gamma*Cxyz*fm)
        
        K[:,:,nmi]=RandSampleSphere(nf) # Coordenadas uniformemente distribuidas en una esfera de radio unitario
        
        for i in range(nf):
            XX=K[i,:,nmi].transpose()
            resMapp=mapp(XX,P[i,:,nmi],Q[i,:,nmi]).transpose() # Ecuacion 3 paper, no se para que se usa esta variable Parece que la meti yo
            K[i,:,nmi]=mapp(XX,P[i,:,nmi],Q[i,:,nmi]).transpose() # Ecuacion 3 paper

    ## Generar los campos de velocidad
    U=np.zeros((nd,nt))
    V=np.zeros((nd,nt))
    W=np.zeros((nd,nt))

    auxP=np.zeros((nf,1))
    auxQ=np.zeros((nf,1))
    auxWn=np.zeros((nf,1))
    auxZeros=np.zeros((Z.shape[0],1))
    vectorNTcolumnas=np.ones((1,nt))
    kjxj=np.zeros((nf,1))

    for inxyi in range(nd):
        for nmi in range(nm):


            #xjbar=1/Ls[nmi,:,inxyi]*np.array([X[inxyi],Y[inxyi],Z[inxyi]]) # eq(4) del paper
            xjbar=1/Ls[nmi,:,inxyi]*np.array([X[inxyi],auxZeros[inxyi],Z[inxyi]]) # eq(4) del paper
            kjxj[:,0]=(xjbar[0]*K[:,0,nmi]+xjbar[1]*K[:,1,nmi]+xjbar[2]*K[:,2,nmi])

            auxP[:,0]=P[:,0,nmi]
            auxQ[:,0]=Q[:,0,nmi]
            auxWn[:,0]=wn[:,nmi]

            U[inxyi,:]=U[inxyi,:]+sum(np.sqrt(Su[nmi,inxyi]*df*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*tt+kjxj*vectorNTcolumnas)+np.sqrt(Su[nmi,inxyi]*df*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*tt+kjxj*vectorNTcolumnas))

            auxP[:,0]=P[:,1,nmi]
            auxQ[:,0]=Q[:,1,nmi]
            
            V[inxyi,:]=V[inxyi,:]+sum(np.sqrt(Sv[nmi,inxyi]*df*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*tt+kjxj*vectorNTcolumnas)+np.sqrt(Sv[nmi,inxyi]*df*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*tt+kjxj*vectorNTcolumnas))
            
            auxP[:,0]=P[:,2,nmi]
            auxQ[:,0]=Q[:,2,nmi]
            
            W[inxyi,:]=W[inxyi,:]+sum(np.sqrt(Sw[nmi,inxyi]*df*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*tt+kjxj*vectorNTcolumnas)+np.sqrt(Sw[nmi,inxyi]*df*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*tt+kjxj*vectorNTcolumnas))
        
        ## Sumarle la velocidad media
        U[inxyi,:]=U[inxyi,:]+Uav[inxyi] # Porque solo en dirección longitudinal? 

    ## Pruebo el calculo de la coherencia entre dos puntos
    fs = 5e1
    f, Cxy = signal.coherence(U[0,:], U[3,:],fs)
    plt.semilogy(f, Cxy)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Coherence')
    plt.show()

    ## Pasar a los archivos csv

    TablaVel = np.zeros((X.shape[0],U.shape[1]+V.shape[1]+ W.shape[1] +3))

    TablaVel[:,0]=X[:,0]

    indY=0
    indZ=0
    while indY < TablaVel.shape[0]:
        TablaVel[indY:indY+Z.shape[0],1]= Y[indZ]
        TablaVel[indY:indY+Z.shape[0],2]= Z[:]
        indY=indY+Z.shape[0]
        indZ=indZ+1

    
    indExt=0
    while indExt < TablaVel.shape[0]:
        indVel=3
        indTab=0
        while indVel < TablaVel.shape[1]:
            TablaVel[indExt:indExt+Z.shape[0],indVel]= U[:,indTab]
            TablaVel[indExt:indExt+Z.shape[0],indVel+1]= V[:,indTab]
            TablaVel[indExt:indExt+Z.shape[0],indVel+2]= W[:,indTab]
            indVel=indVel+3
            indTab=indTab+1
        indExt=indExt+Z.shape[0]
    
    for i in range(TablaVel.shape[0]):
        fid2.write('\n')
        for j in range(TablaVel.shape[1]):
            cadena= str(TablaVel[i,j]) + ","
            fid2.write(cadena)

    
    fid2.close()



def main(): 
    h0u=0.3644 # Altura de referencia para la velocidad media Tabla |
    alphau=0.3264 # Exponente para la velocidad media               | -> Tabla 2
    Uh=10.0 # Velocidad media de referencia                         |

    h0I=0.3364 # Altura de referencia para la intesidad -> Revizar origen
    #--------Iuh,Ivh, Iwh son las intensidades longitudinal, transversal. Zou et al 2003 y ESDU 2001
    Iuh=0.2084
    Ivh=0.1815
    Iwh=0.1523
    #------------------------------------
    #-------dIu, dIv, dIw exponentes de intesidad longitudinal, transversal y vertical. Zou et al 2003 y ESDU 2001
    dIu=-0.1914
    dIv=-0.1228
    dIw=-0.0048
    #------------------------------------
    h0L=0.254 # Altura de referencia para la escala de longitud
    #-------Luh, Lvh, Lwh son las escalas de longitud en direccion
    Luh=0.302
    Lvh=0.0815
    Lwh=0.0326
    #------------------------------------
    #------dLu, dLv, dLw exponentes de intesidad longitudinal, transversal y vertical
    dLu=0.473
    dLv=0.8813
    dLw=1.5390
    #-----------------------------------
    Cxyz=np.array([10,10,10])
    ##DGamm Es la distancia caracteristica D. 
    #Para edificios altos tiene que estar entre 0.5h-1.0h donde h es la altura del edificio.
    #Si los valores de D dan un Beta mayor a 6. Beta se vuelve independiente de D
    DGamma=0.3 
    nf=100 # Numero de frecuencias random dentro de un segmento tabla 2 (M)
    nm=50 # Numero de segmentos de frecuencia tabla 2 (N)
    fmax=100 # Frecuencia maxima tabla 2
    dt=1/fmax/2/2.5 # Paso de tiempo. Analizar de donde sale este calculo 
    nt=1000 #Cantidad de pasos de tiempo
    Z= np.arange(0.05,1.3,0.05) # Altura del dominio. 1.3 m
    Y= np.arange(-1.00,1.25,0.25) # Posiciones en Y en el dominio -1.25 a 1.25 cada 0.25
    X=np.zeros((Z.shape[0]*Y.shape[0],1))

    CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,X,Y,Z)
    

if __name__ == "__main__":
    main()