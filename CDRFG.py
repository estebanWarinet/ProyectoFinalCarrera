import numpy as np
import math


########################################################

class RandSampleSphere(N):
    # Generate a random sampling XYZ N coordinates on a unit radius sphere
    t0z=2*math.pi*rand(N,1) # averifguar por el rand
    z=sin(t0z)
    t=2*math.pi*rand(N,1)
    r=sqrt(1-z.^2)
    x=r.*cos(t)
    y=r.*sin(t)
    XYZ=[x,y,z]
    
class mapp(X,q,p):
    # System of non-linear equations that maintains the divergence-free condition
    fx=[1;0;0]
    K=[X(1) X(2) X(3);q;p]
    F=fx-K*X


class CDRFG_2015(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,M):
    
    # OUTPUT Parameters
    # Three files (i.e. inletdata_U, inletdata_V and inletdata_W) that have the
    # generated velocity records compatible with STAR CCM+
    for i in range(nd):
        for j in range(nm):
            fmjs=fm(j)+fms
            if j==0:
                fmjs=fm(j)+fms(nfsm:nfs)
                
            Su(j,i)=mean(4*(Iu(i)*Uav(i))^2*(Lu(i)/Uav(i))./(1+70.8*(fmjs*Lu(i)/Uav(i)).^2).^(5/6)) #ver como calcular la media y demas operaciones
            Sv(j,i)=mean(4*(Iv(i)*Uav(i))^2*(Lv(i)/Uav(i))*(1+188.4*(2*fmjs*Lv(i)/Uav(i)).^2)./(1+70.8*(2*fmjs*Lv(i)/Uav(i)).^2).^(11/6))
            Sw(j,i)=mean(4*(Iw(i)*Uav(i))^2*(Lw(i)/Uav(i))*(1+188.4*(2*fmjs*Lw(i)/Uav(i)).^2)./(1+70.8*(2*fmjs*Lw(i)/Uav(i)).^2).^(11/6))

    UavLs=mean(Uav) # mean long. velocity used to identify the L scale
    
    ## Generate of P,Q,K Matrices
    
    K=np.zeros(nf,3,nm) # Ver que cuerno se quizo hacer aca
    r=randn(nf,3,nm)
    P=r./abs(r).*sqrt(1/nf*(r).^2./(1+r.^2))
    Q=r./abs(r).*sqrt(1/nf*(1).^2./(1+r.^2))
    Ls=zeros(nm,3,nd)
    
    for nmi in range(nm):
        for nyi in range(nd):
            Beta=10*DGamma/Lu(nyi)
            if Beta>6:
                Gammai=2.1
            else 
                Gammai=3.7*Beta^-.3

            Ls(nmi,:,nyi)=Uav(nyi)/fm(nmi)./Cxyz/Gammai # Revisar que cuenta es esta
       
        K(:,:,nmi)=RandSampleSphere(nf) # Revisar que cuenta es esta
        
        for i in range(nf):
            XX=K(i,:,nmi)’ # Hacer el transpuesto
            myfun=@(xx) mapp(xx,P(i,:,nmi),Q(i,:,nmi)) # Invoca otra clase
            K(i,:,nmi)=(fsolve(myfun,XX))’ #Utiliza la clase anterior y la transpone
            
    %% Generate the Velocity Vectors
    U=zeros(nd,nt);V=zeros(nd,nt);W=zeros(nd,nt);

    for inxyi in range(nd):
        for nmi in range(nm):

            xjbar=1./Ls(nmi,:,inxyi).*[X(inxyi) Y(inxyi) Z(inxyi)]

            kjxj=(xjbar(1)*K(:,1,nmi)+xjbar(2)*K(:,2,nmi)+xjbar(3)*K(:,3,nmi))

            U(inxyi,:)=U(inxyi,:)+sum(sqrt(Su(nmi,inxyi)*df*2)*(P(:,1,nmi)*np.ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*np.ones(1,nt))+sqrt(Su(nmi,inxyi)*df*2)*(Q(:,1,nmi)*np.ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*np.ones(1,nt)))
            
            V(inxyi,:)=V(inxyi,:)+sum(sqrt(Sv(nmi,inxyi)*df*2)*(P(:,2,nmi)*np.ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*np.ones(1,nt))+sqrt(Sv(nmi,inxyi)*df*2)*(Q(:,2,nmi)*np.ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*np.ones(1,nt)))
            
            W(inxyi,:)=W(inxyi,:)+sum(sqrt(Sw(nmi,inxyi)*df*2)*(P(:,3,nmi)*np.ones(1,nt)).*cos(wn(:,nmi)*tt+kjxj*np.ones(1,nt))+sqrt(Sw(nmi,inxyi)*df*2)*(Q(:,3,nmi)*np.ones(1,nt)).*sin(wn(:,nmi)*tt+kjxj*np.ones(1,nt)))


        U(inxyi,:)=U(inxyi,:)+Uav(inxyi); # Add the mean velocity

        ## Extract the coordinates and frequency information
        # x and y coordinates vector at the inflow plane
        X=M(:,1)
        Y=M(:,2)
        Z=M(:,3)
         
        nd=size(X,1); # overall no of points
        fmin=fmax/nm/2; # Min Frequency
        df=(fmax-fmin)/(nm-1); # Frequency step
        fm=fmin:df:fmax; # Frequency vector (Ver como construir este vecor)
        tt=dtn(0:(nt-1)); # time vector

        ## Prepare the output file according to the format required by STAR CCM+
        fid2=fopen('inletdata_U.csv',’'w') # Abrir archivo CSV para guardar los datos
        fid3=fopen('inletdata_V.csv',’'w') # Abrir archivo CSV para guardar los datos
        fid4=fopen('inletdata_W.csv',’'w') # Abrir archivo CSV para guardar los datos
        csv='X,Y,Z,'

        ## Ver como imprimir estos datos
        fprintf(fid2,csv)
        fprintf(fid2,'ux(m/s)[t=%es],',tt)
        fprintf(fid2,csv) 
        fprintf(fid2,'ux(m/s)[t=%es],',tt)
        fprintf(fid4,csv)
        fprintf(fid4,'wx(m/s)[t=%es],',tt)

        ## Calculate the average velocity, turbulent Intensity, and length scale profiles
        Uav=Uh*(Z/h0u).^alphau
        
        Iu=Iuh*(Z/h0I).^dIu
        Iv=Ivh*(Z/h0I).^dIv
        Iw=Iwh*(Z/h0I).^dIw
        
        Lu=Luh*(Z/h0L).^dLu
        Lv=Lvh*(Z/h0L).^dLv
        Lw=Lwh*(Z/h0L).^dLw ## Generate Wn (nf x nm) matrix, wn has 2.pi.fm mean and rms=2.pi.df
        
        wn=randn(nf,nm)*2*pi*df
        
        for nmi in range(nm)
            wn(:,nmi)=wn(:,nmi)-mean(wn(:,nmi))
            wn(:,nmi)=wn(:,nmi)/std(wn(:,nmi))*2*pi*df
            wn(:,nmi)=wn(:,nmi)+fm(nmi)*2*pi


        ## Calculate the spectrum matrices
        Su=zeros(nm,nd)
        Sv=zeros(nm,nd)
        Sw=zeros(nm,nd)
        
        fms=(-0.5:0.05:0.5)*df
        nfsm=size(fms,2)/2+0.5
        nfs=size(fms,2)
        
    ## Print the velocity vectors
    TableU=[X Y Z U] # Ver como construir esta matriz 
    TableV=[X Y Z V] # Ver como construir esta matriz
    TableW=[X Y Z W] # Ver como construir esta matriz
    
    for i in range(size(TableU,1))
        fprintf(fid2,'\r\n')
        j=1:size(TableU,2)
        fprintf(fid2,'%e,',TableU(i,j))

    for i in range(size(TableV,1))
        fprintf(fid3,'\r\n')
        j=1:size(TableV,2)
        fprintf(fid3,'%e,',TableV(i,j))

    for i in range(size(TableW,1))
        fprintf(fid4,'\r\n')
        j=1:size(TableW,2)
        fprintf(fid4,'%e,',TableW(i,j))
    
    ## Cierra los CSV
    fclose(fid2)
    fclose(fid3)
    fclose(fid4)


    

# Example on using the CDRFG_2015 Function
h0u=0.3644 # Reference height for the mean velocity
h0I=0.3364 # Reference height for the turbulent intensity
h0L=0.254  # Reference height for the length scale

alphau=0.3264 # Power low exponent of the mean velocity
Uh=10.0 # Mean velocity at h0u

Iuh=0.2084 # Longitudinal turbulent intensity at h0I
Ivh=0.1815 # Transverse turbulent intensity at h0I
Iwh=0.1523 # Vertical turbulent intensity at h0I

dIu=-0.1914 # Power low exponent of the longitudinal turbulent intensity 
dIv=-0.1228 # Power low exponent of the longitudinal turbulent intensity
dIw=-0.0048 # Power low exponent of the longitudinal turbulent intensity

Luh=0.302  # Longitudinal length scale at h0L
Lvh=0.0815 # Transverse length scale at h0L
Lwh=0.0326 # Vertical length scale at h0L

dLu=0.473  # Power low exponent of the longitudinal length scale
dLv=0.8813 # Power low exponent of the longitudinal length scale
dLw=1.5390 # Power low exponent of the longitudinal length scale

Cxyz=[10 10 10] # Coherency decay constants in x, y and z directions [1  3] matrix
DGamma=0.3 # Characteristic length used to maintain the coherency
nf=100 # Number of random frequencies in one segment
nm=50 # Number of frequency segments
fmax=100 # Maximum frequency
dt=1/fmax/2/2.5 # Time step
nt=1000 # Number of time steps
M=[np.zeros(10,1) np.zeros(10,1) (0.05:0.1:1)] # Sample coordinate matrix, Matrix of the inflow coordinates [x y z]


CDRFG_2015(h0u,alphau,Uh,h0I,Iuh,Ivh,Iwh,dIu,dIv,dIw,h0L,Luh,Lvh,Iwh,dLu,dLv,dLw,Cxyz,DGamma,nf,nm,fmax,dt,nt,M)