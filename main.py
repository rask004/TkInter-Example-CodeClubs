from functools import partial
import tkinter as tk
from tkinter import ttk
from minesweeper import mines_grid_init, check_grid, get_count_neighbours_mine, get_neighbours_empty, SPACE, MINE, GRID_SIZE, BOOM, MARK, MINE_COUNT

DEBUG = True

BTN_BGROUND_DEFAULT = "#D3D3E3"
BTN_BGROUND_GAME = "#C8C8D8"
BTN_FGROUND_FAIL = "#FFFF77"
BTN_BGROUND_FAIL = "#600000"
BTN_BGROUND_WIN = "#00FFAA"

mines_grid_init()

game_buttons_rows = []
processed = []
found_mines = []

print("MINESWEEPER")
print("number  -  neighbouring mines")
print("*       -  BOOM!! you clicked on a mine")
print("X       -  marked as mine")
print("Left click to check a cell")
print("right click to mark/unmark a cell")
print("Mark all mines, and only mines, to win!")


### event is necessary for bind function (see below), but callback doesn't use it.
def lclick_callback(btn, x: int, y: int, event=None) -> None:
  """callback function for game button left-clicks
  btn        - button left-clicked
  x          - x coordinate on mine grid
  y          - y coordinate on mine grid
  event      - placeholder argument for callback event
  """
  txt = btn.cget('text')
  if txt == MARK:
    return
  result = check_grid(x, y)
  if result == MINE:
    # game fail state
    for row in game_buttons_rows:
      for game_btn in row:
        game_btn.config(style="G-Fail.TButton", state=tk.DISABLED)
    btn.config(text=BOOM)
  else:
    # show blank space or neighbouring mine count. if blank, repeat for
    # neighbours, keep repeating with blank neighbours
    stack = [(x, y, btn)]
    while stack:
      x, y, next_btn = stack.pop()
      count = get_count_neighbours_mine(x, y)
      result = str(count) if count else SPACE
      next_btn.config(text=result,
                      style="G-Pressed.TButton",
                      state=tk.DISABLED)
      processed.append((x, y, next_btn))
      # if DEBUG:
      #   print( "count=", result, "origin=", (x, y), "processed=", len(processed))
      if count == 0:
        neighbours = [(x, y, game_buttons_rows[y][x])
                      for x, y, _ in get_neighbours_empty(x, y)]
        neighbours = [(x, y, b) for x, y, b in neighbours
                      if (x, y, b) not in processed]
        # if DEBUG:
        #   print("\tneighbours=", [(x, y) for x, y, _ in neighbours])
        for n in neighbours:
          if n not in stack:
            stack.append(n)
      # if DEBUG:
      #   print(">>>>\tstack=", [(x, y) for x, y, _ in stack])
      if len(stack) > GRID_SIZE * GRID_SIZE:
        print("ERROR: stack shouldn't get this big!!")
        exit(127)


def rclick_callback(btn, x: int, y: int, event=None) -> None:
  """callback function for game button right-clicks
  btn        - button right-clicked
  x          - x coordinate on mine grid
  y          - y coordinate on mine grid
  event      - placeholder argument for callback event
  """
  # not a normal click, so have to check the button state
  state = str(btn['state'])
  if state == tk.NORMAL:
    txt = btn.cget('text')
    if txt == MARK:
      btn['text'] = SPACE
      if (x, y) in found_mines:
        found_mines.remove((x, y))
    else:
      btn['text'] = MARK
      if check_grid(x, y) == MINE:
        found_mines.append((x, y))
    if len(found_mines) == MINE_COUNT:
      for row in game_buttons_rows:
        for game_btn in row:
          # Game win state
          game_btn.config(style="G-Win.TButton", state=tk.DISABLED)
  # if DEBUG:
  #   print(f"{found_mines=}")


# if DEBUG:
#   for y in range(9):
#     line = [check_grid(x, y) for x in range(9)]
#     print("".join(line).replace(" ", "."))


def main():
  ### Main Window, sets title and size
  root = tk.Tk()
  root.title("MINESWEEPER")
  root.geometry("260x340")

  ### Styles - create or change styling for different windows or components
  style = ttk.Style()
  style.map("TButton",
            foreground=[("disabled", "black")],
            background=[("disabled", BTN_BGROUND_DEFAULT)])
  style.map("G-Fail.TButton",
            foreground=[("disabled", BTN_FGROUND_FAIL)],
            background=[("disabled", BTN_BGROUND_FAIL)])
  style.map("G-Win.TButton",
            foreground=[("disabled", "black")],
            background=[("disabled", BTN_BGROUND_WIN)])
  style.configure('G.TButton',
                  font=('calibri', 8, 'bold'),
                  relief="groove",
                  background=BTN_BGROUND_GAME)
  style.configure('G-Pressed.TButton',
                  font=('calibri', 8, 'bold'),
                  relief="flat")
  style.configure('G-Fail.TButton', font=('calibri', 8, 'bold'), relief="flat")
  style.configure('G-Win.TButton', font=('calibri', 8, 'bold'), relief="flat")
  style.configure('R.TButton',
                  font=('Arial', 10, 'bold'),
                  background=BTN_BGROUND_DEFAULT)

  ### Section inside main window, gameplay buttons 
  frm1 = ttk.Frame(root, padding=8)
  for y in range(GRID_SIZE):
    game_buttons_rows.append([])
    for x in range(GRID_SIZE):
      btn = ttk.Button(frm1,
                       style="G.TButton",
                       takefocus=False,
                       text=" ",
                       width=2)
      btn.grid(column=x, row=y, padx=1, pady=1)
      game_buttons_rows[y].append(btn)
      # callback needs btn, x, y but the bind function only uses event, hence the partial
      btn.config(command=partial(lclick_callback, btn, x, y))
      btn.bind("<Button-3>", partial(rclick_callback, btn, x, y))
  frm1.grid()

  frm2 = ttk.Frame(root, padding=8)
  btn_quit = ttk.Button(frm2,
                        style="R.TButton",
                        text="Quit",
                        command=root.destroy)
  btn_quit.grid(pady="12 0")
  frm2.grid()

  root.mainloop()


if __name__ == "__main__":
  main()
