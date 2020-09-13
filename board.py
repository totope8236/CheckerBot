from typing import List
import copy

class Board:
    """
    Defines one the the four board present on the game
    """
    WHITE = 0
    BLACK = 1

    OUTPUT = [u'◇', u'◆']

    def __init__(self, height=4, width=4, first_player=0):
        """
        Initialized a standard board with the rocks in the standard pos
        :param height:
        :param width:
        """
        self.width = width
        self.height = height

        self.rocks = [[], []]

        for k in range(2):
            for i in range(width):
                self.rocks[k].append((k * 3, i))

        self.current_player = first_player

        self.update_state()

    def possible_passive_moves_from_position(self, position: (int, int)):
        """
        Given a tuple representing a position on the board,
        calculates all of the possible passive moves possible
        :param position:
        :return:
        """

        def add(p, m):
            return p[0] + m[0], p[1] + m[1]

        def valid_position(p):
            # Checks if a given position p is empty and on the board

            for sub in p:
                if sub > 3 or sub < 0:
                    return False

            for player_rocks in self.rocks:
                for rock in player_rocks:
                    if rock == p:
                        return False

            return True

        def check_movement(p, m):

            possible_position = add(p, m)

            if valid_position(possible_position):
                return possible_position
            else:
                return None

        possible_directions = ([(i, j)
                           for i in range(-1, 2)
                           for j in range(-1, 2)
                           if i != 0 or j != 0])

        # Check if a move is valid
        valid_moves = []

        for move in possible_directions:
            new_position = check_movement(position, move)
            if new_position:
                valid_moves.append(new_position)

                # Can also move once more
                sub_new = check_movement(new_position, move)
                if sub_new:
                    valid_moves.append(sub_new)

        return valid_moves

    def passive_moves(self):
        l = []
        for rock in self.rocks[self.current_player]:
            l += [(rock, new_p) for new_p in self.possible_passive_moves_from_position(rock)]
        return l

    def passive_moves_boards(self):
        moves = self.passive_moves()

        out = []

        for move in moves:
            out.append(
                self.new_replace(move[0], move[1])
            )

        return out

    def new_replace(self, old, new):
        new_board = copy.deepcopy(self)
        i = new_board.rocks[new_board.current_player].index(old)
        new_board.rocks[new_board.current_player][i] = new
        new_board.current_player = 1 - new_board.current_player # Set the current player to the next
        return new_board


    def update_state(self):
        self.boardState = [[" " for _ in range(4)] for _ in range(4)]
        for color, rock_line in enumerate(self.rocks):
            for rock in rock_line:
                self.boardState[rock[0]][rock[1]] = self.OUTPUT[color]

    def print(self):
        """
        Prints a unicode encoding of the board
        :return:
        """
        print(self)

    def __str__(self):
        """

        :return: Unicode encoding of the current board
        """
        self.update_state()

        lines = []

        # Prints top line
        lines.append(u'╭' + (u'───┬' * (self.width - 1)) + u'───╮')

        # Print the boards rows
        for num, row in enumerate(self.boardState[:-1]):
            lines.append(u'│ ' + u' │ '.join(row) + u' │')
            lines.append(u'├' + (u'───┼' * (self.width - 1)) + u'───┤')

        # Print the last row
        lines.append(u'│ ' + u' │ '.join(self.boardState[-1]) + u' │')

        # Prints the final line in the board
        lines.append(u'╰' + (u'───┴' * (self.width - 1)) + u'───╯')
        return '\n'.join(lines)


b = Board()
# print(b)
[s.print() for s in b.passive_moves_boards()]


