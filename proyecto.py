# -*- coding: utf-8 -*-
from SimPy.Simulation import * #libreria de SymPy
from random import * #generadores

#generador
class Generador(Process):
    def genVotantes(self,tasaLleg):
        global comp, i, n #contador de votante comun y especial
        comp=True
        while (comp==True): #Comparación para detener la generación de votantes al superar la duración de la jornada
            aux=random() #Se genera un valor random entre 0 y 1 para utilizarlo en la generación de votantes especiales
            tLleg=expovariate(tasaLleg) #
            yield hold,self,tLleg #Se espera un tiempo t para generar un nuevo votante
            if (now()<duraJornada):
                if (aux <= porcenEspe):
                    vot=Votante(name="Votante Especial %d"%(n))
                    #print n
                    activate(vot,vot.votar(tVotante=2)) #Se genera un nuevo votante especial
                    n+=1
                elif (aux>porcenEspe):
                    vot=Votante(name="Votante %d"%(i))
                    activate(vot,vot.votar(tVotante=1)) #Se genera un nuevo votante
                    i+=1
            else:
                comp=False


#votante
class Votante(Process):
    def votar(self,tVotante):
        global cont10, cont1020, cont2030, cont30x
        #print "%7.4f %s: Llegando a votar "%(float(now()/3600.0),self.name)
        votCol=len(sala.waitQ)
        votSal=len(sala.activeQ)
        if (itera==1):
            traza.write("%.6f"%float(now()/3600.0)+"|"+str(votCol)+"|"+str(votSal)+"\n") #Imprimir traza
        llego=now()
        if (tVotante==2):
            yield request,self,sala,2 #Llega un nuevo votante especial, verifica capacidad de la sala.. en caso de no obtener el recurso se coloca de primero en la cola
            #print "%7.4f %s: Pase a votar "%(float(now()/3600.0),self.name)
            entro=now()
            tcol=entro-llego
            #print tcol/60
            if (tcol>=0.0 and tcol<600.0):
                cont10+=1
            elif (tcol>=600.0 and tcol<1200.0):
                cont1020+=1
            elif (tcol>=1200.0 and tcol<=1800.0):
                cont2030+=1
            elif (tcol>1800.0):
                cont30x+=1
            monTiempoColaSala.observe(tcol)
        else:
            yield request,self,sala,1 #Llega un nuevo votante, verifica capacidad de la sala.. en caso de no obtener el recurso se quedara esperando en la cola
            #print "%7.4f %s: Pase a votar "%(float(now()/3600.0),self.name)
            entro=now()
            tcol=entro-llego
            #print tcol/60
            if (tcol>=0.0 and tcol<600.0):
                cont10+=1
            elif (tcol>=600.0 and tcol<1200.0):
                cont1020+=1
            elif (tcol>=1200.0 and tcol<=1800.0):
                cont2030+=1
            elif (tcol>1800.0):
                cont30x+=1
            monTiempoColaSala.observe(tcol)
        
        t=triangular(tminSAI,tmodSAI,tmaxSAI)
        if (tVotante==2):
            #print "%7.4f %s: Llegue al SAI "%(float(now()/3600.0),self.name)
            yield request,self,SAI,2
            #print "%7.4f %s: Pase al SAI "%(float(now()/3600.0),self.name)
            t=2*t
            monSAI.observe(t)
            yield hold,self,t #Tiempo que tarda en autenticarse en el SAI (especial)
        else:
            #print "%7.4f %s: Llegue al SAI "%(float(now()/3600.0),self.name)
            yield request,self,SAI,1
            #print "%7.4f %s: Pase al SAI "%(float(now()/3600.0),self.name)
            monSAI.observe(t)
            yield hold,self,t #Tiempo que tarda en autenticarse en el SAI
        yield release,self,SAI

        t=triangular(tminMV,tmodMV,tmaxMV)
        if (tVotante==2):
            yield request,self,MV,2
            t=2*t
            monMV.observe(t)
            yield hold,self,t #Tiempo que tarda en pasar por la maquina de votacion(especial)
        else:
            yield request,self,MV,1
            monMV.observe(t)
            yield hold,self,t #Tiempo que tarda en pasar por la maquina de votacion
        yield release,self,MV

        t=triangular(tminURNA,tmodURNA,tmaxURNA)
        if (tVotante==2):
            yield request,self,Urna,2
            t=2*t
            monURNA.observe(t)
            yield hold,self,t #Tiempo que tarda en depositar el voto en la urna(especial)
        else:
            yield request,self,Urna,1
            monURNA.observe(t)
            yield hold,self,t #Tiempo que tarda en depositar el voto en la urna
        yield release,self,Urna

        t=triangular(tminCUAD,tmodCUAD,tmaxCUAD)
        if (tVotante==2):
            yield request,self,Cuaderno,2
            t=2*t
            monCUAD.observe(t)
            yield hold,self,t #Tiempo que tarda en firmar el cuaderno de votacion(especial)
        else:
            yield request,self,Cuaderno,1
            monCUAD.observe(t)
            yield hold,self,t #Tiempo que tarda en firmar el cuaderno de votacion
        yield release,self,Cuaderno

        t=triangular(tminTINTA,tmodTINTA,tmaxTINTA)
        if (tVotante==2):
            yield request,self,Tinta,2
            t=2*t
            monTINTA.observe(t)
            yield hold,self,t #Tiempo que tarda en marcar el dedo con la tinta indeleble(especial)
        else:
            yield request,self,Tinta,1
            monTINTA.observe(t)
            yield hold,self,t #Tiempo que tarda en marcar el dedo con la tinta indeleble
        yield release,self,Tinta
        
        yield release,self,sala
        votCol=len(sala.waitQ)
        votSal=len(sala.activeQ)
        if (itera==1):
            traza.write("%.6f"%float(now()/3600.0)+"|"+str(votCol)+"|"+str(votSal)+"\n") #Imprimir traza
            #saliendo=now()
            #monCierre.observe(saliendo)

        #print "%7.4f %s: Saliendo de votar "%(float(now()/3600.0),self.name)


#entrada
def entrada(nombreArch):
    global numCorr, duraJornada, tasaLlegada, capaSala, porcenEspe, tminSAI, tmodSAI, tmaxSAI, tminMV, tmodMV, tmaxMV, tminURNA, tmodURNA, tmaxURNA, tminCUAD, tmodCUAD, tmaxCUAD, tminTINTA, tmodTINTA, tmaxTINTA
    entrada=open(nombreArch, 'r')
    entrada.readline()
    numCorr=int(entrada.readline().split()[0]) 	#Cantidad de corridas
    #print numCorr
    entrada.readline()
    duraJornada=float(entrada.readline().split()[0])*3600.0	#Duracion de la jornada en horas (convertida a segundos) de tiempo simulado
    #print duraJornada
    entrada.readline()
    tasaLlegada=float(entrada.readline().split()[0])/60.0	#Tasa de llegada de los votantes por minuto (convertida a segundos)
    #print tasaLlegada
    entrada.readline()
    capaSala=float(entrada.readline().split()[0])	#Capacidad de la sala
    #print capaSala
    entrada.readline()
    porcenEspe=float(entrada.readline().split()[0])/100.0	#% de votantes especiales
    #print porcenEspe
    entrada.readline()
    tminSAI=float(entrada.readline().split()[0])	#Tiempo minimo que tarda en autenticarse en el SAI en segundos
    #print tminSAI
    entrada.readline()
    tmodSAI=float(entrada.readline().split()[0])	#Tiempo medio que tarda en autenticarse en el SAI en segundos
    #print tmodSAI
    entrada.readline()
    tmaxSAI=float(entrada.readline().split()[0])	#Tiempo maximo que tarda en autenticarse en el SAI en segundos
    #print tmaxSAI
    entrada.readline()
    tminMV=float(entrada.readline().split()[0])	#Tiempo minimo que tarda en pasar por la maquina de votacion en segundos
    #print tminMV
    entrada.readline()
    tmodMV=float(entrada.readline().split()[0])	#Tiempo medio que tarda en pasar por la maquina de votacion en segundos
    #print tmodMV
    entrada.readline()
    tmaxMV=float(entrada.readline().split()[0])	#Tiempo maximo que tarda en pasar por la maquina de votacion en segundos
    #print tmaxMV
    entrada.readline()
    tminURNA=float(entrada.readline().split()[0])	#Tiempo minimo que tarda en depositar el voto en la urna en segundos
    #print tminURNA
    entrada.readline()
    tmodURNA=float(entrada.readline().split()[0])	#Tiempo medio que tarda en depositar el voto en la urna en segundos
    #print tmodURNA
    entrada.readline()
    tmaxURNA=float(entrada.readline().split()[0])	#Tiempo maximo que tarda en depositar el voto en la urna en segundos
    #print tmaxURNA
    entrada.readline()
    tminCUAD=float(entrada.readline().split()[0])	#Tiempo minimo que tarda en firmar el cuaderno de votacion en segundos
    #print tminCUAD
    entrada.readline()
    tmodCUAD=float(entrada.readline().split()[0])	#Tiempo medio que tarda en firmar el cuaderno de votacion en segundos
    #print tmodCUAD
    entrada.readline()
    tmaxCUAD=float(entrada.readline().split()[0])	#Tiempo maximo que tarda en firmar el cuaderno de votacion en segundos
    #print tmaxCUAD
    entrada.readline()
    tminTINTA=float(entrada.readline().split()[0])	#Tiempo minimo que tarda en marcar el dedo con la tinta indeleble en segundos
    #print tminTINTA
    entrada.readline()
    tmodTINTA=float(entrada.readline().split()[0])	#Tiempo medio que tarda en marcar el dedo con la tinta indeleble en segundos
    #print tmodTINTA
    entrada.readline()
    tmaxTINTA=float(entrada.readline().split()[0])	#Tiempo maximo que tarda en marcar el dedo con la tinta indeleble en segundos
    #print tmaxTINTA


#corrida
def corrida():
    global votCol, votSal, monCierre, monSAI, monMV, monURNA, monCUAD, monTINTA, i, n, monTiempoColaSala, realDuraJornada, cont10, cont1020, cont2030, cont30x
    #monCierre=Monitor(name="Monitor de hora de cierre")
    monSAI=Monitor(name="Monitor de SAI")
    monMV=Monitor(name="Monitor de MV")
    monURNA=Monitor(name="Monitor de URNA")
    monCUAD=Monitor(name="Monitor de CUAD")
    monTINTA=Monitor(name="Monitor de TINTA")
    monTiempoColaSala=Monitor(name="Monitor del tiempo en cola de la sala")
    sala.waitMon.reset()
    cont10=0
    cont1020=0
    cont2030=0
    cont30x=0
    votCol=0
    realDuraJornada=1
    votSal=0
    i=0
    n=0
    initialize() #inicializa el reloj de simulacion
    g=Generador() #instanciando al generador
    activate(g,g.genVotantes(tasaLleg=tasaLlegada),at=0.0) #invocando al generador
    simulate(until=5000000) #inicio de la simulacion hasta un tiempo grande
    
    realDuraJornada=now()
    realJornadaSalida=realDuraJornada/3600
    ocupSAI=(100*monSAI.total())/realDuraJornada
    ocupMV=(100*monMV.total())/realDuraJornada
    ocupURNA=(100*monURNA.total())/realDuraJornada
    ocupCUAD=(100*monCUAD.total())/realDuraJornada
    ocupTINTA=(100*monTINTA.total())/realDuraJornada
    lMaxCola=max(sala.waitMon.yseries())           # Revisar bien wtf hace el len no entiendo por que restarle 1
    tMaxCola=max(monTiempoColaSala.yseries())/60
    u=i+n
    #print monSAI.yseries()
    #print monSAI.total()
    #print cont10
    #print cont1020
    #print cont2030
    #print cont30x
    #print cont10+cont1020+cont2030+cont30x
    #print u
    porcent10=(cont10*100.0)/float(u)
    porcent1020=(cont1020*100.0)/float(u)
    porcent2030=(cont2030*100.0)/float(u)
    porcent30x=(cont30x*100.0)/float(u)
    #print porcent10
    #print porcent1020
    #print porcent2030
    #print porcent30x
    #haha=porcent10+porcent1020+porcent2030+porcent30x
    #print haha
    
    #monitoreando para medidas
    medMonSAI.observe(ocupSAI)
    medMonMV.observe(ocupMV)
    medMonURNA.observe(ocupURNA)
    medMonCUAD.observe(ocupCUAD)
    medMonTINTA.observe(ocupTINTA)
    medMonPorcent10.observe(porcent10)
    medMonPorcent1020.observe(porcent1020)
    medMonPorcent2030.observe(porcent2030)
    medMonPorcent30x.observe(porcent30x)
    medMonJornada.observe(realJornadaSalida)
    medMonTiempoColaSala.observe(tMaxCola)
    medMonLargoColaSala.observe(lMaxCola)
    medMonCantVotantes.observe(u)
    medMonCantVotantesEsp.observe(n)
    #print u
    #print n
    #print lMaxCola
    #print tMaxCola
    #print ocupSAI
    #print ocupMV
    #print ocupURNA
    #print ocupCUAD
    #print ocupTINTA
    msj=str(itera)+"|%.6f"%realJornadaSalida+"|%d"%u+"|%d"%n+"|%d"%lMaxCola+"|%.6f"%tMaxCola+"|%.6f"%porcent10+"|%.6f"%porcent1020+"|%.6f"%porcent2030+"|%.6f"%porcent30x+"|%.6f"%ocupSAI+"|%.6f"%ocupMV+"|%.6f"%ocupURNA+"|%.6f"%ocupCUAD+"|%.6f"%ocupTINTA+"\n"
    salida.write(msj)


#monitores para medidas
def monMedidas():
    global medMonJornada, medMonSAI, medMonMV, medMonURNA, medMonCUAD, medMonTINTA, medMonTiempoColaSala, medMonLargoColaSala, medMonCantVotantes, medMonCantVotantesEsp, medMonPorcent10, medMonPorcent1020, medMonPorcent2030, medMonPorcent30x
    medMonJornada=Monitor(name="Monitor de duracion de la jornada")
    medMonSAI=Monitor(name="Monitor de SAI para medidas")
    medMonMV=Monitor(name="Monitor de MV para medidas")
    medMonURNA=Monitor(name="Monitor de URNA para medidas")
    medMonCUAD=Monitor(name="Monitor de CUAD para medidas")
    medMonTINTA=Monitor(name="Monitor de TINTA para medidas")
    medMonTiempoColaSala=Monitor(name="Monitor del tiempo en cola de la sala para medidas")
    medMonLargoColaSala=Monitor(name="Monitor largo de cola de la sala para medidas")
    medMonCantVotantes=Monitor(name="Monitor de la cantidad de votantes para medidas")
    medMonCantVotantesEsp=Monitor(name="Monitor de la cantidad de votantes especiales para medidas")
    medMonPorcent10=Monitor(name="Monitor de MV para medidas")
    medMonPorcent1020=Monitor(name="Monitor de URNA para medidas")
    medMonPorcent2030=Monitor(name="Monitor de CUAD para medidas")
    medMonPorcent30x=Monitor(name="Monitor de TINTA para medidas")

def percentil(self, per): #calcular percentil
    a=int(len(self.yseries())*(per/100.0))
    #print a
    b=sorted(self.yseries())
    #print b
    if a%2==0:
        result=b[a]
    else:
        result=(b[a]+b[a+1])/2
    return result

def calcMedidas(self,final): #calcular medidas para monitores
    promedio=self.mean()
    minimo=min(self.yseries())
    maximo=max(self.yseries())
    per25=percentil(self,25)
    per50=percentil(self,50)
    per75=percentil(self,75)
    medidas.write("%.6f"%promedio+"|%.6f"%minimo+"|%.6f"%maximo+"|%.6f"%per25+"|%.6f"%per50+"|%.6f"%per75+"|%s\n"%final)

def impMedidas():
    calcMedidas(medMonJornada,"Hora_cierre_mesa")
    calcMedidas(medMonCantVotantes,"Cantidad_votantes_atendidos")
    calcMedidas(medMonCantVotantesEsp,"Cantidad_votantes_especiales")
    calcMedidas(medMonLargoColaSala,"Longitud_maxima_cola_fuera_sala")
    calcMedidas(medMonTiempoColaSala,"Tiempo_max_espera_en_cola")
    calcMedidas(medMonPorcent10,"porcentaje_votantes_esperan_<10min")
    calcMedidas(medMonPorcent1020,"porcentaje_votantes_esperan_10a20min")
    calcMedidas(medMonPorcent2030,"porcentaje_votantes_esperan_20a30min")
    calcMedidas(medMonPorcent30x,"porcentaje_votantes_esperan_>30min")
    calcMedidas(medMonSAI,"porcentaje_ocupacion_SAI")
    calcMedidas(medMonMV,"porcentaje_ocupacion_MV")
    calcMedidas(medMonURNA,"porcentaje_ocupacion_Urna")
    calcMedidas(medMonCUAD,"porcentaje_ocupacion_Cuaderno")
    calcMedidas(medMonTINTA,"porcentaje_ocupacion_Tinta")

#programa principal normal **************************
entrada('entrada.txt')

#recursos
sala=Resource(capacity=capaSala,monitored=True,qType=PriorityQ) #Instancia y define la sala con capacidad +1 y activa los monitores
SAI=Resource(capacity=1,monitored=True,qType=PriorityQ)
MV=Resource(capacity=1,monitored=True,qType=PriorityQ)
Urna=Resource(capacity=1,monitored=True,qType=PriorityQ)
Cuaderno=Resource(capacity=1,monitored=True,qType=PriorityQ)
Tinta=Resource(capacity=1,monitored=True,qType=PriorityQ)

#inicializo monitores de medidas
monMedidas()

#archivos
traza=open("traza.txt", "w")
traza.write("hora|votantes_en_cola|votantes_en_sala\n")
salida=open("salida.txt", "w")
salida.write("N_Corrida|Hora_Cierre|Cantidad_Votantes|Cantidad_votantes_especiales|L_Max_Cola|T_Max_Cola|porcentaje_Menos_10_min|porcentaje_de_10_a_20_min|porcentaje_de_20_a_30_min|porcentaje_mas_30_min|porcentaje_Ocupa_SAI|porcentaje_Ocupa_MV|porcentaje_Ocupa_Urna|porcentaje_Ocupa_Cuaderno|porcentaje_Ocupa_Tinta\n")
medidas=open("medidas.txt", "w")
medidas.write("Promedio|Minimo|Maximo|Percentil_25|Percentil_50|Percentil_75|Medidas\n")

#iteraciones
global itera
itera=1
while (itera<=numCorr):
    corrida()
    itera+=1
impMedidas()
salida.close()
traza.close()
medidas.close()

#programa capa sala -1 **********************

#recursos
sala=Resource(capacity=capaSala-1,monitored=True,qType=PriorityQ) #Instancia y define la sala con capacidad +1 y activa los monitores
SAI=Resource(capacity=1,monitored=True,qType=PriorityQ)
MV=Resource(capacity=1,monitored=True,qType=PriorityQ)
Urna=Resource(capacity=1,monitored=True,qType=PriorityQ)
Cuaderno=Resource(capacity=1,monitored=True,qType=PriorityQ)
Tinta=Resource(capacity=1,monitored=True,qType=PriorityQ)

#inicializo monitores de medidas
monMedidas()

#archivos
traza=open("traza_menos.txt", "w")
traza.write("hora|votantes_en_cola|votantes_en_sala\n")
salida=open("salida_menos.txt", "w")
salida.write("N_Corrida|Hora_Cierre|Cantidad_Votantes|Cantidad_votantes_especiales|L_Max_Cola|T_Max_Cola|porcentaje_Menos_10_min|porcentaje_de_10_a_20_min|porcentaje_de_20_a_30_min|porcentaje_mas_30_min|porcentaje_Ocupa_SAI|porcentaje_Ocupa_MV|porcentaje_Ocupa_Urna|porcentaje_Ocupa_Cuaderno|porcentaje_Ocupa_Tinta\n")
medidas=open("medidas_menos.txt", "w")
medidas.write("Promedio|Minimo|Maximo|Percentil_25|Percentil_50|Percentil_75|Medidas\n")

#iteraciones
itera=1
while (itera<=numCorr):
    corrida()
    itera+=1
impMedidas()
salida.close()
traza.close()
medidas.close()

#programa capa sala +1 *****************************
#recursos
sala=Resource(capacity=capaSala+1,monitored=True,qType=PriorityQ) #Instancia y define la sala con capacidad +1 y activa los monitores
SAI=Resource(capacity=1,monitored=True,qType=PriorityQ)
MV=Resource(capacity=1,monitored=True,qType=PriorityQ)
Urna=Resource(capacity=1,monitored=True,qType=PriorityQ)
Cuaderno=Resource(capacity=1,monitored=True,qType=PriorityQ)
Tinta=Resource(capacity=1,monitored=True,qType=PriorityQ)

#inicializo monitores de medidas
monMedidas()

#archivos
traza=open("traza_mas.txt", "w")
traza.write("hora|votantes_en_cola|votantes_en_sala\n")
salida=open("salida_mas.txt", "w")
salida.write("N_Corrida|Hora_Cierre|Cantidad_Votantes|Cantidad_votantes_especiales|L_Max_Cola|T_Max_Cola|porcentaje_Menos_10_min|porcentaje_de_10_a_20_min|porcentaje_de_20_a_30_min|porcentaje_mas_30_min|porcentaje_Ocupa_SAI|porcentaje_Ocupa_MV|porcentaje_Ocupa_Urna|porcentaje_Ocupa_Cuaderno|porcentaje_Ocupa_Tinta\n")
medidas=open("medidas_mas.txt", "w")
medidas.write("Promedio|Minimo|Maximo|Percentil_25|Percentil_50|Percentil_75|Medidas\n")

#iteraciones
itera=1
while (itera<=numCorr):
    corrida()
    itera+=1
impMedidas()
salida.close()
traza.close()
medidas.close()
