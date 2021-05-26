import tkinter
import random
import neat
from PIL import Image,ImageTk
import os

CWD = os.getcwd()
OBJECT_DIAMETER = 18
VERS = 33
COLUMN = 22
CANVAS_WIDTH = OBJECT_DIAMETER * COLUMN
CANVAS_HEIGHT = OBJECT_DIAMETER * VERS
UPDATE_DELAY_TIME = 200
MAX_GENERATION_AMOUNT = 20

def draw():
    g_canvas.delete("all")
    for column_id in range(COLUMN):
        for vers_id in range(VERS):
            x = column_id*OBJECT_DIAMETER
            y = vers_id*OBJECT_DIAMETER
            if g_grid[column_id][vers_id] == True:
                g_canvas.create_image((x,y),image = g_potato.widget,anchor = "nw")

def update():
    g_snake.movement()
    if exit_game == True:
        draw()
        window.quit()
        window.destroy()
    else:
        draw()
        window.after(UPDATE_DELAY_TIME,update)

def key_input(event):
    if event.char == "d" and g_snake.direction != "west":
        g_snake.direction = "east"
    if event.char == "a" and g_snake.direction != "east":
        g_snake.direction = "west"
    if event.char == "w" and g_snake.direction != "south":
        g_snake.direction = "north"
    if event.char == "s" and g_snake.direction != "north":
        g_snake.direction = "south"

def init():
    global g_canvas, g_grid, window, COLUMN, VERS, exit_game
    window = tkinter.Tk()
    window.resizable(False,False)
    g_canvas = tkinter.Canvas(width = CANVAS_WIDTH,height = CANVAS_HEIGHT)

    exit_game = False
    
    Potatoes.texture = Image.open(os.path.join(CWD,"..","..","kropka.jpg"))

    g_canvas.grid(column = 0, row = 0)

    g_canvas.bind("<Key>", key_input)
    g_canvas.focus_set()
    
    g_grid = []
    for x in range(COLUMN):
        verses = []
        g_grid.append(verses)
        for y in range(VERS):
            verses.append(False)

class Potatoes:
    def __init__(self):
        self.widget = ImageTk.PhotoImage(Potatoes.texture)
        self.location_x = random.randint(0,COLUMN-1)
        self.location_y = random.randint(0,VERS-1)

        while g_grid[self.location_x][self.location_y] == True:
            self.location_x = random.randint(0,COLUMN-1)
            self.location_y = random.randint(0,VERS-1)
        
        g_grid[self.location_x][self.location_y] = True

    def die(self):
        g_grid[self.location_x][self.location_y] = False
        
        self.location_x = random.randint(0,COLUMN-1)
        self.location_y = random.randint(0,VERS-1)

        g_grid[self.location_x][self.location_y] = True

class Snake:
    def __init__(self):
        self.location_x = 11 #poprawić
        self.location_y = 16 #poprawić
        self.direction = "east"
        self.parts = []
        self.parts.append(Snake_parts(self.location_x,self.location_y))

    def movement(self):
        global exit_game
        if self.direction == "east":
            self.location_x += 1
        if self.direction == "west":
            self.location_x -= 1
        if self.direction == "south":
            self.location_y += 1
        if self.direction == "north":
            self.location_y -= 1

        if self.location_x == COLUMN or self.location_y == VERS:
            exit_game = True
        else:
            if g_grid[self.location_x][self.location_y] == False:
                if self.location_x < 0 or self.location_y < 0:
                    exit_game = True
                else:
                    self.parts.insert(0,Snake_parts(self.location_x,self.location_y))
                    self.parts.pop().die()
            else:
                if not (self.location_x == g_potato.location_x and self.location_y == g_potato.location_y):
                    exit_game = True
                else:
                    self.eat_potatoe()

    def eat_potatoe(self):
        global g_potato
        self.parts.insert(0,Snake_parts(self.location_x,self.location_y))
        g_potato = Potatoes()

class Snake_parts:
    def __init__(self,x,y):
        self.location_x = x
        self.location_y = y   
        
        g_grid[self.location_x][self.location_y] = True

    def die(self):
        g_grid[self.location_x][self.location_y] = False

def gameplay():   
    global g_snake, g_potato
    init()
    g_snake = Snake()
    g_potato = Potatoes()
    update()

    window.mainloop()

def fitness_function(l_genomes, l_config):
    for id_genom, genome in l_genomes:
        genome.fitness = 0

config_path = os.path.join(CWD,"TextFile1.txt")
g_config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                            neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
population = neat.Population(g_config)

population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

winners = population.run(fitness_function, MAX_GENERATION_AMOUNT)

gameplay()
gameplay()