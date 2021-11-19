# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
from Mesa import Agent, Model
import pandas as pd
import numpy as np

class Coche(Agent):
    def __init__(self, id_unico, modelo):
        super().__init__(id_unico, modelo)
        self.id_unico=id_unico
        self.nueva_posicion = None
        self.movimientos = 0
        self.sentidoCOCHE=None
  
    def step(self):
        global randomDireccion
        global auxSwitch

        vecinos = self.model.grid.get_neighbors(
            self.pos,
            moore=False,
            include_center=True)
        for vecino in vecinos:
            if isinstance(vecino,Coche) and self.sentidoCOCHE==vecino.sentidoCOCHE:
                self.nueva_posicion=self.pos
        for vecino in vecinos:
            if isinstance(vecino,Semaforo):
                if (vecino.estadoS==vecino.ROJO or vecino.estadoS==vecino.AMARILLO) and vecino.sentidoSEMAFORO==self.sentidoCOCHE:
                    self.nueva_posicion=self.pos
                    break
                if vecino.estadoS==vecino.VERDE and vecino.sentidoSEMAFORO==self.sentidoCOCHE:
                    randomDireccion=random.randint(1,2)
                    vecinos2 = self.model.grid.get_neighbors(
                        self.pos,
                        moore=False,
                        include_center=True)
                     for vecino2 in vecinos2:
                        if isinstance(vecino, Piso) and vecino.pos==self.pos:
                            vecino.siguiente_estado = vecino.estado
                            if vecino.siguiente_estado==vecino.CALLE:
                                #Se moverá del semáforo dependiendo que sentido tiene la calle
                                if vecino.SENTIDO_CALLE==vecino.SENTIDO_Este:
                                    self.nueva_posicion= tuple(sum(x) for x in zip(self.pos,(0,1)))
                                    self.sentidoCOCHE="E"
                                    break

                                if vecino.SENTIDO_CALLE==vecino.SENTIDO_Oeste:
                                    self.nueva_posicion= tuple(sum(x) for x in zip(self.pos,(0,-1)))
                                    self.sentidoCOCHE="O"
                                    break

                                if vecino.SENTIDO_CALLE==vecino.SENTIDO_Norte:
                                    self.nueva_posicion= tuple(sum(x) for x in zip(self.pos,(1,0)))
                                    self.sentidoCOCHE="N"
                                    break

                                if vecino.SENTIDO_CALLE==vecino.SENTIDO_Sur:
                                    self.nueva_posicion= tuple(sum(x) for x in zip(self.pos,(-1,0)))
                                    self.sentidoCOCHE="S"
                                    break

     def advance(self):
        global auxSwitch
        global switchSemaforo
        global movimientosT
        
        if self.pos != self.nueva_posicion:
            self.movimientos = self.movimientos + 1
            movimientosT=movimientosT+1
        
        if auxSwitch:
            switchSemaforo=False
        
          
        self.model.grid.move_agent(self, self.nueva_posicion)








class Semaforo(Agent):
    ROJO=2
    AMARILLO=3
    VERDE=4

    def __init__(self,pos,modelo,estadoS=ROJO):
        super().__init__(pos,modelo)
        self.x,self.y=pos
        self.estadoS=estadoS
        self.siguienteEstadoS=None
        self.sentidoSEMAFORO=None

    def step(self):
        global switchSemaforo

        vecinos = self.model.grid.get_neighbors(
              self.pos,
              moore=True,
              include_center=False)
        for vecinoSem in vecinos:
            if isinstance(vecinoSem,Coche) and self.sentidoSEMAFORO==vecinoSem.sentidoCOCHE and not switchSemaforo:
                auxSwitch=False
                switchSemaforo=True
                self.siguienteEstadoS=self.VERDE
                break
            else:
                vecinosR = self.model.grid.get_neighbors(
                  self.pos,
                  moore=True,
                  include_center=False)
                for vecinoR in vecinosR:
                    if not isinstance(vecinoR,Coche) and not switchSemaforo:
                        self.siguienteEstadoS=self.AMARILLO
                        
                    else: 
                        self.siguienteEstadoS=self.ROJO

    def advance(self):
        self.estadoS=self.siguienteEstadoS
    
