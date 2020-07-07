import numpy as np
import math


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
    fid2=fopen('inletdata_U.csv','w')
    fid3=fopen('inletdata_V.csv','w')
    fid4=fopen('inletdata_W.csv','w')
    csv='X,Y,Z,'

    fprintf(fid2,csv)
    fprintf(fid2,'ux(m/s)[t=%es],',tt)
    fprintf(fid3,csv)
    fprintf(fid3,'ux(m/s)[t=%es],',tt)
    fprintf(fid4,csv)
    fprintf(fid4,'wx(m/s)[t=%es],',tt)


    ## Calculate the average velocity
    Uav=Uh*(Z/h0u).^alphau
    
    ## Turbulent Intensity
    Iu=Iuh*(Z/h0I).^dIu 
    Iv=Ivh*(Z/h0I).^dIv
    Iw=Iwh*(Z/h0I).^dIw
    
    ## Length scale profiles 
    Lu=Luh*(Z/h0L).^dLu 
    Lv=Lvh*(Z/h0L).^dLv
    Lw=Lwh*(Z/h0L).^dLw 
        
    ## Generate Wn (nf x nm) matrix, wn has 2.pi.fm mean and rms=2.pi.df
    wn=randn(nf,nm)*2*pi*df
    for nmi=1:nm
        wn(:,nmi)=wn(:,nmi)-mean(wn(:,nmi))
        wn(:,nmi)=wn(:,nmi)/std(wn(:,nmi))*2*pi*df
        wn(:,nmi)=wn(:,nmi)+fm(nmi)*2*pi
    endfor

    ## Calculate the spectrum matrices
    Su=zeros(nm,nd)
    Sv=zeros(nm,nd)
    Sw=zeros(nm,nd)
        
    fms=(-0.5:0.05:0.5)*df
    nfsm=size(fms,2)/2+0.5
    nfs=size(fms,2)
    
    ##==========================================================================
    
    for i=1:nd
        for j=1:nm
            fmjs=fm(j)+fms
            if j==1
                fmjs=fm(j)+fms(nfsm:nfs)
            endif
            
            Su(j,i)=mean(4*(Iu(i)*Uav(i))^2*(Lu(i)/Uav(i))./(1+70.8*(fmjs*Lu(i)/Uav(i)).^2).^(5/6))
            Sv(j,i)=mean(4*(Iv(i)*Uav(i))^2*(Lv(i)/Uav(i))*(1+188.4*(2*fmjs*Lv(i)/Uav(i)).^2)./(1+70.8*(2*fmjs*Lv(i)/Uav(i)).^2).^(11/6))
            Sw(j,i)=mean(4*(Iw(i)*Uav(i))^2*(Lw(i)/Uav(i))*(1+188.4*(2*fmjs*Lw(i)/Uav(i)).^2)./(1+70.8*(2*fmjs*Lw(i)/Uav(i)).^2).^(11/6))
        endfor
    endfor
    
    ## Mean long. velocity used to identify the L scale
    UavLs=mean(Uav) 

    ## Generate of P,Q,K Matrices

    K=zeros(nf,3,nm)
    r=randn(nf,3,nm)
    P=r./abs(r).*sqrt(1/nf*(r).^2./(1+r.^2))
    Q=r./abs(r).*sqrt(1/nf*(1).^2./(1+r.^2))
    Ls=zeros(nm,3,nd)
    for nmi=1:nm
        for nyi=1:nd
            Beta=10*DGamma/Lu(nyi)
            
            if Beta>6
                Gammai=2.1
            else 
                Gammai=3.7*Beta^-.3
            endif
            
            Ls(nmi,:,nyi)=Uav(nyi)/fm(nmi)./Cxyz/Gammai
        endfor
        
        K(:,:,nmi)=RandSampleSphere(nf)
        
        for i=1:nf
            XX=K(i,:,nmi)'
            K(i,:,nmi)=mapp(XX,P(i,:,nmi),Q(i,:,nmi))'
        endfor
        
    endfor

    ## Generate the Velocity Vectors
    U=zeros(nd,nt)
    V=zeros(nd,nt)
    W=zeros(nd,nt)

    for inxyi=1:nd
        for nmi=1:nm

            xjbar=1./Ls(nmi,:,inxyi).*[X(inxyi) Y(inxyi) Z(inxyi)]

            kjxj=(xjbar(1)*K(:,1,nmi)+xjbar(2)*K(:,2,nmi)+xjbar(3)*K(:,3,nmi))

            U(inxyi,:)=U(inxyi,:)+sum(sqrt(Su(nmi,inxyi)*df*2)*(P(:,1,nmi)*ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*ones(1,nt))+sqrt(Su(nmi,inxyi)*df*2)*(Q(:,1,nmi)*ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*ones(1,nt)))
            V(inxyi,:)=V(inxyi,:)+sum(sqrt(Sv(nmi,inxyi)*df*2)*(P(:,2,nmi)*ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*ones(1,nt))+sqrt(Sv(nmi,inxyi)*df*2)*(Q(:,2,nmi)*ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*ones(1,nt)))
            W(inxyi,:)=W(inxyi,:)+sum(sqrt(Sw(nmi,inxyi)*df*2)*(P(:,3,nmi)*ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*ones(1,nt))+sqrt(Sw(nmi,inxyi)*df*2)*(Q(:,3,nmi)*ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*ones(1,nt)))
        endfor
        
        ## Add the mean velocity
        U(inxyi,:)=U(inxyi,:)+Uav(inxyi) 
    
    endfor

    ## Print the velocity vectors
    TableU=[X Y Z U]
    TableV=[X Y Z V] 
    TableW=[X Y Z W]
    
    for i=1:size(TableU,1)
        fprintf(fid2,'\r\n')
        j=1:size(TableU,2)
        fprintf(fid2,'%e,',TableU(i,j))
    endfor
    
    for i=1:size(TableV,1)
        fprintf(fid3,'\r\n')
        j=1:size(TableV,2)
        fprintf(fid3,'%e,',TableV(i,j))
    endfor
    
    for i=1:size(TableW,1)
        fprintf(fid4,'\r\n')
        j=1:size(TableW,2)
        fprintf(fid4,'%e,',TableW(i,j))
    endfor
    
    fclose(fid2)
    fclose(fid3)
    fclose(fid4)



#main 
#h0u=0.3644;alphau=0.3264;Uh=10.0;
#h0I=0.3364;
#Iuh=0.2084;Ivh=0.1815;Iwh=0.1523;
#dIu=-0.1914;dIv=-0.1228;dIw=-0.0048;
#h0L=0.254;
#Luh=0.302;Lvh=0.0815;Lwh=0.0326;
#dLu=0.473;dLv=0.8813;dLw=1.5390;
#Cxyz=[10 10 10];DGamma=0.3;
#nf=100;nm=50;fmax=100;
#dt=1/fmax/2/2.5;nt=1000;
#M=[zeros(10,1) zeros(10,1) (0.05:0.1:1)']; % Sample coordinate matrix

#[X,Y,Z,U,V,W]=CDRFG_script(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,M);