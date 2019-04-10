COLUMNS = 10
ROWS = 20

class Shape:
    def __init__(self, shape, phases):
        self._shape = shape
        self._ghost = self.call_shape()
        self._phases = phases
        self._phase = 0

    def call_shape(self):
        return self._shape

    def _is_drop_legal(self, occupied):
        return all([i[0], i[1]+1] not in occupied for i in self._shape)

    def drop(self, occupied):
        if self._is_drop_legal(occupied) and all(self._shape[i][1] + 1 != ROWS for i in range(len(self._shape))):
            for i in range(len(self._shape)):
                self._shape[i][1] += 1

    def fall(self, occupied):
        while ROWS - 1 not in (i[1] for i in self._shape):
            if not self._is_drop_legal(occupied):
                break
            self.drop(occupied)

    def move_up(self, occupied):
        if all([i[0], i[1]-1] not in occupied for i in self._shape):
            for i in range(len(self._shape)):
                self._shape[i][1] -= 1

    def move_left(self, occupied):
        if all([i[0]-1, i[1]] not in occupied for i in self._shape) and \
                all(self._shape[i][0] - 1 != -1 for i in range(len(self._shape))):
            for i in range(len(self._shape)):
                self._shape[i][0] -= 1

    def move_right(self, occupied):
        if all([i[0]+1, i[1]] not in occupied for i in self._shape) and \
                all(self._shape[i][0] + 1 != COLUMNS for i in range(len(self._shape))):
            for i in range(len(self._shape)):
                self._shape[i][0] += 1

    def rotate_clockwise(self, occupied):
        def rotate_phase(coordinates, phases, num):
            if num == 4:
                num = 0
            return [[coordinates[0][0] + phases[num][0][0], coordinates[0][1] + phases[num][0][1]],
                    [coordinates[0][0] + phases[num][1][0], coordinates[0][1] + phases[num][1][1]],
                    [coordinates[0][0] + phases[num][2][0], coordinates[0][1] + phases[num][2][1]],
                    [coordinates[0][0] + phases[num][3][0], coordinates[0][1] + phases[num][3][1]]]\

        if all(i not in occupied for i in rotate_phase(self._shape, self._phases, self._phase+1)):
            if self._phase != 3:
                self._phase += 1
            else:
                self._phase = 0
            if self._shape[0][1] == ROWS - 1:
                self.move_up(occupied)
            if 0 in (i[0] for i in self._shape):
                self.move_right(occupied)
                self._shape = rotate_phase(self._shape, self._phases, self._phase)
                self.move_left(occupied)
            elif COLUMNS - 1 in (i[0] for i in self._shape):
                self.move_left(occupied)
                self._shape = rotate_phase(self._shape, self._phases, self._phase)
                self.move_right(occupied)
            else:
                self._shape = rotate_phase(self._shape, self._phases, self._phase)


class I(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [3, 1], [5, 1], [6, 1]],
                       [[[0, 0], [-1, 0], [1, 0], [2, 0]],
                        [[1, 1], [1, -1], [1, 0], [1, 2]],
                        [[-2, 0], [-1, 0], [0, 0], [1, 0]],
                        [[1, -1], [1, -2], [1, 0], [1, 1]]])
        # [[3, 1], [4, 1], [5, 1], [6, 1]] = HORIZONTAL 0 = [[4, 1], [3, 1], [5, 1], [6, 1]]
        # [[5, 0], [5, 1], [5, 2], [5, 3]] = VERTICAL 1 = [[5, 2], [5, 0], [5, 1], [5, 3]]
        # [[3, 2], [4, 2], [5, 2], [6, 2]] = HORIZONTAL 2 = same
        # [[4, 1], [4, 0], [4, 2], [4, 3]] = VERTICAL 3 = same


class O(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 0], [5, 0], [4, 1], [5, 1]],
                       [[[0, 0], [1, 0], [0, 1], [1, 1]],
                        [[0, 0], [1, 0], [0, 1], [1, 1]],
                        [[0, 0], [1, 0], [0, 1], [1, 1]],
                        [[0, 0], [1, 0], [0, 1], [1, 1]]])


class T(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [5, 1], [4, 0], [3, 1]],
                       [[[0, 0], [1, 0], [0, -1], [-1, 0]],
                        [[0, 0], [0, 1], [1, 0], [0, -1]],
                        [[0, 0], [-1, 0], [0, 1], [1, 0]],
                        [[0, 0], [0, -1], [-1, 0], [0, 1]]])


class Z(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [5, 1], [3, 0], [4, 0]],
                       [[[0, 0], [1, 0], [-1, -1], [0, -1]],
                        [[0, 0], [0, 1], [1, -1], [1, 0]],
                        [[0, 0], [-1, 0], [1, 1], [0, 1]],
                        [[0, 0], [0, -1], [-1, 1], [-1, 0]]])
        self._phase = 0
        # [[4, 1], [3, 0], [4, 0], [5, 1]] = 0 = [[4, 1], [5, 1], [3, 0], [4, 0]]
        # [[4, 1], [5, 0], [5, 1], [4, 2]] = 1 = [[4, 1], [4, 2], [5, 0], [5, 1]]
        # [[4, 1], [3, 1], [4, 2], [5, 2]] = 2 = [[4, 1], [3, 1], [5, 2], [4, 2]]
        # [[4, 1], [3, 2], [3, 1], [4, 0]] = 3 = [[4, 1], [4, 0], [3, 2], [3, 1]]
        # [[4, 1], [3, 0], [4, 0], [5, 1]] = 0


class S(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [4, 0], [5, 0], [3, 1]],
                       [[[0, 0], [-1, 0], [0, -1], [1, -1]],
                        [[0, 0], [0, -1], [1, 0], [1, 1]],
                        [[0, 0], [-1, 1], [0, 1], [1, 0]],
                        [[0, 0], [-1, -1], [-1, 0], [0, 1]]])
        # [[4, 1], [3, 1], [4, 0], [5, 0]] = 0
        # [[4, 1], [4, 0], [5, 1], [5, 2]] = 1
        # [[4, 1], [3, 2], [4, 2], [5, 1]] = 2
        # [[4, 1], [3, 0], [3, 1], [4, 2]] = 3


class L(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [3, 1], [5, 0], [5, 1]],
                       [[[0, 0], [-1, 0], [1, -1], [1, 0]],
                        [[0, 0], [0, -1], [0, 1], [1, 1]],
                        [[0, 0], [-1, 0], [-1, 1], [1, 0]],
                        [[0, 0], [-1, -1], [0, -1], [0, 1]]])
        # [[5, 0], [5, 1], [4, 1], [3, 1]] = 0 = [[4, 1], [3, 1], [5, 0], [5, 1]]
        # [[4, 0], [4, 1], [4, 2], [5, 2]] = 1 = [[4, 1], [4, 0], [4, 2], [5, 2]]
        # [[3, 2], [3, 1], [4, 1], [5, 1]] = 2 = [[4, 1], [3, 1], [3, 2], [5, 1]]
        # [[3, 0], [4, 0], [4, 1], [4, 2]] = 3 = [[4, 1], [3, 0], [4, 0], [4, 2]]


class J(Shape):
    def __init__(self):
        Shape.__init__(self, [[4, 1], [3, 0], [3, 1], [5, 1]],
                       [[[0, 0], [-1, -1], [-1, 0], [1, 0]],
                        [[0, 0], [0, -1], [1, -1], [0, 1]],
                        [[0, 0], [-1, 0], [1, 0], [1, 1]],
                        [[0, 0], [0, -1], [-1, 1], [0, 1]]])
        # [[4, 1], [3, 0], [3, 1], [5, 1]] = 0
        # [[4, 1], [4, 0], [5, 0], [4, 2]] = 1
        # [[4, 1], [3, 1], [5, 1], [5, 2]] = 2
        # [[4, 1], [4, 0], [3, 2], [4, 2]] = 3
