#!/usr/bin/python
from scipy.interpolate import griddata
import numpy as np
import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from stl import mesh

if 1:
    #filename = 'Turb15_rect21x21_100s.wind'
    filename = 'Vientos.wind'
    iblock = 1
    data = dict()
    data['nt'] = []
    data['ny'] = []
    data['nz'] = []
    data['times'] = []
    data['Y'] = []
    data['Z'] = []
    data['Ux'] = []
    data['Uy'] = []
    data['Uz'] = []

    aux = []
    with open(filename, mode='r') as windfile:
        iline = 0
        it = 0
        iy = 0
        iz = 0
        for line in windfile:
            if iblock==1:
                #no hago nada, supongo que es cartesiano
                iblock = iblock+1
            elif iblock==2:
                row = line.split()
                nt = int(row[0])
                ny = int(row[1])
                nz = int(row[2])
                data['nt'] = nt
                data['ny'] = ny
                data['nz'] = nz
                iblock = iblock+1
            elif iblock==3:
                row = line.split()
                for irow in row:
                    data['times'].append(float(irow))
                    it=it+1
                if it==nt:
                    iblock = iblock+1
                    it = 0
            elif iblock==4:
                row = line.split()
                for irow in row:
                    data['Y'].append(float(irow))
                    iy=iy+1                
                if iy==ny:
                    iblock = iblock+1
                    iy=0
            elif iblock==5:
                row = line.split()
                for irow in row:
                    data['Z'].append(float(irow))
                    iz=iz+1
                if iz==nz:
                    iblock = iblock+1
                    iz=0
            elif iblock==6:
                row = line.split()
                for irow in row:
                    aux.append(float(irow))
                    iz = iz+1
                    if iz==nz:
                        iz = 0
                        iy = iy+1
                    if iy==ny:
                        iy = 0
                        it = it + 1
                        data['Ux'].append(aux)
                        aux = []
                    if it == nt:
                        iy = 0
                        iz = 0
                        it = 0
                        iblock = iblock + 1
                        print('Ux completed')
            elif iblock==7:
                row = line.split()
                for irow in row:
                    aux.append(float(irow))
                    iz = iz+1
                    if iz==nz:
                        iz = 0
                        iy = iy+1
                    if iy==ny:
                        iy = 0
                        it = it + 1
                        data['Uy'].append(aux)
                        aux = []
                    if it == nt:
                        iy = 0
                        iz = 0
                        it = 0
                        iblock = iblock + 1
                        print('Uy completed')
            elif iblock==8:
                row = line.split()
                for irow in row:
                    aux.append(float(irow))
                    iz = iz+1
                    if iz==nz:
                        iz = 0
                        iy = iy+1
                    if iy==ny:
                        iy = 0
                        it = it + 1
                        data['Uz'].append(aux)
                        aux = []
                    if it == nt:
                        iy = 0
                        iz = 0
                        it = 0
                        iblock = iblock + 1
                        print('Uz completed')
            else:
                print('Ojo! leyendo basura: %s'%line)
                
        windfile.close()
        

    
    data['Y'] = np.array(data['Y'])
    data['Z'] = np.array(data['Z'])
    data['Ux'] = np.array(data['Ux'])
    data['Uy'] = np.array(data['Uy'])
    data['Uz'] = np.array(data['Uz'])
    
    if 0:
        plt.figure()
        for it in range(nt):
            plt.clf()
            yv, zv = np.meshgrid(data['Y'], data['Z'])
            magU = np.sqrt(np.square(data['Ux'][it])+np.square(data['Uy'][it])+np.square(data['Uz'][it]))
            plt.pcolor(yv,zv,np.reshape(magU,(data['ny'],data['nz']),order='F'))
            plt.colorbar()
            plt.draw()
            plt.pause(0.1)


#stlmesh = mesh.Mesh.from_file('Inlet_swt23_300p.stl')
stlmesh = mesh.Mesh.from_file('Grilla.stl')
#stlmesh = mesh.Mesh.from_file('GrillaGerardoBin.stl')
#stlmesh = mesh.Mesh.from_file('GrillaGerardoCode.stl')



# extraer todos los centroides
Xc = []
for iv in range(len(stlmesh.v0)):
    xc = 1./3.*(stlmesh.v0[iv,:] + stlmesh.v1[iv,:] + stlmesh.v2[iv,:])
    Xc.append(xc)
Xc = np.array(Xc)

#computar limites para desplazar z (ojo con y)
miny = np.min(Xc[:,1])
minz = np.min(Xc[:,2])
maxy = np.max(Xc[:,1])
maxz = np.max(Xc[:,2])
print('y:[%3.5f, %3.5f] z:[%3.5f, %3.5f]'%(miny,maxy,minz,maxz))

minz_data = 0

# pongo las posiciones originales en una tira
yv, zv = np.meshgrid(data['Y'], data['Z'])
Y = np.reshape(yv,data['ny']*data['nz'],order='F')
Z = np.reshape(zv,data['ny']*data['nz'],order='F')

# genero al vuelo un csv
import csv

#data['nt'] = 10
#nt = 10
Ux = []
Uy = []
Uz = []

for it in range(data['nt']):
    print('computing time %3.5f'%data['times'][it])
    Ux.append(griddata(np.array([Y,Z-(minz_data-minz)]).transpose(),data['Ux'][it],Xc[:,1:], method='linear', fill_value=0, rescale=False))
    Uy.append(griddata(np.array([Y,Z-(minz_data-minz)]).transpose(),data['Uy'][it],Xc[:,1:], method='linear', fill_value=0, rescale=False))
    Uz.append(griddata(np.array([Y,Z-(minz_data-minz)]).transpose(),data['Uz'][it],Xc[:,1:], method='linear', fill_value=0, rescale=False))


Ux = np.array(Ux)
Uy = np.array(Uy)
Uz = np.array(Uz)

with open('TablaVelocidadesInterpolada.csv', 'w') as csvfile:
    
    fieldnames = ['X', 'Y', 'Z']
    for it in range(data['nt']):
        fieldnames.append('Ux(m/s)[t=%3.5fs]'%data['times'][it])
    for it in range(data['nt']):
        fieldnames.append('Uy(m/s)[t=%3.5fs]'%data['times'][it])
    for it in range(data['nt']):
        fieldnames.append('Uz(m/s)[t=%3.5fs]'%data['times'][it])
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=',')
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=' ')

    writer.writeheader()
    
    for ip in range(Xc.shape[0]):
    
        print("Writing point %i"%ip)
        
        dataout = dict()
        dataout['X'] = Xc[ip,0]
        dataout['Y'] = Xc[ip,1]
        dataout['Z'] = Xc[ip,2]
        
        for it in range(data['nt']):
            dataout['Ux(m/s)[t=%3.5fs]'%data['times'][it]] = Ux[it,ip]
        for it in range(data['nt']):
            dataout['Uy(m/s)[t=%3.5fs]'%data['times'][it]] = Uy[it,ip]
        for it in range(data['nt']):
            dataout['Uz(m/s)[t=%3.5fs]'%data['times'][it]] = Uz[it,ip]
        
        writer.writerow(dataout)
    
if 0:
    it = 0
    magU = np.sqrt(np.square(data['Ux'][it])+np.square(data['Uy'][it])+np.square(data['Uz'][it]))
    MAGU = griddata(np.array([Y,Z-(minz_data-minz)]).transpose(),magU,Xc[:,1:], method='nearest', fill_value=0, rescale=False)


    # Just plot interpolated values
    N = 50
    yy = np.array([miny*((N-i)/float(N))+maxy*i/float(N) for i in range(N+1)])
    zz = np.array([minz*((N-i)/float(N))+maxz*i/float(N) for i in range(N+1)])
    yv, zv = np.meshgrid(yy,zz)
    magUv = griddata(Xc[:,1:],MAGU,np.array([np.reshape(yv,(N+1)*(N+1),order='F'),np.reshape(zv,(N+1)*(N+1),order='F')]).transpose(),method='linear', fill_value=0, rescale=False)
    plt.figure(1)
    plt.clf()
    plt.pcolor(yv,zv,np.reshape(magUv,(N+1,N+1),order='F'))
    plt.colorbar()
    plt.draw()
    plt.pause(0.1)

