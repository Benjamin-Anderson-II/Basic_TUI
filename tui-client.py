# echo-client

import socket
from getkey import getkey, keys
import tui_api as api

HOST = "127.0.0.1" # Server's hostname or IP addr
PORT = 65432 # Same port as server

#(x, y)
yes_pos = (18, 7)
yes_txt = "NEW WIN"
no_pos  = (48, 11)
no_txt  = "EXIT"
nothing_pos = (31, 6)
nothing_txt = "NOTHING"

cursor_pos = [yes_pos[0], yes_pos[1]]
highlight = ('G', 'B')

def decode_pos(pos):
    cursor_pos[0] = int(pos[1:-1].split(",")[0])
    cursor_pos[1] = int(pos[1:-1].split(",")[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print("\033[2J")
    prompt = "This is the first line, and will act as a header.\nThis is after a newline character."
    main_win = api.create_window(s, 10, 3, 70, 15, "M", "T", prompt, "K", "W", "C", "R", -1)
    curr_win = main_win
    api.create_button(s, yes_pos[0], yes_pos[1], yes_txt, "W", "K")
    api.create_button(s, no_pos[0], no_pos[1], no_txt, "W", "K")
    api.create_button(s, nothing_pos[0], nothing_pos[1], nothing_txt, "W", "K")
    decode_pos(api.search_button(s, "{%s}" % (yes_txt)))

    while True:
        print(f"\033[H{curr_win}")
        key = getkey()
        if key == keys.LEFT:
            decode_pos(api.search_button(s, "-x"))
        if key == keys.RIGHT:
            decode_pos(api.search_button(s, "+x"))
        if key == keys.UP:
            decode_pos(api.search_button(s, "-y"))
        if key == keys.DOWN:
            decode_pos(api.search_button(s, "+y"))
        if key == keys.ENTER:
            if cursor_pos[0] == yes_pos[0] + 10 and cursor_pos[1] == yes_pos[1] + 3:
                curr_win = api.create_window(s, 20, 6, 40, 10, "M", "C", "NEW WINDOW", "M", "G", "", "", main_win)
                decode_pos(api.create_button(s, 36, 1, "X", "R", "B"))
            elif(curr_win == 1 and cursor_pos[0] == 36+20 and cursor_pos[1] == 1+6):
                    curr_win = api.exit_window(s, curr_win)
            elif cursor_pos[0] == no_pos[0] + 10 and cursor_pos[1] == no_pos[1] + 3:
                break
                
        if key == 'q':
            if curr_win != main_win:
                curr_win = api.exit_window(s, curr_win)
            else:
                print("\033[H\033[0m", end = "")
                break
