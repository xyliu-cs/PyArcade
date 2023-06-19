from turtle import Turtle, Screen
import random
import time

#global variables
winning = 0
lastkey = 'right'
motion = 'right'
bodylen = 6
foodpos = {}
segment=[]
bodypos = []
delay = 200
startTime = 0
contact = 0

#initiate the screen
screen = Screen()
screen.title('The Snake by @LiuXiaoyuan')
screen.setup(width=660, height=740)
screen.tracer(0)

#initiate the snake's head
head = Turtle()
head.shape('square')
head.color('red')
head.up()
head.goto((0,-40))
head.direction = 'right'

#create the pen for drawing
foodpen = Turtle()
foodpen.hideturtle()

#create the monster
monster = Turtle()

#creater several pens for drawing 
titlepen1 = Turtle()
titlepen1.up()
titlepen1.hideturtle()

titlepen2 = Turtle()
titlepen2.up()
titlepen2.hideturtle()

titlepen3 = Turtle()
titlepen3.up()
titlepen3.hideturtle()

titlepen4 = Turtle()
titlepen4.up()
titlepen4.hideturtle()

def initMonster():
    monster.shape('square')
    monster.color('purple')
    while True:
        x = random.randint(-230, 230)
        y = random.randint(-270, 190)
        if head.distance((x,y)) >= 200 and (x,y) not in bodypos:
            monster.up()
            monster.setpos((x,y))
            break       

def drawBorder():
    pen = Turtle()
    pen.pensize(2)
    pen.up()
    pen.setpos((-250,290))
    pen.down()
    pen.forward(500)
    pen.right(90)
    pen.forward(80)
    pen.right(90)
    pen.pensize(4)
    pen.forward(500)
    pen.right(90)
    pen.pensize(2)
    pen.forward(80)
    pen.backward(580)
    pen.right(90)
    pen.forward(500)
    pen.left(90)
    pen.forward(500)
    pen.hideturtle()


    titlepen1.setpos((-200, 220))
    titlepen1.write('Contact: ',font=('Arial', 14, 'normal'))
    titlepen1.setpos((-50, 220))
    titlepen1.write('Time: ', font=('Arial', 14, 'normal'))
    titlepen1.setpos((80, 220))
    titlepen1.write('Motion: ', font=('Arial', 14, 'normal'))

def setFood():
    global foodpos
    for i in range(1,10):
        x = random.randrange(-245, 245, 5)
        y = random.randrange(-280, 205, 5)
        if (x,y) not in foodpos:
            foodpos[i] = (x,y)

def drawfood(somedic):
    foodpen.clear()
    for i in somedic:
        foodpen.up()
        foodpen.goto(somedic[i])
        foodpen.setheading(270)
        foodpen.forward(10)
        foodpen.down()
        foodpen.write(i, font=('Arial', 12, 'normal'))
    foodpen.hideturtle()

def goUp():
    global motion
    head.direction = "up"
    motion = 'up'
  
def goDown():
    global motion
    head.direction = "down"
    motion = 'down'
    
def goLeft():
    global motion
    head.direction = "left"
    motion = 'left'
   
def goRight():
    global motion
    head.direction = "right"
    motion = 'right'

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

def pause():
    global motion, lastkey
    if head.direction in ['up', 'down', 'left', 'right']:
        lastkey = head.direction
        head.direction = 'stop'
        motion = 'stop'
    elif head.direction == 'stop':
        head.direction = lastkey
        motion = lastkey
    elif head.direction == 'blocked' and motion != 'stop':
        motion = 'stop'
    elif head.direction == 'blocked' and motion == 'stop':
        motion = lastkey
    
def eatFood():
    global winning, bodylen, foodpos
    foodnew = foodpos.copy()
    for i in foodpos:
        if head.distance(foodpos[i]) < 15:
            bodylen += i
            foodnew.pop(i)
    if len(foodnew) == 0 and len(segment) == 50:
        winning = 1
    if len(foodnew) != len(foodpos):
        drawfood(foodnew)
        foodpos = foodnew

def runMonster():
    global winning, contact
    if winning == 1:
        return
    pace = random.randint(150,500)
    x = monster.xcor() - head.xcor()
    y = monster.ycor() - head.ycor()
    if x!= 0:
        x1 = x / abs(x)
    else:
        x1 = x
    if y!= 0:
        y1 = y / abs(y)
    else:
        y1 = y

    for i in bodypos:
        if monster.distance(i) <= 10:
            contact += 1
            break

    (x0,y0) = monster.pos()
    if monster.distance(head.position()) <= 20:
        winning = -1
    else:
        if abs(y) >= abs(x):
            monster.setpos((x0, y0-(y1*20)))
        else:
            monster.setpos((x0-(x1*20),y0))
        screen.ontimer(runMonster, pace)
        screen.update()
    
def runSnake():
    global delay, lastkey
    if winning == -1 or winning == 1:
        return
    elif head.direction == 'stop' or head.direction == 'blocked':
        screen.ontimer(runSnake,200)
    else:
        move()
        eatFood()
        x = head.xcor()
        y = head.ycor()
        if y > 200 or y < -280 or x < -250 or x >250:
            head.undo()
            head.direction = 'blocked'
            lastkey = motion
        else:        
            head.color('black', 'orange')
            segment.append(head.stamp())
            bodypos.append(head.pos())
            head.color('red')
            if len(segment) > bodylen:
                head.clearstamp(segment.pop(0))
                bodypos.pop(0)
            elif len(segment) < bodylen:
                delay = 400
            else:
                delay = 200
            
        screen.ontimer(runSnake, delay)
        screen.update()

def drawTitle():
    if winning == 1:
        titlepen1.up()
        (x,y) = head.pos()
        titlepen1.goto(x-80,y)
        titlepen1.color('red')
        titlepen1.write('Winner!',font=('Arial', 12, 'normal'))
    elif winning == -1:
        titlepen1.up()
        (x,y) = head.pos()
        titlepen1.goto(x-80,y)
        titlepen1.color('purple')
        titlepen1.write('Failed!',font=('Arial', 12, 'normal'))
    else:
        titlepen2.clear()
        titlepen3.clear()
        titlepen4.clear()

        titlepen2.setpos((-120, 220))
        titlepen2.write(str(contact), font=('Arial', 14, 'normal'))
        titlepen3.setpos((20,220))
        currentTime = time.time()
        titlepen3.write(int(currentTime-startTime), font=('Arial', 14, 'normal'))
        titlepen4.setpos((160,220))
        titlepen4.write(motion, font=('Arial', 14, 'normal'))
        screen.ontimer(drawTitle, 1000)
    
def main(x,y):
    global startTime
    startTime = time.time()
    setFood()
    drawfood(foodpos)
    screen.onkey(goUp, "Up")
    screen.onkey(goDown, "Down")
    screen.onkey(goRight, "Right")
    screen.onkey(goLeft, "Left")
    screen.onkey(pause, 'space')
    screen.listen()
    drawTitle()
    runSnake()
    runMonster()
    screen.exitonclick()

def drawTitle0():
        titlepen2.setpos((-120, 220))
        titlepen2.write(str(contact), font=('Arial', 14, 'normal'))
        titlepen3.setpos((20,220))
        titlepen3.write(int(0), font=('Arial', 14, 'normal'))
        titlepen4.setpos((160,220))
        titlepen4.write('paused', font=('Arial', 14, 'normal'))
        titlepen4.setpos((-220,100))
        titlepen4.write(' >>> Welcome to the Snake by Liu Xiaoyuan...\n >>> You are going to use four arrow keys to move the snake. \
                        \n >>> Consume all the food items before the monster catches you!\
                        \n >>> Click anywhere on the screen to start the game. \
                        \n >>> After start, click again to exit. GL & HF!', font=('Arial', 12, 'normal'))

def initGame():
    drawBorder()
    initMonster()
    drawTitle0()
    screen.update()
    screen.onclick(main)

if __name__ == '__main__':
    initGame()
    screen.mainloop()

