import numpy as np
import sys
import csv
from zipfile import ZipFile

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

def CargarDatos(archivo, vectorTiempo, vectorPuntosX, vectorPuntosY, vectorPuntosZ, vectorU, vectorV, vectorW):
    
    TablaVel = np.zeros((vectorPuntosX.shape[0],vectorU.shape[1]+vectorV.shape[1]+ vectorW.shape[1] +3))

    TablaVel[:,0]=vectorPuntosX[:,0]

    ## Cargo los puntos de Y junto con Z
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
            if (np.count_nonzero(TablaVel[indExt:indExt+vectorPuntosZ.shape[0],1]<0) > 0):
                TablaVel[indExt:indExt+vectorPuntosZ.shape[0],indVel+1]= -1 * vectorV[:,indTab]
            else:
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

    ##==========================================================================
    ##============= Cargar archivo .wind =======================================
    ##==========================================================================

    archivoWind = open('Vientos.wind', 'w')
    cadena='1 0 0 \n'
    archivoWind.write(cadena) 

    cadena=str(vectorTiempo.shape[0])+' '+str(vectorPuntosY.shape[0])+' '+str(vectorPuntosZ.shape[0])+'\n'
    archivoWind.write(cadena)
    archivoWind.write(str(vectorTiempo[:])[1:-1])
    archivoWind.write('\n')
    archivoWind.write(str(vectorPuntosY[:])[1:-1])
    archivoWind.write('\n')
    archivoWind.write(str(vectorPuntosZ[:])[1:-1])
    archivoWind.write('\n')

    for indTemp in range(vectorTiempo.shape[0]):
        for indPuntosY in range(vectorPuntosY.shape[0]):
            archivoWind.write(np.array2string(vectorU[:,indTemp], precision=2, separator=' ')[1:-1])
            archivoWind.write(' ')
    
    archivoWind.write('\n')

    for indTemp in range(vectorTiempo.shape[0]):
        for indPuntosY in range(vectorPuntosY.shape[0]):
            archivoWind.write(np.array2string(vectorV[:,indTemp], precision=2, separator=' ')[1:-1])
            archivoWind.write(' ')
    
    archivoWind.write('\n')

    for indTemp in range(vectorTiempo.shape[0]):
        for indPuntosY in range(vectorPuntosY.shape[0]):
            archivoWind.write(np.array2string(vectorW[:,indTemp], precision=2, separator=' ')[1:-1])
            archivoWind.write(' ')
    
    archivoWind.write('\n')
    
    archivoWind.close()

def CrearArchivoZip():
    # create a ZipFile object
    zipObj = ZipFile('api.zip', 'w')
    # Add multiple files to the zip
    zipObj.write('TablaVelocidades.csv')
    zipObj.write('TablaVelocidadesInterpolada.csv')
    zipObj.write('Vientos.wind')
    # close the Zip File
    zipObj.close()
