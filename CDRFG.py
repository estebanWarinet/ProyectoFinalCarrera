import numpy as np
import math
import csv


########################################################

def RandSampleSphere(N):
    # Generate a random sampling XYZ N coordinates on a unit radius sphere
    t0z=2*math.pi*np.random.rand(N,1) # vector de numeros aleatorio de N filas por 1 columna
    z=np.sin(t0z)
    t=2*math.pi*np.random.rand(N,1)# vector de numeros aleatorio de N filas por 1 columna
    r=np.sqrt(1-np.power(z))
    x=r*np.cos(t)
    y=r*np.sin(t)
    XYZ=np.zeros((N,3))
    XYZ[:,0]=x[:,0]
    XYZ[:,1]=y[:,0]
    XYZ[:,2]=z[:,0]
    return XYZ

    
def mapp(X,q,p):
    # System of non-linear equations that maintains the divergence-free condition
    # X vector columna, q y p Vectores filas
    fx=np.zeros((3,1))
    fx[0,0]=1
    K=np.zeros((3,3))
    K[0,:]=X[:,0]
    K[1,:]=q[0,:]
    K[2,:]=p[0,:]
    F=fx-np.dot(K,X)
    return F


def CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Lwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,M):

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
    
    ## Extract the coordinates and frequency information
    X=M[:,0]
    Y=M[:,1] 
    Z=M[:,2] # x and y coordinates vector at the inflow plane
    nd,_=X.shape # overall no of points
    fmin=(fmax/nm)/2 # Min Frequency
    df=(fmax-fmin)/(nm-1) # Frequency step
    fm=np.arange(fmin,fmax,df) # Frequency vector
    #tt=dtn(0:(nt-1)); # time vector
    lim_tt=(nt*dt)-dt # time vector
    tt=np.arange(0,lim_tt,dt) # time vector

    ## Prepare the output file according to the format required by STAR CCM+
    fid2 = open("inletdata_U.csv",'w')
    fid3 = open("inletdata_V.csv",'w')
    fid4 = open("inletdata_W.csv",'w')
    csv='X,Y,Z,'
    fid2.write(csv)
    fid3.write(csv)
    fid4.write(csv)

    for i in range(tt.shape[0]):
        cadena='ux(m/s)[t='+str(tt[i])+'],'
        fid2.write(cadena)
        fid3.write(cadena)
        fid4.write(cadena)


    ## Calculate the average velocity
    Uav=Uh*np.power(Z/h0u,alphau)
    
    ## Turbulent Intensity
    Iu=Iuh*np.power(Z/h0I,dIu) 
    Iv=Ivh*np.power(Z/h0I,dIv)
    Iw=Iwh*np.power(Z/h0I,dIw)
    
    ## Length scale profiles 
    Lu=Luh*np.power(Z/h0L,dLu) 
    Lv=Lvh*np.power(Z/h0L,dLv)
    Lw=Lwh*np.power(Z/h0L,dLw) 
        
    ## Generate Wn (nf x nm) matrix, wn has 2.pi.fm mean and rms=2.pi.df
    wn=np.random.randn(nf,nm)*2*np.pi*df
    for nmi in range(nm):
        wn[:,nmi]=wn[:,nmi]-np.mean(wn[:,nmi])
        wn[:,nmi]=wn[:,nmi]/np.std(wn[:,nmi])*2*np.pi*df
        wn[:,nmi]=wn[:,nmi]+fm[nmi]*2*np.pi

    ## Calculate the spectrum matrices
    Su=np.zeros((nm,nd))
    Sv=np.zeros((nm,nd))
    Sw=np.zeros((nm,nd))
        
    fms=np.arrange(-0.5,0.5,0.05)*df
    nfsm=fms.shape[1]/2+0.5 #Aca puede existir terrible error
    nfs=fms.shape[1] #Aca tambien
    
    ##==========================================================================
    
    for i in range(nd):
        for j in range (nm):
            fmjs=fm[j]+fms
            if (j==1):
                fmjs=fm[j]+fms[nfsm:nfs]
            
            Su[j,i]=np.mean(4*(Iu[i]*Uav[i])^2*(Lu[i]/Uav[i])/np.power(1+70.8*np.power(fmjs*Lu[i]/Uav[i],2),(5/6))) #Revisar division
            Sv[j,i]=np.mean(4*(Iv[i]*Uav[i])^2*(Lv[i]/Uav[i])*np.power(1+188.4*(2*fmjs*Lv[i]/Uav[i],2))/np.power(1+70.8*np.power(2*fmjs*Lv[i]/Uav[i],2),(11/6)))
            Sw[j,i]=np.mean(4*(Iw[i]*Uav[i])^2*(Lw[i]/Uav[i])*np.power(1+188.4*(2*fmjs*Lw[i]/Uav[i],2))/np.power(1+70.8*np.power(2*fmjs*Lw[i]/Uav[i],2),(11/6)))
    
    ## Mean long. velocity used to identify the L scale
    UavLs=np.mean(Uav) 

    ## Generate of P,Q,K Matrices

    K=np.zeros((nf,3,nm)) #Buscar porque tiene 3 parametros
    r=np.random.randn(nf,3,nm)
    P=r/abs(r)*np.sqrt(1/nf*np.power(r,2)/(1+np.power(r,2)))
    Q=r/abs(r)*np.sqrt(1/nf*1**2/(1+np.power(r,2)))
    Ls=np.zeros((nm,3,nd))
    for nmi in range(nm):
        for nyi in range(nd):
            Beta=10*DGamma/Lu[nyi]
            
            if (Beta>6):
                Gammai=2.1
            else: 
                Gammai=3.7*np.power(Beta,-0.3)
            
            Ls[nmi,:,nyi]=Uav[nyi]/fm[nmi]/Cxyz/Gammai
        
        K[:,:,nmi]=RandSampleSphere(nf)
        
        for i in range(nf):
            XX=K[i,:,nmi].transpose()
            K[i,:,nmi]=mapp(XX,P[i,:,nmi],Q[i,:,nmi]).transpose()

    ## Generate the Velocity Vectors
    U=np.zeros((nd,nt))
    V=np.zeros((nd,nt))
    W=np.zeros((nd,nt))

    for inxyi in range(nd):
        for nmi in range(nm):

            xjbar=1/Ls[nmi,:,inxyi]*np.array([X[inxyi],Y[inxyi],Z[inxyi]])

            kjxj=(xjbar[0]*K[:,0,nmi]+xjbar[1]*K[:,1,nmi]+xjbar[2]*K[:,2,nmi])

            U[inxyi,:]=U[inxyi,:]+sum(np.sqrt(Su[nmi,inxyi]*df*2)*(P[:,0,nmi]*np.ones((1,nt)))*np.cos(wn[:,nmi]*tt+kjxj*np.ones((1,nt)))+np.sqrt(Su[nmi,inxyi]*df*2)*(Q[:,0,nmi]*np.ones((1,nt)))*np.sin(wn[:,nmi]*tt+kjxj*np.ones((1,nt))))
            V[inxyi,:]=V[inxyi,:]+sum(np.sqrt(Sv[nmi,inxyi]*df*2)*(P[:,1,nmi]*np.ones((1,nt)))*np.cos(wn[:,nmi]*tt+kjxj*np.ones((1,nt)))+np.sqrt(Sv[nmi,inxyi]*df*2)*(Q[:,1,nmi]*np.ones((1,nt)))*np.sin(wn[:,nmi]*tt+kjxj*np.ones((1,nt))))
            W[inxyi,:]=W[inxyi,:]+sum(np.sqrt(Sw[nmi,inxyi]*df*2)*(P[:,2,nmi]*np.ones((1,nt)))*np.cos(wn[:,nmi]*tt+kjxj*np.ones((1,nt)))+np.sqrt(Sw[nmi,inxyi]*df*2)*(Q[:,2,nmi]*np.ones((1,nt)))*np.sin(wn[:,nmi]*tt+kjxj*np.ones((1,nt))))
        
        ## Add the mean velocity
        U[inxyi,:]=U[inxyi,:]+Uav[inxyi] 

    ## Print the velocity vectors
    TableU=np.zeros((X.shape[0],U.shape[1]+3))
    TableV=np.zeros((X.shape[0],V.shape[1]+3))
    TableW=np.zeros((X.shape[0],W.shape[1]+3))
    
    TableU[:,0]=X[:]
    TableU[:,1]=Y[:]
    TableU[:,2]=Z[:]
    TableU[:,3::]=U[:,:]
    TableV[:,0]=X[:]
    TableV[:,1]=Y[:]
    TableV[:,2]=Z[:]
    TableV[:,3::]=V[:,:]
    TableW[:,0]=X[:]
    TableW[:,1]=Y[:]
    TableW[:,2]=Z[:]
    TableW[:,3::]=W[:,:]
    
    for i in range(TableU.shape[0]):
        fid2.write('\n')
        for j in range(TableU.shape[1]):
            cadena=str(TableU[i,j])+','
            fid2.write(cadena)

    
    for i in range(TableV.shape[0]):
        fid3.write('\n')
        for j in range(TableV.shape[1]):
            cadena=str(TableV[i,j])+','
            fid3.write(cadena)

    
    for i in range(TableW.shape[0]):
        fid4.write('\n')
        for j in range(TableW.shape[1]):
            cadena=str(TableW[i,j])+','
            fid4.write(cadena)

    
    fid2.close()
    fid3.close()
    fid4.close()



def main(): 
    h0u=0.3644;alphau=0.3264;Uh=10.0;
    h0I=0.3364;
    Iuh=0.2084;Ivh=0.1815;Iwh=0.1523;
    dIu=-0.1914;dIv=-0.1228;dIw=-0.0048;
    h0L=0.254;
    Luh=0.302;Lvh=0.0815;Lwh=0.0326;
    dLu=0.473;dLv=0.8813;dLw=1.5390;
    Cxyz=np.array([10,10,10]);
    DGamma=0.3;
    nf=100;nm=50;fmax=100;
    dt=1/fmax/2/2.5;nt=1000;
    M=np.zeros((10,3));
    M[:,2]=np.arange(0.05,1,0.1).transpose(); # Sample coordinate matrix

    CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,M);
    

if __name__ == "__main__":
    main()