from tkinter import *
import time
import random

HEIGHT = 500
WIDTH = 800
F_HEIGHT = 80

RADIUS = 20
ball_vel = [0, 0]

PAD_WIDTH = 30
PAD_HEIGHT = 100
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

def new_game():
    global score1, score2
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)
    while score1 < 5 and score2 < 5:
        draw()
        window.update()
        window.after(10)
    
    if score1 == 5:
        winner = "Player 1 wins"
    elif score2 == 5:
        winner = "Player 2 wins"
    c.create_text(WIDTH/2, HEIGHT/4*3, text=winner, font=("Arial", 40, "bold"), fill='white')

def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60.0
    elif direction == LEFT:
        ball_vel[0] = - random.randrange(120, 240) / 60.0
    
    ball_vel[1] = - random.randrange(60, 180) / 60.0

def keydown(e):
    global paddle1_vel, paddle2_vel
        
    if e.keysym == 'e':
        paddle1_vel = -5
    elif e.keysym == 'd':
        paddle1_vel = 5
    elif e.keysym == 'o':
        paddle2_vel = -5
    elif e.keysym == 'l':
        paddle2_vel = 5

    return True
    
def keyup(e):
    global paddle1_vel, paddle2_vel
        
    if e.keysym == 'e':
        paddle1_vel = 0
    elif e.keysym == 'd':
        paddle1_vel = 0
    elif e.keysym == 'o':
        paddle2_vel = 0
    elif e.keysym == 'l':
        paddle2_vel = 0

    return True

def draw():
    global ball_pos, ball_vel, ball, score1, score2, paddle1_pos, paddle2_pos, c

    c.delete("all")

    # draw mid line and gutters
    c.create_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], fill="white")
    c.create_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], fill="white")
    c.create_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], fill="white")

    # update ball
    # determine whether paddle and ball collide
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 

    if ball_pos[1]-RADIUS <= 0 or ball_pos[1]+RADIUS >= HEIGHT:
        ball_vel[1] = - ball_vel[1]       

    if ball_pos[0]-RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= (paddle1_pos-HALF_PAD_HEIGHT) and ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score2 += 1        
            spawn_ball(RIGHT)
        
    if ball_pos[0]+RADIUS >= WIDTH-PAD_WIDTH:
        if ball_pos[1] >= (paddle2_pos-HALF_PAD_HEIGHT) and ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)

    # draw ball
    ball = c.create_oval(ball_pos[0]-RADIUS, ball_pos[1]-RADIUS, ball_pos[0]+RADIUS, ball_pos[1]+RADIUS, fill="white")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos - HALF_PAD_HEIGHT + paddle1_vel) <= 0 or (paddle1_pos + HALF_PAD_HEIGHT + paddle1_vel) >= HEIGHT:
        pass
    else:
        paddle1_pos += paddle1_vel
    
    if (paddle2_pos - HALF_PAD_HEIGHT + paddle2_vel) <= 0 or (paddle2_pos + HALF_PAD_HEIGHT + paddle2_vel) >= HEIGHT:
        pass
    else:
        paddle2_pos += paddle2_vel
     
    # draw paddles
    paddle1 = c.create_rectangle(0, paddle1_pos-HALF_PAD_HEIGHT, PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT, fill="white")
    paddle2 = c.create_rectangle(WIDTH-PAD_WIDTH, paddle2_pos-HALF_PAD_HEIGHT, WIDTH, paddle2_pos+HALF_PAD_HEIGHT, fill="white")

    # draw scores
    c.create_text(WIDTH/4, HEIGHT/8, text=str(score1), font=("Arial", 40), fill='white')
    c.create_text(WIDTH/4*3, HEIGHT/8, text=str(score2), font=("Arial", 40), fill='white')

window = Tk()
window.title('Pong!')
window.resizable(width=FALSE, height=FALSE)

c = Canvas(window, width=WIDTH, height=HEIGHT, bg='black')
c.pack()
c_text = "Player 1 controls the left hand paddle using the \"E\" (up) and \"D\" (down) keys\n\
Player 2 controls the right hand paddle using the \"O\" (up) and \"L\" (down) keys\n\
First player to 5 points wins the game"
c.create_text(WIDTH/2, HEIGHT/2, text=c_text, font=("Arial", 12, "bold"), fill='white')
c.bind_all('<KeyPress>', keydown)
c.bind_all('<KeyRelease>', keyup)

f = Frame(width=WIDTH, height=F_HEIGHT)
f.pack()

b_start = Button(f, text="START NEW GAME", font=("Arial", 12, "bold"), command=new_game)
b_quit = Button(f, text="QUIT", font=("Arial", 12, "bold"), command=exit)
b_start.grid(row=1, column=1)
b_quit.grid(row=1, column=2)
