from enum import Enum
from typing import List, Optional
from collections import deque


class PieceType(Enum):
    X=0
    O=1


class PlayingPiece:

    def __init__(self, piece_type: PieceType) -> None:
        self.piece_type = piece_type


class PlayingPieceX(PlayingPiece):

    def __init__(self) -> None:
        super().__init__(PieceType.X)



class PlayingPieceO(PlayingPiece):

    def __init__(self) -> None:
        super().__init__(PieceType.O)




class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.board: List[List[Optional[PlayingPiece]]] = [[None for _ in range(size)] for _ in range(size)]

    def print_board(self):
        for row in self.board:
            print("|".join(list(map( lambda cell: f" {cell.piece_type.name} " if cell is not None else "   " , row))))
            

    def get_free_cells(self):
        free_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is None:
                    free_cells.append((row, col))
        return free_cells

    def add_piece(self, row, col, playing_piece):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:
            return False
        if self.board[row][col] is not None:
            return False
        self.board[row][col] = playing_piece
        return True

class Player:
    def __init__(self, name: str, playing_piece: PlayingPiece) -> None:
        self.name = name
        self.playing_piece = playing_piece

"""
    This above approach matches the original Java code's behavior, where the fields name and playing_piece are public and 
    there are no enforced encapsulations via getters and setters. If you decide later that you need to add controlled 
    access or validation, you can refactor the code to include @property decorators and make the attributes non-public by 
    using an underscore prefix. Here is how you would add getters and setters while using encapsulation:

    class Player:
    def __init__(self, name: str, playing_piece: 'PlayingPiece') -> None:
        self._name = name
        self._playing_piece = playing_piece

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def playing_piece(self) -> 'PlayingPiece':
        return self._playing_piece

    @playing_piece.setter
    def playing_piece(self, value: 'PlayingPiece') -> None:
        self._playing_piece = value


"""


class Game:
    def __init__(self) -> None:
        self.initialize_game()

    def initialize_game(self):
        # Create 2 players -> can handle multiple players by adding a mapping of some sort
        self.players = deque()
        self.player1 = Player('Player 1', PlayingPieceX())
        self.player2 = Player('Player 2', PlayingPieceO())
        self.players = deque([self.player1, self.player2])

        # Create the board
        self.game_board = Board(3)

    def is_winner(self, row, col, piece_type):
        row_match = True
        col_match = True
        diag_match = True
        anti_diag_match = True
        board = self.game_board.board
        size = self.game_board.size
        for i in range(size):
            if board[i][col] is None or board[i][col].piece_type != piece_type:
                col_match = False
        
        for i in range(size):
            if board[row][i] is None or board[row][i].piece_type != piece_type:
                row_match = False 

        for i in range(size):
            if board[i][i] is None or board[i][i].piece_type != piece_type:
                diag_match = False 

        for i in range(size):
            if board[i][size-1] is None or board[i][size-1].piece_type != piece_type:
                anti_diag_match = False

        return row_match or col_match or diag_match or anti_diag_match 


    def start_game(self):
        no_winner = True
        while no_winner:
            player_turn = self.players.popleft()

            self.game_board.print_board()
            # Check for tie
            

            # Take user input

            print(f"PLayer: {player_turn.name}, Enter row,column")
            row, col = map(lambda x: int(x), input().split(','))
            piece_added_success = self.game_board.add_piece(row, col, player_turn.playing_piece)
            if not piece_added_success:
                print("Position already filled: Try again!")
                self.players.appendleft(player_turn)
                continue

            self.players.append(player_turn)

            winner = self.is_winner(row, col, player_turn.playing_piece.piece_type)
            if winner:
                self.game_board.print_board()
                return player_turn.name
            
            freee_cells = self.game_board.get_free_cells()

            if not freee_cells:
                no_winner = False
                continue
        return 'tie'
    

if __name__ == '__main__':
    game =  Game()
    print(f'game winner is: {game.start_game()}')