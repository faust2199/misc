import sys

class TicTacToe:
    """
    Generalized to an m,n,k game: an m*n board, with the goal of getting k in a row
    """
    def __init__(self, width, height, k):
        self.width = width
        self.height = height
        self.k = k
        self.board = [[" "] * width for _ in range(height)]
        self.numMoves = 0
        self.result = None


    def getBoardAsStr(self):
        """
        Get on screen visualization of the board
        """
        lines = []
        splitter = "-" * (self.width * 2 - 1)
        for row in self.board:
            lines.append("|".join(row))
            lines.append(splitter)
        lines.pop()
        return "\n".join(lines)


    def findWinner(self, x, y):
        """
        Assuming a player just made a valid move, find if that move completes the goal. If so, return the player.
        """
        player = self.board[y][x]
        directionPairs = [
            [(-1, 0), (1, 0)],
            [(0, -1), (0, 1)],
            [(-1, -1), (1, 1)],
            [(-1, 1), (1, -1)],
        ]
        for directionPair in directionPairs:
            count = 1
            for direction in directionPair:
                multipler = 1
                while True:
                    newY = y + direction[0] * multipler
                    newX = x + direction[1] * multipler
                    if newX < 0 or newX >= self.width or newY < 0 or newY >= self.height:
                        break
                    if self.board[newY][newX] != player:
                        break
                    count += 1
                    multipler += 1
            if count == self.k:
                return player
        return None


    def canContinue(self):
        """
        Find if the board can accept more moves.
        Note that it does not check for winners.
        """
        if self.result is not None:
            return False
        if self.numMoves >= self.width * self.height:
            self.result = "D"
            return False
        return True


    def place(self, x, y, player):
        """
        Place a player's mark on the board, then check if the player becomes the winner.
        Return True if the move is valid. Return False otherwise.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if self.board[y][x] != " ":
            return False
        self.board[y][x] = player
        self.numMoves += 1
        self.result = self.findWinner(x, y)
        if self.result is None and self.numMoves >= self.width * self.height:
            self.result = "D"
        return True


def main():
    ticTacToe = TicTacToe(3, 3, 3)
    players = ["X", "O"]
    index = 0
    while ticTacToe.canContinue():
        print(ticTacToe.getBoardAsStr())
        player = players[index % 2]
        print("Player %s's turn. Enter row and column separated by comma." % player)
        line = sys.stdin.readline().rstrip()
        tokens = line.split(",")
        if len(tokens) != 2:
            print("Invalid number of arguments. Please try again.")
            continue
        if tokens[0].isdecimal() and tokens[1].isdecimal():
            row = int(tokens[0])
            col = int(tokens[1])
            if ticTacToe.place(col, row, player):
                if ticTacToe.result is not None:
                    break
                else:
                    index += 1
                    continue
            else:
                print("Invalid position. Please try again.")
        else:
            print("Invalid number format. Please try again.")
    print(ticTacToe.getBoardAsStr())
    if ticTacToe.result == "D":
        print("Draw")
    else:
        print("Player %s wins." % ticTacToe.result)


def runTests():
    """
    Test cases taken from Wikipedia assume we have a board with the nine positions numbered as follows:
    1|2|3
    -----
    4|5|6
    -----
    7|8|9
    """
    cases = [
        {
            "data": [1, 5, 9, 2, 8, 7, 3, 6, 4],
            "expected": "D"
        },
        {
            "data": [1, 5, 3, 2, 8, 4, 6, 9, 7],
            "expected": "D"
        },
        {
            "data": [1, 5, 9, 3, 7, 6, 4],
            "expected": "X"
        }
    ]
    for i in range(len(cases)):
        test = cases[i]
        ticTacToe = TicTacToe(3, 3, 3)
        index = 0
        players = ["X", "O"]
        data = test["data"]
        for j in range(len(data)):
            pos = data[j]
            row = (pos - 1) // 3
            col = (pos - 1) % 3
            assert ticTacToe.canContinue()
            assert ticTacToe.place(col, row, players[index % 2])
            index += 1
        assert not ticTacToe.canContinue()
        assert test["expected"] == ticTacToe.result
        print("Test %d passed." % i)


if __name__=="__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tests":
        runTests()
    else:
        main()