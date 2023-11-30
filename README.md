# Basic_TUI
This is a basic terminal-based ui engine made with python.

# GUIDELINES
- HOST and PORT must be the same on both sides
- Server will always respond with `<data>;;<printable>`
- A window must be created in order to create buttons
- client messages will have parameters separated by a semicolon (`;`)

# Create Window Message (W)
## Creation Elements
| Name | API Variable Name | API Default Value | Description | Syntax |
|---|---|---|---|---|
| X-Position | `x` | `1` | X-Position of the top-left corner of the window | `<num>x` |
| Y-Position | `y` | `1` | Y-Position of the top-left corner of the window | `<num>y` |
| Prompt | `prompt` | `"Window"` | A `\n` separated string of text lines | `{<str>}` |
| Window Width | `win_wid` | `50` | How many characters wide the window is | `<num>W` |
| Window Height | `win_hgt` | `7` | How many characters tall the window is | `<num>H` |
| Vertical Align | `v_align` | `"T"` | Where on the y-axis the prompt should be placed (top, center, bottom) | `[T\|C\|B]` |
| Horizontal Align | `h_align` | `"M"` | Where on the x-axis the prompt should be placed (left, middle, right) | `[L\|M\|R]` |
| Prompt Text Color | `p_txt_col` | `"0"` | The color of the prompt's text | `[K\|R\|G\|Y\|B\|M\|C\|W]f` |
| Window Background Color | `win_bg_col` | `"0"` | The background color for the window | `[K\|R\|G\|Y\|B\|M\|C\|W]f` |
| Highlighted Text Color | `hgl_txt_col` | `"K"` | The color of the text when highlighted (used for buttons) | `[K\|R\|G\|Y\|B\|M\|C\|W]s` |
| Highlighted Background Color | `hgl_bg_col` | `"W"` | The color of the background when text is highlighted (Used for buttons) | `[K\|R\|G\|Y\|B\|M\|C\|W]S` |
| Parent Window | `parent_win` | `-1` | The index of the window to revert to when this one exits (-1 if first window)| `<num>p` |
### Example Window Creation Message
- `b"W;-1p;1x;2y;Kf;Wb;{Hello World\nThis is a prompt};T;M;30W;10H;RS;Cs"`
### Example API Uses
- `tui_api.create_window(socket, win_wid = 60, win_hgt = 5, prompt = "This is a prompt", hgl_txt_col = "R", hgl_bg_col = "W")`
- `tui_api.create_window(socket)`
- `tui_api.create_window(socket, 20, 3, 60, 7, "T", "L", "Hello World", parent_win = 0)`

# Change Window Message (C)
## Creation Elements
| Name | API Variable Name | Description | Syntax |
|---|---|---|---|
| Window Index | `idx` | Index returned by the Window Creation Message of the window you wish to change to | `<num>` |
### Example Window Change Message
- `b"C;1"`
### Example API Use
- `tui_api.change_window(socket, 1)`

# Create Button Message (B)
## Creation Elements
| Name | API Variable Name | API Default Value | Description | Syntax |
|---|---|---|---|---|
| X-Position | `x` | `1` | X-Position of the first text character | `<num>x` |
| Y-Position | `y` | `1` | Y-Position of the first text character | `<num>y` |
| Text | `txt` | `"Button"` | Text to be put on the button | `{<str>}` |
| Text Color | `txt_col` | `"0"` | The color of the text | `[K\|R\|G\|Y\|B\|M\|C\|W]f` |
| Background Color | `bg_col` | `"0"` | The background color for the text (padding included) | `[K\|R\|G\|Y\|B\|M\|C\|W]b` |
| Padding | `pad` | `1` | How many blocks of padding will surround text | `<num>p` |
### Example Button Creation Message
- `b"B;1p;4x;24y;Wf;Bb;{Hello World}"`
### Example API Uses
- `tui_api.create_button(socket, 4, 24, "Hello World", "W", "B", 1)`
- `tui_api.create_button(socket, txt = "Shorthand")`
- `tui_api.create_button(socket)`

# Search Button Message (S)
## Creation Elements
| Name | Description | Syntax |
|---|---|---|
| Text | Text of the button to go to | `{<str>}` |
| Search X-Axis | Search to the right or left for nearest button (+x is right) | `[+\|-]x` |
| Search Y-Axis | Search down or up for the nearest button (+y is down) | `[+\|-]y` |
### Example Button Selection Messages
- `b"S;{Hello World}"`
- `b"S;-y"`
### Example API Uses
- `tui_api.search_button(socket, "Hello World")`
- `tui_api.search_button(socket, "+x")`

(**) ***Note that you can only use one method of selection***

# Exit Window Message (E)
## Creation Elements
| Name | API Variable Name | Description | Syntax |
|---|---|---|---|
| Window Index | `idx` | Index returned by the Window Creation Message of the window you wish to exit | `<num>` |
### Example Window Exitting Messages
- `b"E;0"`
### Example API Use
- `tui_api.exit_window(socket, 0)`

UML UPDATE: Exit now clears previous window from screen
# UML
![UML](images/Microservice_UML.png)
