#! /usr/bin/python3

#Snake game in python originally written by EngineerMan on YouTube. The game was originally written in Python 2 and thus needed some bug fixes to work python3. The game was made slightly more robust by adding some error checking, and missing functions before ending the curses window which can mess up the terminal afterwards. Added a simple score counter to make the game more replayable. Github/YorkieWoW.

#play instructions. open terminal, cd into game dir and use ./snake.py to run

#import modules
import random #rng
import curses #window

score = 0 #variable to track score
s = curses.initscr() #init screen
s.keypad(True) # recommended from curses docs
curses.noecho() #recommended from curses docs
curses.cbreak() #recommended from curses docs
curses.curs_set(0) #dont show cursor on screen
sh, sw = s.getmaxyx() #get window size
w = curses.newwin(sh, sw, 0, 0) # create new window using height width
w.keypad(1) #accept keyboard input 
w.timeout(80) #controls speed of snake. also is essentially the rendering of the game. lower number is more difficult, higher is easier

#create snake start position
snk_x = sw // 4 #needs // in python 3 as / returns a float and causes a crash. Must be whole integers.
snk_y = sh // 2 #same reason as above. anywhere in the code you see // is changed from a / in python2. 

#create snake body
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
] 

food = [sh // 2, sw // 2 ] #create food
w.addch(food[0], food[1], curses.ACS_DIAMOND) #add food to screen. change curses.ACS_ to change what icon the food is.

key = curses.KEY_RIGHT #start direction of the snake

#movement of the snake
while True:
    next_key = w.getch()
    key = key if next_key == -1 else next_key
    #game over conditions if snake touches itself(pause)
    if snake[0] in snake[1:]:
        curses.nocbreak() #recommended from docs
        s.keypad(False) #recommended from docs
        curses.echo() #recommended from docs
        curses.endwin() #now we can close the game
        print(f"GAME OVER! Your score was {score}. Thanks for playing. ") #game over message
        quit() #quits game
              
    #determine new head of snake
    new_head = [snake[0][0], snake[0][1]]
    
    #movement keys. This could use a bit of clean up as it does not have any error handling, so if the user presses any other key than the arrow keys the program will terminate. Also does not factor in opposite movements so hitting UP+DOWN or LEFT+RIGHT simultaneously will cause the program to terminate. It works well enough for basic play in it's current state.  
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    #wrap around edges
    new_head[0] = int(new_head[0]) % (sh - 1)
    new_head[1] = int(new_head[1]) % sw

    #insert new head of snake
    snake.insert(0, new_head)
    #determine if snake has eaten food
    if snake[0] == food:
        score += 1
        food = None
        while food is None:
            nf = [
                random.randint(1, sh - 2),
                random.randint(1, sw - 1)
            ]
            food = nf if nf not in snake else None             
        w.addch(food[0], food[1], curses.ACS_DIAMOND)
    else:
        tail = snake.pop()
        w.addch(tail[0], tail[1], " ")
    #add score to the screen
    w.addstr(sh - 1,0, f"Score:{score}")
    #safe draw of snake head
    if 0 <= snake[0][0] < sh - 1 and 0 <= snake[0][1] < sw:
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
    else:
        curses.nocbreak() #start exit flow if somehow error happens.
        s.keypad(False) #recommended from docs
        curses.echo() #recommended from docs
        curses.endwin() #now we can close the game
        print("You made the snake go out of bounds! Please tell me how you did that?!")
        quit()
