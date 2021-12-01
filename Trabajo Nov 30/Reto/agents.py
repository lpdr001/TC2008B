'''
Sotero Osuna Gómez - A01251505
26 de Noviembre del 2021

Simulación de tráfico en una cuadra con una intersección de dos calles 
de doble sentido
'''
from mesa import Agent

class Street(Agent):

    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.type = type
        self.options = []
        if (type == "N"):
            self.options = [[-1,0]]
        elif (type == "E"):
            self.options = [[0,1]]
        elif (type == "S"):
            self.options = [[1,0]]
        elif (type == "W"):
            self.options = [[0,-1]]
        elif (type == "TWTR"):
            self.options = [[1,0], [0,-1]]
        elif (type == "TWTL"):
            self.options = [[0,-1], [1,0]]
        elif (type == "TWBR"):
            self.options = [[-1,0], [0,1]]
        elif (type == "TWBL"):
            self.options = [[1,0], [0,1]]
        elif (type == "LC"):
            self.options = [[0,1],[-1,0]]
        elif (type == "TC"):
            self.options = [[0,1], [1,0]]
        elif (type == "RC"):
            self.options = [[0,-1], [1,0]]
        elif (type == "BC"):
            self.options = [[0,-1], [-1,0]]
        else:
            self.options = [[0,0]]

class TrafficLight(Agent):
    def __init__(self, unique_id, model,type):
        super().__init__(unique_id, model)
        self.type = type
        self.started = False
        self.original = False
        self.status = 2

    def checkInitialize(self):
        if (self.started == False):
            neighbors = self.model.grid.get_neighborhood(self.pos, False, False, 1)
            for neighbor in neighbors:
                cell = self.model.grid.get_cell_list_contents([neighbor])
                objects = [obj for obj in cell if isinstance(obj, Car)]
                if len(objects) > 0:
                    print("Starting from", self.type)
                    self.started = True
                    self.original = True
                    self.status = 0
                    self.synchronize()
                    break

    def synchronize(self):
        if(self.type == "TR" and self.original == True):
            print(self.pos[0], self.pos[1], self.type)
            cell = self.model.grid.get_cell_list_contents([(4,3)])
            objects = [obj for obj in cell if isinstance(obj, TrafficLight)]
            objects[0].status = self.status
            objects[0].started = True
            cell2 = self.model.grid.get_cell_list_contents([(4,4)])
            objects2 = [obj for obj in cell2 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects2[0].status = 0
            else:
                objects2[0].status = 1
            objects2[0].started = True
            cell3 = self.model.grid.get_cell_list_contents([(3,3)])
            objects3 = [obj for obj in cell3 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects3[0].status = 0
            else:
                objects3[0].status = 1
            objects3[0].started = True

        elif(self.type == "TL" and self.original == True):
            print(self.pos[0], self.pos[1], self.type)
            cell = self.model.grid.get_cell_list_contents([(4,4)])
            objects = [obj for obj in cell if isinstance(obj, TrafficLight)]
            objects[0].status = self.status
            objects[0].started = True
            cell2 = self.model.grid.get_cell_list_contents([(4,3)])
            objects2 = [obj for obj in cell2 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects2[0].status = 0
            else:
                objects2[0].status = 1
            objects2[0].started = True
            cell3 = self.model.grid.get_cell_list_contents([(3,4)])
            objects3 = [obj for obj in cell3 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects3[0].status = 0
            else:
                objects3[0].status = 1
            objects3[0].started = True

        elif(self.type == "BL" and self.original == True):
            print(self.pos[0], self.pos[1], self.type)
            cell = self.model.grid.get_cell_list_contents([(3,4)])
            objects = [obj for obj in cell if isinstance(obj, TrafficLight)]
            objects[0].status = self.status
            objects[0].started = True
            cell2 = self.model.grid.get_cell_list_contents([(4,4)])
            objects2 = [obj for obj in cell2 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects2[0].status = 0
            else:
                objects2[0].status = 1
            objects2[0].started = True
            cell3 = self.model.grid.get_cell_list_contents([(3,3)])
            objects3 = [obj for obj in cell3 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects3[0].status = 0
            else:
                objects3[0].status = 1
            objects3[0].started = True

        elif(self.type == "BR" and self.original == True):
            print(self.pos[0], self.pos[1], self.type)
            cell = self.model.grid.get_cell_list_contents([(3,3)])
            objects = [obj for obj in cell if isinstance(obj, TrafficLight)]
            objects[0].status = self.status
            objects[0].started = True
            cell2 = self.model.grid.get_cell_list_contents([(4,3)])
            objects2 = [obj for obj in cell2 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects2[0].status = 0
            else:
                objects2[0].status = 1
            objects2[0].started = True
            cell3 = self.model.grid.get_cell_list_contents([(3,4)])
            objects3 = [obj for obj in cell3 if isinstance(obj, TrafficLight)]
            if self.status == 1:
                objects3[0].status = 0
            else:
                objects3[0].status = 1
            objects3[0].started = True



    def changeLights(self):
        if (self.original == True):
            if (self.status == 1):
                self.status = 0
            elif (self.status == 0):
                self.status = 1

    def step(self):
        self.checkInitialize()
        print("It",self.model.it, " and TI", self.model.ti, "and modulo", self.model.it % self.model.ti == 0, "and started", self.started)
        print("Original:",self.original)
        if (self.started and (self.model.it % self.model.ti == 0)):
            self.changeLights()
            self.synchronize()
        

class Car(Agent):

    def __init__(self, unique_id, model, velocity):
        super().__init__(unique_id, model)
        self.velocity = velocity
        self.orientation = 0
    
    def updateOrienation(self):
        cellPostition = self.model.grid.get_cell_list_contents([self.pos])
        cell = [obj for obj in cellPostition if isinstance(obj, Street)]
        if cell[0].type == "N" or cell[0].type == "LC" or cell[0].type == "TWBR":
            self.orientation = 3
        elif cell[0].type == "E" or cell[0].type == "TC" or cell[0].type == "TWBL":
            self.ortientation = 0
        elif cell[0].type == "S" or cell[0].type == "RC" or cell[0].type == "TWTR":
            self.orientation = 1
        else:
            self.orientation = 2


    def inCenter(self):
        return (self.pos[0] == 3 or self.pos[0] == 4) and (self.pos[1] == 3 or self.pos[1] == 4)

    def move(self):
        if (self.model.it % self.velocity == 0):
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            options = [obj for obj in this_cell if isinstance(obj, Street)]
            movement = self.random.choice(options[0].options)
            new_position = (self.pos[0] + movement[0], self.pos[1] + movement[1])
            prospect_cell = self.model.grid.get_cell_list_contents([new_position])
            possible_obstacles = [obj for obj in prospect_cell if (isinstance(obj, Car) or isinstance(obj, TrafficLight))]
            for possible_obstacle in possible_obstacles:
                if (isinstance(possible_obstacle, Car)):
                    return
                if (isinstance(possible_obstacle,TrafficLight)):
                    if possible_obstacle.status == 1 and (not self.inCenter()):
                        return
            self.model.grid.move_agent(self, new_position)
            self.updateOrienation()

    def step(self):
        self.move()
