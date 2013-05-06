# -*- coding: utf-8 -*-
from __future__ import division
#######################################
#                                     #
# Probabilidad y Estadistica          #
# Humberto José Ojeda Malavé          #
# C.I: 20.185.583 (Adrián Bottini C2) #
# Francisco Vergara                   #
# C.I: 17389551 (José Sosa C1)        #
#                                     #
#  Progamando en Python 2.7.3         #
#######################################
import sys
import random
import threading
import time
from math import*
from random import*
from random import random, uniform
from random import expovariate, seed
from time import sleep
#---#
ValoresEntrada=[ ]              #Arreglo que contendra las variables de entrada
#---#
class Inicio:   
     global ValoresEntrada
     def __init__(self):
          self.i = 0                       
     def readFile(self):     #Este metodo se encarga de leer el archivo de entrada y leer las variables              
          while True:
               try:
                    archivo = open("entrada.txt", "r")      
                    break
               except:                                         
                    import sys
                    print "error al abrir el archivo"
                    sys.exit(-1)            
          while True:                     
               linea = archivo.readline()      #Leo del archivo
               ValoresEntrada.append(linea)    #Sino es caso especial guardo la linea en el arreglo de variables de entrada
               if (len(linea))==0:
                    break
               self.i = self.i+1
#---#
def Distancia(Array,x):
     i=0
     espa=0
     tam=len(Array)
     r=(x+1)%tam
     while ((Array[r]=="_")):
          espa=espa+1
          r=(r+1)%tam
     #print "espa es ",espa
     return espa
#---#
def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
#---#
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()
    
#---------------------Main--------------------#
print "Leyendo Datos del archivo de Entrada...\n"
#---#
ini = Inicio()  
ini.readFile() 
print "Realizando Simulacion...\n"
#---#
#for i in progressbar(range(100), "Procesando: ", 40):
#    time.sleep(0.1) # long computation
#---#
cantidadCeldas= int (ValoresEntrada[1]) # M celdas (longitud de la via):
numeroVehiculos = int (ValoresEntrada[3]) # N vehiculos en la via:
velocidadMaxima = int (ValoresEntrada[5])# VMax Velocidad maxima permitida (celdas/seg):
probabilidadFrenar = float (ValoresEntrada[7])# p probabilidad de frenar para cada vehiculo en cada instante de tiempo:
tiempoSimulacion = int (ValoresEntrada[9])# TS seg tiempo a simular (duracion de la corrida):
duracionTraza = int (ValoresEntrada[11])# DurTraza seg tiempo que dura la traza:
#---#
traza=open("traza.txt","w")
salida=open("salida.txt","w")
#declaro un arreglo con las M celdas lleno de _
via = []
car = []
#---#
for i in range(cantidadCeldas):
    via.append("_")
    car.append("_")
#---#
#declaro un arreglo con las Vmax celdas lleno de 0 que esto me ayudara a la hora de imprimir la traza
velo = []
#---#
for i in range(velocidadMaxima+1):
    velo.append(0)
#---#
#declaro un arreglo con las cantidad de celdas - vehiculos lleno de 0 que esto me ayudara a la hora de imprimir la salida
EspacioTotal=cantidadCeldas-numeroVehiculos
dist = []
#---#
for i in range(EspacioTotal+1):
    dist.append(0)   
#---#
#espacio entre caeda vehiculo
espacio = (EspacioTotal)/numeroVehiculos
#
espacioCarros = int(espacio)
#
aux=numeroVehiculos
#
can=numeroVehiculos
#
cont=0
cuenta=0
#---#
for i in range(cantidadCeldas):
          if (i==0):
               via[i]=velocidadMaxima
               car[i]=aux
               aux=aux-1
               cuenta=cuenta+1
          else:
               if ((cont==espacioCarros) and(cuenta != can)):
                    via[i]=velocidadMaxima
                    car[i]=aux
                    aux=aux-1
                    cont=0
                    cuenta=cuenta+1
               else:
                         cont=cont+1
#---#
proba= probabilidadFrenar*100
#print "proba ",proba
vel=0
#print "Via antes de de hacer los pasos......"
#print via
traza.writelines(str(0)+":", )
#---#
for i in range (cantidadCeldas):
	traza.writelines(str(via [i]))
traza.writelines("\n")
#---#
CV=0
for instante in range(tiempoSimulacion):
     #print "i vale",TIEMPO 
     #aceleracion
     for i in range(cantidadCeldas):
          if (via[i]!="_"):
               x=min(via[i]+1,velocidadMaxima)
               via[i]=x;
               #---#
   #  print"ACELERAR...."
   #  print via
     #frenado
     for i in range(cantidadCeldas):
          if (via[i]!="_"):
               y=Distancia(via,i)
               x=min(via[i],y)
               via[i]=x;
               #---#
  #print "FRENAR...."
  #print via
     #Aleatoriedad:
     proba= probabilidadFrenar*100    
     frenado = []
     for i in range(cantidadCeldas):
          if (via[i]!="_"):
               rand= float(uniform(0.0,100.0))
               if (rand<=proba):
                    vel=max(via[i]-1,0)
                    via[i]=vel
                    frenado.append(car[i])   
               else:
                    via[i]=via[i]
                      #---#      
     #print "ALETORIEDAD...."
     #print via
     #---#                
     #JUSTO ANTE DE MOVERME HAGO LOS CALCULOS DE CUANTOS ESPACIOS VACIOS TENGO Y CUANTAS VELOCIDADES HAY:
     for i in range(cantidadCeldas):
          if(via[i]!="_"):
               Velc=via[i]
               velo[Velc]=velo[Velc]+1
               y=Distancia(via,i)
               dist[y]=dist[y]+1
     #---#
     #print carros
     R=cantidadCeldas   
     # AQUI EMPEZAMOS A MOVERNOS
     carros=[] #se crea un arreglo de carros para almacenar
     #---#
     for i in range (numeroVehiculos): #a cada carro se le asigna una especie de ID
          carros.append(i)
     #---#
     c=0
     for i in range (cantidadCeldas): #llenamos el arreglo de carros
          if(via[i]!="_"):
               carros[c]=i
               c+=1
     #---#
     for i in range (c): #for en el rango del arreglo de carros
          speed= via [carros [i]] #guardo la velicidad del primero carro 
          via [carros[i]]= "_" #a la posicion que tenia la velocidad le asigno "_"
          RT=car[carros[i]]
          car[carros[i]]= "_"
          carros [i]= carros [i]+ speed #actualizo el arreglo de carros con la nueva posicion que tomo
          if (carros[i]>=R): 
               CV=CV+1
               carros[i]= carros[i]%R
               car[carros[i]]= RT
               via [carros [i]]= speed #luego me muevo el numero conduzco segun la velocidad      
          else:
               car[carros[i]]= RT
               via [carros [i]]= speed
     #---#
     '''
     ejemplo: via = [2___0_1_2_] el arreglo de carros es [0,2,4,6,8]
     recorro en el rango de carros que seria 5
     for i in 5:
          speed = via [carros [0]] =2
          via [carros [0]]= '_' arreglo via quedaria [__0_0_1_2_]
          carros [0]= carros [0]+ speed= 0+2 => quedaría asi el arreglo de carros [2,2,4,6,8]
          via [carros [0]]= speed = 2 la via queda [__2_0_1_2_]
     '''
     #---#
     arregloCarros=" "
     for i in range (cantidadCeldas):
          if(car[i]!="_"):
               #print saco
               arregloCarros=arregloCarros+" "+str(car[i])
     #---#
     frenadosAlazar=" "
     S=len(frenado)
     frenado.sort()
     #---#
     for i in range(S):
          frenadosAlazar=frenadosAlazar+" "+str(frenado[i])
     #---#
     #print"CONDUCCION"
     #print via
     #print frenado
     if (instante<duracionTraza):
          traza.writelines(str(instante+1)+":",)
          for i in range (cantidadCeldas):
               traza.writelines(str(via [i]))
          traza.writelines(" carros #"+str(arregloCarros)+" frenaron al azar:"+str(frenadosAlazar)+"\n")
traza.close()
#---#
#print CV
#print velo
print "Fin de Simulacion...\n"
print "Revisar archivos generados: traza.txt y salida.txt"
data =  []
data2 = []
X=len(velo)
Y=len(dist)
Numero=float(numeroVehiculos*tiempoSimulacion)
Q = '%.6f' %(CV/tiempoSimulacion)
salida.writelines("VS = "+ str(CV)+" carros llegaron al final de la via en TS = "+str (tiempoSimulacion)+" seg de tiempo simulado\n")
salida.writelines("Flujo promedio de vehiculos Q = "+ str (Q) +" carros/seg\n")
salida.writelines("Velocidad (celdas/seg) Frecuencia relativa:\n")
for i in range(X):
     velocidad=velo[i]
     imp=str(i)
     total='%.6f' %(velocidad/Numero)
     data.append(total)
     salida.writelines(imp+" "+str(total)+"\n")
salida.writelines("Distancia (celdas libres delante) Frecuencia relativa: \n")
#---#
for i in range(Y):
     distancia=dist[i]
     imp=str(i)
     total='%.6f' %(distancia/Numero)
     data2.append(total)
     salida.writelines(imp+" "+str(total)+"\n")
salida.close()
#---#
