import numpy as np
import math

def GenCamposVelocidad(vecTiempo,deltafrec, numPasoTiempo, numPuntos, numFrecuenciasSegmento, numSegFrec, P, Q, wn, K, longEscala, ptX, ptZ, Su, Sv, Sw, vecVelEnDiferentesAlt):
    # deltafrec PasoFrecuencia
    # vecTiempo Vector de tiempo
    # numPasoTiempo Number of time steps
    # numPuntos Numeros de puntos
    # numFrecuenciasSegmento Number of random frequencies in one segment
    # numSegFrec es el numero de segmentos de frecuencia
    # longEscala longitud de escala
    # Su,Sv,Sw Espectros de frecuencias
    # vecVelEnDiferentesAlt Vetor de velocidad promedio a diferentes alturas
    U=np.zeros((numPuntos,numPasoTiempo))
    V=np.zeros((numPuntos,numPasoTiempo))
    W=np.zeros((numPuntos,numPasoTiempo))

    auxP=np.zeros((numFrecuenciasSegmento,1))
    auxQ=np.zeros((numFrecuenciasSegmento,1))
    auxWn=np.zeros((numFrecuenciasSegmento,1))
    auxZeros=np.zeros((ptZ.shape[0],1))
    vectorNTcolumnas=np.ones((1,numPasoTiempo))
    kjxj=np.zeros((numFrecuenciasSegmento,1))

    for inxyi in range(numPuntos):
        for nmi in range(numSegFrec):

            xjbar=1/longEscala[nmi,:,inxyi]*np.array([ptX[inxyi],auxZeros[inxyi],ptZ[inxyi]]) # eq(4) del paper
            kjxj[:,0]=(xjbar[0]*K[:,0,nmi]+xjbar[1]*K[:,1,nmi]+xjbar[2]*K[:,2,nmi])

            auxP[:,0]=P[:,0,nmi]
            auxQ[:,0]=Q[:,0,nmi]
            auxWn[:,0]=wn[:,nmi]

            U[inxyi,:]=U[inxyi,:]+sum(np.sqrt(Su[nmi,inxyi]*deltafrec*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas)+np.sqrt(Su[nmi,inxyi]*deltafrec*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas))

            auxP[:,0]=P[:,1,nmi]
            auxQ[:,0]=Q[:,1,nmi]
            
            V[inxyi,:]=V[inxyi,:]+sum(np.sqrt(Sv[nmi,inxyi]*deltafrec*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas)+np.sqrt(Sv[nmi,inxyi]*deltafrec*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas))
            
            auxP[:,0]=P[:,2,nmi]
            auxQ[:,0]=Q[:,2,nmi]
            
            W[inxyi,:]=W[inxyi,:]+sum(np.sqrt(Sw[nmi,inxyi]*deltafrec*2)*(auxP[:]*vectorNTcolumnas)*np.cos(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas)+np.sqrt(Sw[nmi,inxyi]*deltafrec*2)*(auxQ[:]*vectorNTcolumnas)*np.sin(auxWn[:]*vecTiempo+kjxj*vectorNTcolumnas))
        
        ## Sumarle la velocidad media
        U[inxyi,:]=U[inxyi,:]+vecVelEnDiferentesAlt[inxyi] # Porque solo en dirección longitudinal?
    
    return U,V,W