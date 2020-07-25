import numpy as np
import csv

def AbrirArchivos(vectorTiempo):
    ## Abrir los archivos y acomodarlos de la forma que se requiere para STAR CCM+
    fid2 = open('TablaVelocidades.csv','w')
    #Escribo las cabezeras de los archivos (primer fila)
    csvHead='X,Y,Z,'
    fid2.write(csvHead)

    for i in range(vectorTiempo.shape[0]):
        cadena='ux(m/s)[t='+str(vectorTiempo[i])+'], '+'vx(m/s)[t='+str(vectorTiempo[i])+'], '+'wx(m/s)[t='+str(vectorTiempo[i])+'], '
        fid2.write(cadena)

    return fid2

def CargarDatos(archivo, vectorPuntosX, vectorPuntosY, vectorPuntosZ, vectorU, vectorV, vectorW):
    
    TablaVel = np.zeros((vectorPuntosX.shape[0],vectorU.shape[1]+vectorV.shape[1]+ vectorW.shape[1] +3))

    TablaVel[:,0]=vectorPuntosX[:,0]

    indY=0
    indZ=0
    while indY < TablaVel.shape[0]:
        TablaVel[indY:indY+vectorPuntosZ.shape[0],1]= vectorPuntosY[indZ]
        TablaVel[indY:indY+vectorPuntosZ.shape[0],2]= vectorPuntosZ[:]
        indY=indY+vectorPuntosZ.shape[0]
        indZ=indZ+1

    
    indExt=0
    while indExt < TablaVel.shape[0]:
        indVel=3
        indTab=0
        while indVel < TablaVel.shape[1]:
            TablaVel[indExt:indExt+vectorPuntosZ.shape[0],indVel]= vectorU[:,indTab]
            TablaVel[indExt:indExt+vectorPuntosZ.shape[0],indVel+1]= vectorV[:,indTab]
            TablaVel[indExt:indExt+vectorPuntosZ.shape[0],indVel+2]= vectorW[:,indTab]
            indVel=indVel+3
            indTab=indTab+1
        indExt=indExt+vectorPuntosZ.shape[0]
    
    for i in range(TablaVel.shape[0]):
        archivo.write('\n')
        for j in range(TablaVel.shape[1]):
            cadena= str(TablaVel[i,j]) + ","
            archivo.write(cadena)

    
    archivo.close()