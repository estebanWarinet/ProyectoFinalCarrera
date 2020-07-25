from scipy import signal
import matplotlib.pyplot as plt

def DecaimientoCoherencia (vector, primerPt, SegundoPt, fs = 5e1, ventana='hann'):
    ## Pruebo el calculo de la coherencia entre dos puntos
    ## fs: Frecuencia de muestreo de las series temporales x e y.
    f, Cxy = signal.coherence(vector[primerPt,:], vector[SegundoPt,:],fs,ventana)
    plt.semilogy(f, Cxy)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('Coherence')
    plt.show()