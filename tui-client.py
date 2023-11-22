# echo-client

import socket
from getkey import getkey, keys

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

def send_btn_msg(soc, x, y, txt, highlight_fg, highlight_bg):
    send = "C;1p;%dx;%dy;{%s};%sb;%sf" % (x, y, txt, highlight_bg, highlight_fg)
    soc.sendall(send.encode())
    btn = soc.recv(1024).decode("utf-8").split(";;")
    print(btn[1])
    decode_pos(btn[0])
    return btn[0]

def send_window_msg(soc, x, y, window_width, window_height, v_align, h_align, txt, 
                    txt_width, txt_height, fg, bg, highlight_fg, highlight_bg, prev_win):
    send = "W;%dx;%dy;%dW;%dH;%s;%s;{%s};%dw;%dh;%sf;%sb;%ss;%sS;%dp" % (x, 
                                                                         y, 
                                                                         window_width, 
                                                                         window_height, 
                                                                         v_align, 
                                                                         h_align, 
                                                                         txt, 
                                                                         txt_width, 
                                                                         txt_height, 
                                                                         fg, 
                                                                         bg, 
                                                                         highlight_fg, 
                                                                         highlight_bg, 
                                                                         prev_win)
    soc.sendall(send.encode())
    win = soc.recv(4096)
    #print(win[2:].decode("utf-8"))
    s = win.decode("utf-8").split(";;")
    print(s[1])
    return int(s[0])

def send_select_msg(soc, search):
    send = "S;%s" % (search)
    soc.sendall(send.encode())
    btn = soc.recv(1024).decode("utf-8").split(";;")
    print(btn[1])
    decode_pos(btn[0])
    return btn[0]

def send_exit_win_msg(soc, idx):
    send = "E;%d" % (idx)
    soc.sendall(send.encode())
    win = soc.recv(4096).decode("utf-8").split(";;")
    print(win[1])
    return int(win[0])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print("\033[2J")
    prompt = "This is the first line, and will act as a header.\nThis is after a newline character."
    main_win = send_window_msg(s, 10, 3, 70, 15, "M", "T", prompt, 60, 2, "K", "W", "C", "R", -1)
    curr_win = main_win
    send_btn_msg(s, yes_pos[0], yes_pos[1], yes_txt, "W", "K")
    send_btn_msg(s, no_pos[0], no_pos[1], no_txt, "W", "K")
    send_btn_msg(s, nothing_pos[0], nothing_pos[1], nothing_txt, "W", "K")
    send_select_msg(s, "{%s}" % (yes_txt))

    while True:
        print(f"\033[H{curr_win}")
        key = getkey()
        if key == keys.LEFT:
            send_select_msg(s, "-x")
        if key == keys.RIGHT:
            send_select_msg(s, "+x")
        if key == keys.UP:
            send_select_msg(s, "-y")
        if key == keys.DOWN:
            send_select_msg(s, "+y")
        if key == keys.ENTER:
            if cursor_pos[0] == yes_pos[0] + 10 and cursor_pos[1] == yes_pos[1] + 3:
                curr_win = send_window_msg(s, 20, 6, 40, 10, "M", "C", "NEW WINDOW", 20, 1, "M", "G", "", "", main_win)
                send_btn_msg(s, 36, 1, "X", "R", "B")
            elif(curr_win == 1 and cursor_pos[0] == 36+20 and cursor_pos[1] == 1+6):
                    curr_win = send_exit_win_msg(s, curr_win)
            elif cursor_pos[0] == no_pos[0] + 10 and cursor_pos[1] == no_pos[1] + 3:
                break
                
        if key == 'q':
            if curr_win != main_win:
                curr_win = send_exit_win_msg(s, curr_win)
            else:
                print("\033[H\033[0m", end = "")
                break
