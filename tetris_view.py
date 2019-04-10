import tkinter
import tetris_model
import tetris_blocks

CANVAS_HEIGHT = 525
CANVAS_WIDTH = 525
SIDEBAR_WIDTH = 250
GAME_HEIGHT = 500
GAME_WIDTH = 250
DEFAULT_FONT = ('Helvetica', 12)
SQUARE_HEIGHT = GAME_HEIGHT / tetris_blocks.ROWS
SQUARE_WIDTH = GAME_WIDTH / tetris_blocks.COLUMNS


class TetrisApplication:
    def __init__(self):
        """MAIN GAME WINDOW"""
        self._root_window = tkinter.Tk()
        self._canvas = tkinter.Canvas(master=self._root_window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                      background='#83DECD')
        self._canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        """SIDEBAR"""
        self._sidebar = tkinter.Frame(master=self._root_window, width=SIDEBAR_WIDTH, height=CANVAS_HEIGHT)
        self._sidebar.grid(row=0, column=0, sticky=tkinter.E)
        self._side_canvas = tkinter.Canvas(master=self._sidebar, width=SIDEBAR_WIDTH, height=CANVAS_HEIGHT)
        self._side_canvas.grid(sticky=tkinter.E)
        self._game_button = tkinter.Button(master=self._sidebar, text="Start", command=self._start_game,
                                           font=('Helvetica', 16), background='#CD83DE')
        self._game_button.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.S + tkinter.E)

        self._game_text = tkinter.StringVar()
        self._game_text.set("WELCOME TO TETRIS")
        game_text = tkinter.Label(master=self._sidebar, textvariable=self._game_text, font=('Helvetica', 16))
        game_text.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.N)

        self._control_text = tkinter.StringVar()
        control_text = tkinter.Label(master=self._sidebar, textvariable=self._control_text, font=DEFAULT_FONT)
        self._control_text.set("\n\nLeft: <Left>\nRight: <Right>\nUp: <Up>\nDown: <Down>"
                               "\nDrop: <Space>\nPause: <Escape>")
        control_text.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W)

        self._speed_text = tkinter.StringVar()
        speed_text = tkinter.Label(master=self._sidebar, textvariable=self._speed_text, font=DEFAULT_FONT)
        speed_text.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W + tkinter.S)

        """THE GAME"""
        self._game_state = tetris_model.Board(tetris_blocks.COLUMNS, tetris_blocks.ROWS)
        self._drop_timer = 1000
        self._is_game_stopped = False

    """CONTROLS"""
    def bind_controls(self):
        self._root_window.bind("<space>", self._on_space)
        self._root_window.bind("<Left>", self._on_left)
        self._root_window.bind("<Right>", self._on_right)
        self._root_window.bind("<Up>", self._on_up)
        self._root_window.bind("<Down>", self._on_down)
        self._root_window.bind("<Escape>", self._stop)

    def unbind_controls(self):
        self._root_window.unbind("<space>")
        self._root_window.unbind("<Left>")
        self._root_window.unbind("<Right>")
        self._root_window.unbind("<Up>")
        self._root_window.unbind("<Down>")
        self._root_window.unbind("<Escape>")

    def run(self):
        self._root_window.mainloop()

    def _start_game(self):
        self._game_state.new_gameboard()
        self._start()
    
    def _start(self, *args):
        """start the game, adding a pause button and binding the appropriate controls"""
        self._is_game_stopped = False
        self._game_text.set("LINES DONE: " + str(self._game_state.call_count()))

        self._control_text.set("\n\nLeft: <Left>\nRight: <Right>\nUp: <Up>\nDown: "
                               "<Down>\nDrop: <Space>\nPause: <Escape>")
        self._game_button.destroy()
        self._pause_button = tkinter.Button(master=self._sidebar, text="Pause", command=self._stop,
                                            font=('Helvetica', 16), background='#CD83DE')
        self._pause_button.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.S + tkinter.E)

        self._speed_text.set("Speed: " + str(self._drop_timer))

        self.bind_controls()
        self._game_state.update_board(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._draw()
        self._root_window.after(1000, func=self._next_frame)

    def _stop(self, *args):
        """stops the game, if the game is over then it is game over.  if not, unbind the controls and destroy the
        current pause button to make room for the game button so the player can start the game once more."""
        self._is_game_stopped = True
        self.unbind_controls()
        if self._game_state.call_is_game_over():
            self._game_text.set("Game Over\nLINES DONE: " + str(self._game_state.call_count()))
        else:
            self._pause_button.destroy()

            self._game_button = tkinter.Button(master=self._sidebar, text="Resume", command=self._start_game,
                                               font=('Helvetica', 16), background='#CD83DE')
            self._game_button.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.S + tkinter.E)
            self._game_text.set("Paused\nLINES DONE: " + str(self._game_state.call_count()))

            self._control_text.set("\n\nResume: <Space>")

            self._root_window.bind("<space>", self._start)

    def _set_destroyed_lines(self):
        self._game_text.set("LINES DONE: " + str(self._game_state.call_count()))

    def _draw(self):
        for row in range(tetris_blocks.COLUMNS):
            for column in range(tetris_blocks.ROWS):
                self._canvas.create_rectangle((SQUARE_HEIGHT*row) + 10, (SQUARE_WIDTH*column),
                                              (SQUARE_HEIGHT*(row+1)) + 10, (SQUARE_WIDTH*(column+1)))
                if self._game_state.call_gameboard()[row][column] == 1:
                    self._canvas.create_rectangle((SQUARE_HEIGHT*row) + 10, (SQUARE_WIDTH*column),
                                                  (SQUARE_HEIGHT*(row+1)) + 10, (SQUARE_WIDTH*(column+1)), fill='black')
                elif self._game_state.call_gameboard()[row][column] == 2:
                    self._canvas.create_rectangle((SQUARE_HEIGHT*row) + 10, (SQUARE_WIDTH*column),
                                                  (SQUARE_HEIGHT*(row+1)) + 10,
                                                  (SQUARE_WIDTH*(column+1)), fill='purple')
                elif self._game_state.call_gameboard()[row][column] == 3:
                    self._canvas.create_rectangle((SQUARE_HEIGHT*row) + 10, (SQUARE_WIDTH*column),
                                                  (SQUARE_HEIGHT*(row+1)) + 10, (SQUARE_WIDTH*(column+1)), fill='red')
        self._set_destroyed_lines()

    def _redraw(self):
        self._canvas.delete(tkinter.ALL)
        self._game_state.update_board(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        # print(tetris_model.print_gameboard(self._game_state.call_gameboard()))
        self._draw()
        if self._game_state.call_is_game_over():
            self._stop()

    def _next_frame(self):
        """drops the current tetrino by one column according to the timer we have set,
        counting down from 1000 until we reach 100."""
        if not self._is_game_stopped:
            self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
            self._game_state.call_current_tetrino().drop(self._game_state.call_occupied())
            self._redraw()
            if self._drop_timer > 100:
                self._drop_timer -= 3
            self._speed_text.set("Speed: " + str(self._drop_timer))
            self._root_window.after(self._drop_timer, func=self._next_frame)

    """MOVESET"""
    def _on_space(self, event):
        """spacebar control drops the current tetrino"""
        self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._game_state.call_current_tetrino().fall(self._game_state.call_occupied())
        # self._on_new_tetrino()
        self._redraw()

    def _on_left(self, event):
        """left directional button control moves the current tetrino left"""
        self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._game_state.call_current_tetrino().move_left(self._game_state.call_occupied())
        self._redraw()

    def _on_right(self, event):
        """right directional button control moves the current tetrino right"""
        self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._game_state.call_current_tetrino().move_right(self._game_state.call_occupied())
        self._redraw()

    def _on_up(self, event):
        """up directional button rotates the current tetrino clockwise"""
        self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._game_state.call_current_tetrino().rotate_clockwise(self._game_state.call_occupied())
        self._redraw()

    def _on_down(self, event):
        """down directional button moves the current tetrino down one"""
        self._game_state.delete_position(self._game_state.call_current_tetrino(), self._game_state.call_occupied())
        self._game_state.call_current_tetrino().drop(self._game_state.call_occupied())
        self._redraw()
