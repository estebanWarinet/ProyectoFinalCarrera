import numpy as np
import math
import csv

import Funciones as fun
import Validar as val
import ManejarArchivos as archivos
import EspectrosFrecuencias as espFrec
import GenerarCamposVelocidad as genCamVel

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

    # Elementos que retorna
    # Un archivo ".csv" con los valores de velocidad para la capa inlet listo para pasar a Star ccm+
    # La imagen del decaimiento de la coherencia con el aumento de la frecuencia
    
    ##==========================================================================
    ##================== Inicializacion de variables ===========================
    ##==========================================================================

    nd=Z.shape[0] # Generar numero de puntos. Termina siendo el numero de filas de M
    
    ## Infomacion de la frecuencia
    # nm es el numero de segmentos de frecuencia
    fmin=(fmax/nm)/2 # Frecuencia Minima Averiguar porque se calcula asi
    df=(fmax-fmin)/(nm-1) # Paso de frecuencia
    fm=np.arange(fmin,fmax+df,df) # Vector de frecuencia

    ## Informacion temporal
    lim_tt=(nt*dt)-dt # Limite de tiempo
    tt=np.arange(0,lim_tt+dt,dt) # Vector de tiempo

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

    #================================================================================================
    #=============================== Abir los archivos csv ==========================================
    #================================================================================================  
    fid2=archivos.AbrirArchivos(tt)


    #================================================================================================
    #========================== Calcular espectros de frecuencia ====================================
    #================================================================================================
    
    Su,Sv,Sw = espFrec.CalcularEspectrosFrecuencias(df,nm,nd,Uav,fm,Iu,Iv,Iw,Lu, Lv, Lw)

    #=============================================================================================
    #============================= Generar P, Q y las matriz K ===================================
    #=============================================================================================
    # nm es el numero de segmentos de frecuencia, nf Número de frecuencias aleatorias en un segmento.
    # Matriz (nf x 3 x nm) Estos, por cada segmento de frecuencia se tiene una matriz de (nf x 3), es decir
    # que por cada frecuencia dentro del segmento se tiene un valor para cada direccion. 

    K=np.zeros((nf,3,nm))
    r=np.random.randn(nf,3,nm) #Matriz nf filas, 3 columnas, nm capaz random con distribucion aleatoria media 0 desviacion 1
    P=np.sign(r)*np.sqrt(1/nf*np.power(r,2)/(1+np.power(r,2))) # p eq (6)
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
        
        K[:,:,nmi]=fun.RandSampleSphere(nf) # Coordenadas uniformemente distribuidas en una esfera de radio unitario

        for i in range(nf):
            XX=K[i,:,nmi].transpose()
            resMapp=fun.mapp(XX,P[i,:,nmi],Q[i,:,nmi]).transpose() # Ecuacion 3 paper, no se para que se usa esta variable Parece que la meti yo
            K[i,:,nmi]=fun.mapp(XX,P[i,:,nmi],Q[i,:,nmi]).transpose() # Ecuacion 3 paper

    #=============================================================================================
    #============================ Generar los campos de velocidad ================================
    #=============================================================================================

    U,V,W = genCamVel.GenCamposVelocidad(tt,df,nt,nd,nf,nm,P,Q,wn,K,Ls,X,Z,Su,Sv,Sw,Uav)

    #=============================================================================================
    #====================== Graficar el decaimiento de coherencia ================================
    #=============================================================================================

    ## Calcular el decaimiento de la coherencia con el aumento de la frecuencia
    val.DecaimientoCoherencia(U,0,3)

    #================================================================================================
    #=============================== Pasar a los archivos csv =======================================
    #================================================================================================

    archivos.CargarDatos(fid2, X, Y, Z, U, V, W)



def main(): 
    ## La escala  que uso Aboshosha es de 1:500
    ## Las medidas del edificio son Height Hs 182.2, width Ws 30.48, depth Ds 30.48
    h0u=0.3644 # Altura de referencia para la velocidad media Tabla |
    alphau=0.3264 # Exponente para la velocidad media               | -> Tabla 2
    Uh=10.0 # Velocidad media de referencia                         |

    h0I=0.3364 # Altura de referencia para la intesidad -> Revizar origen == # Altura de referencia para la velocidad media Tabla
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
    dt=1/fmax/2/2.5 # Paso de tiempo. Analizar de donde sale este calculo Seguro para mantener el numero de número de Courant
    nt=1000 #Cantidad de pasos de tiempo
    Z= np.arange(0.05,1.3,0.05) # Altura del dominio. 1.3 m
    Y= np.arange(-1.00,1.25,0.25) # Posiciones en Y en el dominio -1.25 a 1.25 cada 0.25
    X=np.zeros((Z.shape[0]*Y.shape[0],1))

    CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,X,Y,Z)
    

if __name__ == "__main__":
    main()