import numpy as np
import math

def CalcularEspectrosFrecuencias(deltafrec, numSegmentos, numPuntos, vecVelEnDiferentesAlt, vecFrecuencias, intensidadU, intensidadV, intensidadW,escalaLongU, escalaLongV, escalaLongW):
    # deltafrec PasoFrecuencia

    ## Creo las matrices del espectro
    # numSegmentos es el numero de segmentos, numPuntos cantidad de puntos
    Su=np.zeros((numSegmentos,numPuntos))
    Sv=np.zeros((numSegmentos,numPuntos))
    Sw=np.zeros((numSegmentos,numPuntos))
    
    ## Investigar de donumPuntose salen estos numeros    
    vecFrecuenciass=np.arange(-0.5,0.5+0.05,0.05)*deltafrec
    nfsm=vecFrecuenciass.shape[0]/2+0.5 
    nfs=vecFrecuenciass.shape[0] 
    
    ## Espectros de la turbulencia según los define Von Karma
    # vecFrecuencias vector de frecuencias
    # vecVelEnDiferentesAlt Vetor de velocidad promedio a diferentes alturas
    # intensidadU, intensidadV, intensidadW son las intensidades longitudinal, transversal y vertical
    # escalaLongU, escalaLongV, escalaLongW son los perfiles escalas de longitud en direccion
    for i in range(numPuntos):
        for j in range (numSegmentos):
            vecFrecuenciasjs=vecFrecuencias[j]+vecFrecuenciass
            if (j==1):
                vecFrecuenciasjs=vecFrecuencias[j]+vecFrecuenciass[int(nfsm):int(nfs)]
            Su[j,i]=np.mean(4*((intensidadU[i]*vecVelEnDiferentesAlt[i])**2)*(escalaLongU[i]/vecVelEnDiferentesAlt[i])/np.power(1+70.8*np.power(vecFrecuenciasjs*escalaLongU[i]/vecVelEnDiferentesAlt[i],2),(5/6))) #Revisar dintensidadVision
            Sv[j,i]=np.mean(4*((intensidadV[i]*vecVelEnDiferentesAlt[i])**2)*(escalaLongV[i]/vecVelEnDiferentesAlt[i])*(1+188.4*np.power(2*vecFrecuenciasjs*escalaLongV[i]/vecVelEnDiferentesAlt[i],2))/np.power(1+70.8*np.power(2*vecFrecuenciasjs*escalaLongV[i]/vecVelEnDiferentesAlt[i],2),(11/6)))
            Sw[j,i]=np.mean(4*((intensidadW[i]*vecVelEnDiferentesAlt[i])**2)*(escalaLongW[i]/vecVelEnDiferentesAlt[i])*(1+188.4*np.power(2*vecFrecuenciasjs*escalaLongW[i]/vecVelEnDiferentesAlt[i],2))/np.power(1+70.8*np.power(2*vecFrecuenciasjs*escalaLongW[i]/vecVelEnDiferentesAlt[i],2),(11/6)))
    
    ## Velocidad longitudinal media utilizada para identificar la escala L
    # vecVelEnDiferentesAlt Vetor de velocidad promedio a diferentes alturas
    #vecVelEnDiferentesAltLs=np.mean(vecVelEnDiferentesAlt) # No se utiliza para nada

    return Su,Sv,Sw