
"""
Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""

from typing import Optional, Tuple

from a1_support import *
import copy

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

def initial_state() -> Board:
    """
    Return the board state for a new game.
    """
    init_board = [[BLACK_ROOK,BLACK_KNIGHT,BLACK_BISHOP,BLACK_QUEEN,BLACK_KING,BLACK_BISHOP,BLACK_KNIGHT,BLACK_ROOK,8],
                  [BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,BLACK_PAWN,7],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,6],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,5],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,4],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,3],
                  [WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,WHITE_PAWN,2],
                  [WHITE_ROOK,WHITE_KNIGHT,BLACK_BISHOP,WHITE_QUEEN,WHITE_KING,BLACK_BISHOP,WHITE_KNIGHT,WHITE_ROOK,1],
                  ["a","b","c","d","e","f","g","h",""]]

    return init_board
    pass

def print_board(board: Board) -> None:

    """
    Print a human-readable board. There are two spaces between a row and its number, and one
    empty line between the board and the row of letters abcdefgh
    """

    for i in range(0,BOARD_SIZE+1):
        for j in range(0,BOARD_SIZE+1):
            print(board[i][j],end = " ")
        print("\n")

    return 0
    pass

def sqaure_to_position(square: str) -> Position:
    """
    Convert chess notation to its (row, col): Position equivalent. The top-left corner of the board,
    a8, corresponds to the position (0, 0). The bottom-left corner of the board, a1, corresponds to
    the position (7, 0).
    """
    position_row = ["a","b","c","d","e","f","g","h"]
    
    col, row = square
    row_postion = 8 - int(row) 
    
    for ser, pos in enumerate(position_row):
        if col == pos:
            col_position = ser

    return (row_postion, col_position)
    
    pass

def process_move(user_input: str) -> Move:
    """
    Assume the user_input is valid and convert the user input to a move based on (row, col): Position.
    """
    #Check the input is valid and transform it to postions(origin and destination) 

    origin, _, destination = user_input.partition(" ")
    origin_position = sqaure_to_position(origin)
    destination_position = sqaure_to_position(destination)

    return (origin_position, destination_position)
    
    pass

def change_position(board: Board, position: Position, character: str) -> Board:
    """
    Return a copy of board with the character at position changed to character. Note in the
    example usage that the second call to change_position does not preserve the change from the
    first call.
    """
    import copy
    
    board_copy = copy.deepcopy(board)
    row, col = position
    board_copy[row][col] = character

    return board_copy
    
    pass

def clear_position(board: Board, position: Position) -> Board:
    """
    Clear the piece at position (i.e. replace with an empty square) and return the resulting board.
    The board will remain unchanged when there is no piece at this position.
    """
    row, col = position
    board[row][col] = EMPTY

    return board
    
    pass

def update_board(board: Board, move: Move) -> Board:
    """
    Assume the move is valid and return an updated version of the board with the move made
    """
    origin, destination = move
    piece = piece_at_position(origin, board)

    board = change_position(board, destination, piece)
    clear_position(board, origin)

    return board
    
    pass

def is_current_players_piece(piece: str, whites_turn: bool) -> bool:
    """
    Returns true only when piece is belongs to the player whose turn it is.
    """   
    if (piece in WHITE_PIECES) == whites_turn:
        return True
    else:
        return False
    
def is_move_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """
    Returns true only when the move is valid on the current board state for the player whose turn it
    is. A move is valid if all of the following are true
    """
    origin, destination = move
    row_origin, col_origin = origin
    row_destination, col_destination = destination
    piece = board[row_origin][col_origin]
    target = board[row_destination][col_destination]
    destination_array = (row_destination, col_destination)

    #Both positions in the move exist on the board.
    if out_of_bounds(destination):
        return False
    #The positions in the move are different.
    if origin == destination:
        return False
    #The piece being moved belongs to the player who is trying to move it.
    if (piece == EMPTY) or not(is_current_players_piece(piece,whites_turn)):
        return False
        
    #The square the piece is being moved to is empty or contains a piece of the opposite colour.
    if target != EMPTY:
        if is_current_players_piece(target,whites_turn):
            #print("the same player's piece")
            return False

    #The move is a valid for the type of piece being moved, according to the rules of chess.
    if not destination_array in get_possible_moves(origin, board):
        #print(destination)
        #print(get_possible_moves(origin, board))
        #print("this is not allowed")
        return False
    
    #The move does not put the player whose turn it is in check.
    """ 
    check_board = [[EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,8],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,7],
                  [EMPTY,EMPTY,EMPTY,BLACK_KING,EMPTY,EMPTY,EMPTY,EMPTY,6],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,5],
                  [EMPTY,EMPTY,EMPTY,EMPTY,WHITE_KING,EMPTY,EMPTY,EMPTY,4],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,3],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,2],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,1],
                  ["a","b","c","d","e","f","g","h",""]]
    """
    board_check = copy.deepcopy(board)
    board_check = change_position(board_check, destination, piece)
    board_check = clear_position(board_check, origin)
    if is_in_check(board_check, whites_turn):
        #print("It will make in check!")
        return False

    return True
        
def can_move(board: Board, whites_turn: bool) -> bool:
    """
    Returns true only when the player can make a valid move which does not put them in check
    """
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE):
            piece = board[i][j]
            position = [i,j]
            if ((piece in WHITE_PIECES) and whites_turn) or ((piece in BLACK_PIECES) and (whites_turn == False)):
                for path in get_possible_moves(position, board):
                    board_check = copy.deepcopy(board)
                    board_check = change_position(board_check, path, piece)
                    board_check = clear_position(board_check, position)
                    if not is_in_check(board_check, whites_turn):
                        return True

    return False
                
def is_stalemate(board: Board, whites_turn: bool) -> bool:
    """
    Returns true only when a stalemate has been reached. A stalemate occurs when the player who
    is about to move isn’t currently in check but can’t make any moves without putting themselves
    in check
    """
    if not can_move(board, whites_turn):
        return True

    return False

    


def check_game_over(board: Board, whites_turn: bool) -> bool:
    """
    Returns true only when the game is over (either due to checkmate or stalemate). Also prints
    information about the result if the game is over, or if the player is in check.
    """
    if is_in_check(board, whites_turn):
        print("Checkmate")
        return True
    elif is_stalemate(board, whites_turn):
        print("Stalemate")
        return True
    else:
        return False

def main():
    """Entry point to gameplay"""
    print("Implement your solution and run this file")

    count = 0
    board_play = initial_state()

    while True:
        print_board(board_play)
        if count % 2 == 0:
            user_input = input("White's move:")
            whites_turn = True
        else:
            user_input = input("Black's move:")
            whites_turn = False

        if user_input == 'h' or user_input == 'H':
            print(HELP_MESSAGE)
            continue
        elif user_input == 'q' or user_input == 'Q':
            Ans = input("Are you sure you want to quit?")
            if Ans == 'Y' or Ans == 'y':
                break
            else:
                continue

        if check_game_over(board_play, whites_turn):
            break;
            
        if valid_move_format(user_input):
            move = process_move(user_input)
        else:
            print("Invalid move")
            continue

        print(move)
        print(is_move_valid(move, board_play, whites_turn))
        print(can_move(board_play, whites_turn))
        
        if is_move_valid(move, board_play, whites_turn) and can_move(board_play, whites_turn):
            board_play = update_board(board_play, move)
            count += 1
            continue
        else:
            print("Invalid move")
            continue


    


if __name__ == "__main__":
    main()
    """
    print(HELP_MESSAGE)
    board_play = copy.deepcopy(initial_state())
    print_board(board_play)
    x = process_move("a6 a7")
    is_move_valid(x, board_play,False)
    check_board = [[BLACK_KING,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,8],
                  [EMPTY,EMPTY,WHITE_QUEEN,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,7],
                  [EMPTY,EMPTY,EMPTY,EMPTY,WHITE_KING,EMPTY,EMPTY,EMPTY,6],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,5],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,4],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,3],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,2],
                  [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,1],
                  ["a","b","c","d","e","f","g","h",""]]
    print_board(check_board)
    print(can_move(check_board,False))
    print(is_stalemate(check_board,False))
    print(check_game_over(check_board,False))
    is_move_valid([[0,0],[0,1]], check_board, False)
    """

