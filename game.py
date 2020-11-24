# Implementation of classic arcade game Pong
# Note: Run this code live at http://www.codeskulptor.org
# The support for this code is via the codeskulptor interactivity framework which the code relies on.


import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = random.choice([True, False])
RIGHT = not LEFT
paddle1_vel = paddle2_vel = 0
if LEFT == True:
    direction = LEFT
else:
    direction = RIGHT
score1 = score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1, 2]

paddle1_posd = [HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
paddle1_posu = [HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]

paddle2_posd = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT]
paddle2_posu = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]
# if direction is RIGHT, the ball's velocity is upper right, else upper lef
def vel(dir):
    if dir == RIGHT:
        ball_vel[0] = random.randrange(2,6)
    elif dir == LEFT:
        ball_vel[0] = -random.randrange(2, 6)
    ball_vel[1] = -random.randrange(3, 7)

def spawn_ball(directio):
    global ball_pos, ball_vel, direction# these are vectors stored as lists
    directio = random.choice([LEFT, RIGHT])
    vel(directio)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    directio = random.choice([LEFT, RIGHT])
    ball_pos = [WIDTH/2, HEIGHT/2]
    spawn_ball(directio)
def restart1():
    new_game()
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    flag = 1
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'RED', 'WHITE')
    
    
    
    # draw paddles
    canvas.draw_line(paddle1_posd,paddle1_posu, PAD_WIDTH, 'WHITE')
    canvas.draw_line(paddle2_posd,paddle2_posu, PAD_WIDTH, 'WHITE')
    # determine whether paddle and ball collide    
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and paddle1_posd[1] <= ball_pos[1] and paddle1_posu[1] >= ball_pos[1]:
        ball_vel[0] = -1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
        flag = 0
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and paddle2_posd[1] <= ball_pos[1] and paddle2_posu[1] >= ball_pos[1]:
        ball_vel[0] = -1.1 * ball_vel[0]
        ball_vel[1] = 1.1 * ball_vel[1]
        flag = 0
        
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if flag == 1:
            ball_pos = [WIDTH/2, HEIGHT/2]
            spawn_ball(direction)
            score1 += 1
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if flag == 1:
            ball_pos = [WIDTH/2, HEIGHT/2]
            spawn_ball(direction)
            score2 += 1
    
    # draw scores
    
    canvas.draw_text(str(score1), [WIDTH/4, 40], 30, 'YELLOW')
    
    canvas.draw_text(str(score2), [3*WIDTH/4, 40], 30, 'YELLOW')
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_posd[1] > 0 and paddle1_posu[1] < HEIGHT or  paddle1_posd[1] == 0 and paddle1_vel <0 or paddle1_posu[1] == HEIGHT and paddle1_vel > 0:
        paddle1_posd[1] -= paddle1_vel
        paddle1_posu[1] -= paddle1_vel
    if paddle2_posd[1] > 0 and paddle2_posu[1] < HEIGHT or  paddle2_posd[1] == 0 and paddle2_vel <0 or paddle2_posu[1] == HEIGHT and paddle2_vel > 0:
        paddle2_posd[1] -= paddle2_vel
        paddle2_posu[1] -= paddle2_vel
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 5
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 5
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = -5
     

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart1, 100)

# start frame
new_game()
frame.start()
