'''
Sotero Osuna Gómez - A01251505
26 de Noviembre del 2021

Simulación de tráfico en una cuadra con una intersección de dos calles 
de doble sentido
'''

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler

from agents import Car, TrafficLight, Street


class TrafficBlock(Model):
    def __init__(self, N = 4, TI = 5, width=8, height=8):
        environment = [ ["E", "E", "E", "TC", "E", "E", "E", "S"],
                ["N", "Non", "Non", "S", "N", "Non", "Non", "S"],
                ["N", "Non", "Non", "S", "N", "Non", "Non", "S"],
                ["N", "W", "W", "TWTL", "TWTR", "W", "W", "RC"],
                ["LC", "E", "E", "TWBL", "TWBR", "E", "E", "S"],
                ["N", "Non", "Non", "S", "N", "Non", "Non", "S"],
                ["N", "Non", "Non", "S", "N", "Non", "Non", "S"],
                ["N", "W", "W", "W", "BC", "W", "W", "W", "W"]
                ]
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = BaseScheduler(self)
        self.ti = TI
        self.it = 0

        #Añadir calle
        for i in range(0, len(environment)):
            for j in range(0, len(environment)):
                a = Street(i*8+j, self, environment[i][j])
                self.grid.place_agent(a, (i,j))

        #Añadir semáforos
        
        tf1 = TrafficLight(65, self, "TL")
        tf2 = TrafficLight(66, self, "TR")
        tf3 = TrafficLight(67, self, "BL")
        tf4 = TrafficLight(68, self, "BR")
        self.grid.place_agent(tf1, (3,3))
        self.grid.place_agent(tf2, (3,4))
        self.grid.place_agent(tf3, (4,3))
        self.grid.place_agent(tf4, (4,4))
        self.schedule.add(tf1)
        self.schedule.add(tf2)
        self.schedule.add(tf3)
        self.schedule.add(tf4)
        

        #Añadir autos
        for i in range(0, N):
            a = Car(69+i, self, self.random.randrange(2,5,2))
            x = self.random.choice([0,1,2,5,6,7])
            y = self.random.choice([0,3,4,7])
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)
        print("car setup ok")

        self.running = True

    def step(self):
        self.it += 1
        self.schedule.step()
        agentInfo = {"Cars": [], "TrafficLights": []}
        for i in range(0, 4):
            tfls = self.schedule.agents[i].status
            info = [tfls]
            agentInfo["TrafficLights"].append(info)
        for i in range(0, self.num_agents):
            xy = self.schedule.agents[4+i].pos
            p = [2.5 + 5*xy[0], 0.75, 37.5-5*xy[1], self.schedule.agents[4+i].orientation]
            agentInfo["Cars"].append(p)
        return agentInfo

    def run_model(self, n):
        for i in range(n):
            self.step()
            print(self.it)

