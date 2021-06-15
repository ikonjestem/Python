import turtle
import winsound


wn = turtle.Screen()
wn.title("Pong by ikon")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

paused = False


    

# paddle a
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("purple")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)



#paddle b
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("pink")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)


#ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("yellow")
ball.penup()
ball.goto(0, 0)

#zmienne punktow
score_a = 0
score_b = 0




#ustalanie wartosci ruchu pilki
ball.dx = 1
ball.dy = 1

#punkty
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("PlayerA: 0   PlayerB: 0", align="center", font=("Courier", 24, "normal"))


# funkcja ruszajaca paletkami
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


#  dodanie klawisza do ruchu
wn.listen()

wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")

wn.onkeypress(paddle_b_up, "Up") #strzałki
wn.onkeypress(paddle_b_down, "Down")






#main game loop
while True:
    

    wn.update()

    if not paused:

   
    #Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)


    # Ustalanie granic i odbijanie od nich
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1 #odwraca kierunek
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write("PlayerA: {}   PlayerB: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("PlayerA: {}   PlayerB: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    #odbijanie
        if (ball.xcor() > 340 and ball.xcor() < 350 and (ball.ycor() < paddle_b.ycor() + 60 and ball.ycor() > paddle_b.ycor() -60)):
            ball.setx(340)
            ball.dx *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

        if (ball.xcor() < -340 and ball.xcor() > -350 and (ball.ycor() < paddle_a.ycor() + 60 and ball.ycor() > paddle_a.ycor() -60)):
            ball.setx(-340)
            ball.dx *= -1
            winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
  
        if (score_a == 10):
            winsound.PlaySound("win.wav", winsound.SND_ASYNC) 
            paused = True
            


        if (score_b == 10):
            winsound.PlaySound("win.wav", winsound.SND_ASYNC) 
            paused = True

            
    else:
        wn.update()



   
