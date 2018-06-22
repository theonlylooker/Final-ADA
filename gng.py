# -*- encoding: utf-8 -*-
from grafo import *
from topologia  import topologia
import operator


class gng():
    def __init__(self,topologia):
        self.topologia = topologia
        self.grafo = Grafo()
        self.senal = []
        nodo1=self.grafo.addNodo1(1,[random.randint(1,600),random.randint(1,600)],0)
        nodo2=self.grafo.addNodo1(1,[random.randint(1,600),random.randint(1,600)],0)
        print("Crear nodos iniciales: ")
        print('\t',nodo1.posicion,nodo2.posicion)
        self.grafo.addConexion(nodo1,nodo2)
        self.edadMax=5
        self.iteracion=0
        self.alpha=0.5  #Factor de aumento en nuevos nodos
        self.betha=0.6  
        
	



    def start(self):

        tam=[600,600]
        pantalla=pg.display.set_mode(tam)
        reloj=pg.time.Clock()
        pg.font.init()
        cerrar=False

        while not cerrar:
            for evento in pg.event.get():
                if evento.type==pg.QUIT:
                    cerrar= True

            pantalla.fill(pg.color.Color('black'))

            #Generar la senal (un elemento random de la topologia)
            signal= random.choice(self.topologia)
            
            #Encontramos los 2 mas cercanos a la senal
            nodo1,nodo2,dist=self.grafo.findCercanos(signal)
            print(signal)

            #Aumentar el error del nodo mas cercano
            nodo1.error+=dist

            #Movemos al nodo mas cercano hacia la senal
            e=0.3  #Factor de movimiento (algo asi como la velocidad)
            nodo1.mover(e,signal)

            #Movemos a todos los vecinos hacia la senal
            for vecino in nodo1.vecinos:
                vecino[0].mover(e,signal)
                vecino[1].edad+=1
            
            #Revisamos si los dos nodos del principio tienen conexion
            arista=nodo1.tieneVecino(nodo2)
            if arista: #Si la tienen se reinicia su edad
                arista.edad=0
            else:     #Si no se crea una nueva conexion
                self.grafo.addConexion(nodo1,nodo2)
            

            #Se revisan todas las aristas para ver si hay una muy vieja 
            ar=self.grafo.aristas[:]
            for arista in ar:
                if arista.edad>self.edadMax:   #Si encontramos una borramos sus conexiones
                    self.grafo.deleteConexionA(arista)
            ar=[]

            #Agregar nodo si no se excedio el limite
            if self.iteracion%10==0 and len(self.grafo.nodos)<=800:
                #Encontrar el nodo con error maximo
                nodoU=self.grafo.getNodeErrorMax()
                #Encontrar el nodo vecino de nodoU con el error maximo
                nodoV , conexion=self.grafo.getNodeErrorMaxByNodo(nodoU)

                #Encontrar la posicion media
                posMedia=nodoU.posMedia(nodoV)
                #Crear un nodo entre los dos
                nodoR=self.grafo.addNodo1(1,posMedia,0)

                #Conectar nodoR a nodoU y nodoV y borrar la conexion entre nodoU y nodoV
                self.grafo.addConexion(nodoU,nodoR)
                self.grafo.addConexion(nodoR,nodoV)
                self.grafo.deleteConexionA(conexion)

                #Modificar los errores de U, V y R
                nodoU.error*=self.alpha
                nodoV.error*=self.alpha
                nodoR.error=nodoU.error

                #Reducir los errores de todos los nodos del grafo
                for nodo in self.grafo.nodos:
                    nodo.error-=self.betha*nodo.error
            
            #Si excedio el limite GG
            if len(self.grafo.nodos)==500:

                print("Termino\n")
                print("Numero de nodos",len(self.grafo.nodos))

                input("Presione una tecla para cerrar")
                # for nodo in self.grafo.nodos:
                #     print(nodo.id,  [i[0].id for i in nodo.vecinos])
                return

            for arista in self.grafo.aristas:
                pg.draw.line(pantalla,pg.color.Color('red'),arista.nodos[0].posicion,arista.nodos[1].posicion,1)

            for nodo in self.grafo.nodos:
                pg.draw.circle(pantalla,pg.color.Color('blue'), list(map(int,nodo.posicion)),3)
                #text_to_screen(pantalla,nodo.id,nodo.posicion)

            for punto in self.topologia:
                pg.draw.circle(pantalla,pg.color.Color('white'),punto,6)



            pg.display.flip()
            reloj.tick(5)
            


            



        
        print("Cercanos:",nodo1.posicion,nodo2.posicion,dist)
