import tetris_blocks
import random

class Board:
    def __init__(self, columns: int, rows: int):
        self._columns = columns
        self._rows = rows

        self._count = 0

        self._board = []
        self._tetrinoes = ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
        self._tetrino = eval("tetris_blocks.{}()".format(random.choice(self._tetrinoes)))
        self._occupied = []

        self._is_game_over = False

    """RETURNS"""
    def call_gameboard(self):
        return self._board

    def call_occupied(self):
        return self._occupied

    def call_is_game_over(self):
        return self._is_game_over

    def call_current_tetrino(self):
        return self._tetrino

    def call_count(self):
        return self._count

    """GAMEBOARD"""
    def new_gameboard(self):
        """create a new gameboard"""
        for col in range(tetris_blocks.COLUMNS):
            self._board.append([])
            for row in range(tetris_blocks.ROWS):
                self._board[col].append(None)

    def delete_row(self):
        """checks to see if an entire row is occupied by a block, if so delete that row and move all of the rows
        above it down one row"""
        def drop_down(board, num):
            for i in range(num - 1, 0, -1):
                for j in range(tetris_blocks.COLUMNS):
                    board[j][i+1] = board[j][i]
                    board[j][i] = None

        def move_up_remaining_rows(occupied, num):
            for n, i in enumerate(occupied):
                if i[1] < num:
                    occupied[n] = [i[0], i[1]+1]

        for row in set(j for i, j in self._occupied):
            if all(self._board[i][row] == 2 for i in range(10)):
                for i in range(tetris_blocks.COLUMNS):
                    self._board[i][row] = None
                    self._occupied.remove([i, row])
                drop_down(self._board, row)
                move_up_remaining_rows(self._occupied, row)
                self._count += 1

    def update_block(self, block, occupied):
        """update the position of the current tetrino and its accompanying 'ghost' tetrino, the block that shows where
        the current tetrino will land if dropped instantly"""
        ghost = self.ghost_fall(block, occupied)
        for i, j in ghost:
            self._board[i][j] = 3
        for i, j in block.call_shape():
            self._board[i][j] = 1
        return ghost

    def update_board(self, block, occupied):
        """uses update_block, and if the position of the tetrino is equal to the position of its ghost, then end the
        turn of the current tetrino and move on to the next tetrino"""
        ghost = self.update_block(block, occupied)
        if ghost == block.call_shape():
            self.end_turn(block)
            self.delete_row()
            self.update_block(self._tetrino, occupied)

    """TETRINO"""
    def _on_new_tetrino(self):
        """find a new tetrino when a new one is needed by random chance"""
        self._tetrino = eval("tetris_blocks.{}()".format(random.choice(self._tetrinoes)))

    @staticmethod
    def ghost_fall(block, occupied):
        """evaluates the position the 'ghost' of the current tetrino"""
        our_ghost = block.call_shape()[:]
        while tetris_blocks.ROWS - 1 not in (i[1] for i in our_ghost):
            if not all([i[0], i[1] + 1] not in occupied for i in our_ghost):
                break
            for n, i in enumerate(our_ghost):
                our_ghost[n] = [i[0], i[1]+1]
        return our_ghost

    def delete_position(self, shape, occupied):
        """deletes the position of the current tetrino"""
        for i, j in shape.call_shape():
            self._board[i][j] = None
        for i, j in self.ghost_fall(shape, occupied):
            self._board[i][j] = None

    """ENDINGS"""
    def end_turn(self, block):
        """ends the position of the current block then, if the game is not over, calls for a new tetrino"""
        for i, j in block.call_shape():
            self._board[i][j] = 2
            self._occupied.append([i, j])
        self.game_over()
        if not self._is_game_over:
            self._on_new_tetrino()

    def game_over(self):
        """if position [4,1] or position [5, 1] is occupied, then the player can no longer move and thus, it is
        game over"""
        if [4, 1] in self._occupied or [5, 1] in self._occupied:
            self._is_game_over = True


def print_gameboard(board: []):
    """prints the gameboard on the console.  this is primarily a console command"""
    for i in range(tetris_blocks.COLUMNS):
        print(i, end=' ')
    print()
    our_board = list(zip(*board))
    for row in our_board:
        for item in row:
            if item is None:
                item = '*'
            elif item == 1:
                item = '1'
            elif item == 2:
                item = '2'
            elif item == 3:
                item = '3'
            print(item, end=' ')
        print()
    print()


"""Before creating the GUI, it was tested using the Python console."""
# if __name__ == '__main__':
#     game = Board(tetris_blocks.COLUMNS, tetris_blocks.ROWS)
#     game.new_gameboard()
#     new_gameboard = game.call_gameboard()
#     print_gameboard(new_gameboard)
#     tetrino = None
#     while True:
#         move = input('which tetrino:')
#         if move.upper() == 'I':
#             tetrino = tetris_blocks.I()
#             # ghost = tetris_blocks.I()
#         elif move.upper().upper() == 'O':
#             tetrino = tetris_blocks.O()
#             # ghost = tetris_blocks.O()
#         elif move.upper().upper() == 'T':
#             tetrino = tetris_blocks.T()
#             # ghost = tetris_blocks.T()
#         elif move.upper() == 'Z':
#             tetrino = tetris_blocks.Z()
#             # ghost = tetris_blocks.Z()
#         elif move.upper() == 'J':
#             tetrino = tetris_blocks.J()
#             # ghost = tetris_blocks.J()
#         elif move.upper() == 'L':
#             tetrino = tetris_blocks.L()
#             # ghost = tetris_blocks.L()
#         elif move.upper() == 'S':
#             tetrino = tetris_blocks.S()
#             # ghost = tetris_blocks.S()
#         elif move.upper() == 'C':
#             break
#         game.update_board(tetrino, game.call_occupied())
#         print_gameboard(game.call_gameboard())
#         while True:
#             move = input('which move: ')
#             new_tetrino = False
#             game.delete_position(tetrino, game.call_occupied())
#             if move.upper() == 'D':
#                 tetrino.drop(game.call_occupied())
#             elif move.upper() == 'L':
#                 tetrino.move_left(game.call_occupied())
#             elif move.upper() == 'R':
#                 tetrino.move_right(game.call_occupied())
#             elif move.upper() == 'RC':
#                 tetrino.rotate_clockwise(game.call_occupied())
#             elif move.upper() == 'F':
#                 tetrino.fall(game.call_occupied())
#                 new_tetrino = True
#             game.update_board(tetrino, game.call_occupied())
#             print_gameboard(game.call_gameboard())
#
#             if new_tetrino:
#                 game.end_turn(tetrino)
#                 print_gameboard(game.call_gameboard())
#                 break
#         game.game_over()
#         if game.call_is_game_over():
#             break
#
#     print('thanks for playing')
