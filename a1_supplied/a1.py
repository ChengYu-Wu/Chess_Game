
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
__author__ = "Cheng-Yu Wu, s4623099"
__email__ = "s4623099@student.uq.edu.au"


#==========User Interaction==================================================================================
#============================================================================================================
def initial_state() -> Board:
    """
    Return the board state for a new game.
    """
    init_board = ("rnbqkbnr", "pppppppp", "........", "........", "........","........", "PPPPPPPP", "RNBQKBNR")


    return init_board
    pass

def print_board(board: Board) -> None:

    """
    Print a human-readable board. There are two spaces between a row and its number, and one
    empty line between the board and the row of letters abcdefgh
    """

    for i in range(0,BOARD_SIZE):
        print(board[i], end = "")
        print(" ",8-i)

    print("\nabcdefgh")

    return None
    pass

def sqaure_to_position(square: str) -> Position:
    """
    Convert chess notation to its (row, col): Position equivalent. The top-left corner of the board,
    a8, corresponds to the position (0, 0). The bottom-left corner of the board, a1, corresponds to
    the position (7, 0).
    """
    position_row = ["a","b","c","d","e","f","g","h"]
    
    col, row = square                                   #get the input information
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
    origin, _, destination = user_input.partition(" ")  #separate input into origin and destination positions
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
    row, col = position
    
    board_list = list(copy.deepcopy(board))
    board_list_2 = list(board_list[row])
    board_list_2[col] = character
    board_list_2 = "".join(board_list_2)
    board_list[row] = board_list_2
    board_list = tuple(board_list)

    return board_list
    
    pass

def clear_position(board: Board, position: Position) -> Board:
    """
    Clear the piece at position (i.e. replace with an empty square) and return the resulting board.
    The board will remain unchanged when there is no piece at this position.
    """
    board = change_position(board, position, EMPTY)

    return board
    
    pass

def update_board(board: Board, move: Move) -> Board:
    """
    Assume the move is valid and return an updated version of the board with the move made
    """
    origin, destination = move
    piece = piece_at_position(origin, board)

    board = change_position(board, destination, piece)
    board = clear_position(board, origin)

    return board
    
    pass


#==========Move Validation===================================================================================
#============================================================================================================
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
            return False

    #The move is a valid for the type of piece being moved, according to the rules of chess.
    if not destination_array in get_possible_moves(origin, board):
        return False
    
    #The move does not put the player whose turn it is in check.
    board_check = copy.deepcopy(board)
    board_check = change_position(board_check, destination, piece)
    board_check = clear_position(board_check, origin)
    if is_in_check(board_check, whites_turn):
        return False

    return True

#==========End of Game Checks================================================================================
#============================================================================================================
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
    if can_move(board, whites_turn) or is_in_check(board, whites_turn):
        return False
    else:
        return True

def check_game_over(board: Board, whites_turn: bool) -> bool:
    """
    Returns true only when the game is over (either due to checkmate or stalemate). Also prints
    information about the result if the game is over, or if the player is in check.
    """
    if (is_in_check(board, whites_turn)) and (not can_move(board, whites_turn)) :
        print("\nCheckmate")
        return True
    elif is_stalemate(board, whites_turn):
        print("\nStalemate")
        return True
    elif is_in_check(board, whites_turn):
        if whites_turn:
            print("\nWhite is in check")
        else:
            print("\nBlack is in check")
        return False
    else:
        return False


#==========CSSE7030 Task=====================================================================================
#============================================================================================================
def attempt_promotion(board: Board, whites_turn: bool) -> Board:
    """
    Checks whether there is a pawn on the board that needs to be promoted. If there is, this function
    should prompt the user and ask which piece should replace the pawn. Update the board if
    necessary then return the board.
    """
    if whites_turn :
        if WHITE_PAWN in board[0]:
            piece_change = input("What piece would you like (q, n, r, b)? ")

            while piece_change not in ["q", "n", "r", "b"]:
                piece_change = input("Not a valid piece. What piece would you like (q, n, r, b)? ")

            #get the position of pawn
            for i, p in enumerate(board[0]):
                if WHITE_PAWN == p:
                    piece_position = (0,i)

            #check theinput
            if piece_change == "q":
                piece_new = WHITE_QUEEN
            elif piece_change == "n":
                piece_new = WHITE_KNIGHT
            elif piece_change == "r":
                piece_new = WHITE_ROOK
            elif piece_change == "b":
                piece_new = WHITE_BISHOP

            board = change_position(board,piece_position, piece_new)
    else:
        if BLACK_PAWN in board[7]:
            piece_change = input("What piece would you like (q, n, r, b)? ")

            while piece_change not in ["q", "n", "r", "b"]:
                piece_change = input("Not a valid piece. What piece would you like (q, n, r, b)? ")

            #get the position of pawn
            for i, p in enumerate(board[7]):
                if BLACK_PAWN == p:
                    piece_position = (7,i)

            #check theinput
            if piece_change == "q":
                piece_new = BLACK_QUEEN
            elif piece_change == "n":
                piece_new = BLACK_KNIGHT
            elif piece_change == "r":
                piece_new = BLACK_ROOK
            elif piece_change == "b":
                piece_new = BLACK_BISHOP

            board = change_position(board,piece_position, piece_new)

    return board

def is_valid_castle_attempt(move: Move, board: Board, whites_turn: bool, castling_info:Tuple[bool, bool, bool]) -> bool:
    """
    Returns true only when the given move is a valid attempt at castling for the current board state.
    castling info is a tuple of booleans which are true if the player’s left rook, king, and right rook
    have moved this game, respectively.
    """
    check_moved = list(castling_info)   #castling_info -> [left rook, king, right rook]
    
    if whites_turn:
        if move == ((7,4),(7,6)) and check_moved[1] == check_moved[2] == False and board[7][5] == board[7][6] == EMPTY:
            if is_move_valid(move, board, whites_turn) and is_move_valid(((7,7),(7,5)), board, whites_turn):
                return True    
        elif move == ((7,4),(7,2)) and check_moved[0] == check_moved[1] == False and board[7][1] == board[7][2] == board[7][3] == EMPTY:
            if is_move_valid(move, board, whites_turn) and is_move_valid(((7,0),(7,3)), board, whites_turn):
                return True
    else:
        if move == ((0,4),(0,6)) and check_moved[1] == check_moved[2] == False and board[0][5] == board[0][6] == EMPTY:
            if is_move_valid(move, board, whites_turn) and is_move_valid(((0,7),(0,5)), board, whites_turn):
                return True    
        elif move == ((0,4),(0,2)) and check_moved[0] == check_moved[1] == False and board[0][1] == board[0][2] == board[0][3] == EMPTY:
            if is_move_valid(move, board, whites_turn) and is_move_valid(((0,0),(0,3)), board, whites_turn):
                return True

    return False



#==========Main==============================================================================================
#============================================================================================================
def main():
    """Entry point to gameplay"""
    #print("Implement your solution and run this file")

    count = 0
    board_play = initial_state()
    while True:
        print_board(board_play)
        
        if count % 2 == 0:
            whites_turn = True
        else:
            whites_turn = False

        if check_game_over(board_play, whites_turn):
            break;    

        if whites_turn:
            user_input = input("\nWhite's move: ")
        else:
            user_input = input("\nBlack's move: ")

        if user_input == 'h' or user_input == 'H':
            print(HELP_MESSAGE)
            continue
        elif user_input == 'q' or user_input == 'Q':
            Ans = input("Are you sure you want to quit? ")
            if Ans == 'Y' or Ans == 'y':
                break
            else:
                continue
            
        if valid_move_format(user_input):
            move = process_move(user_input)
        else:
            print("Invalid move\n")
            continue
        
        if is_move_valid(move, board_play, whites_turn) and can_move(board_play, whites_turn):
            board_play = update_board(board_play, move)
            board_play = attempt_promotion(board_play, whites_turn)
            count += 1
            continue
        else:
            print("Invalid move\n")
            continue

    return None

if __name__ == "__main__":
    main()
