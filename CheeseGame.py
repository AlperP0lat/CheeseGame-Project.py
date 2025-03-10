#This decorator is controlling any piece on the road
def path_blocker(func):
    def wp(self,start_r,start_c,end_r,end_c,board):

       if start_r == end_r :
           step= 1 if start_c< end_c else -1
           for col in range(start_c+step,end_c,step):
               if isinstance(board[start_r][col],Piece):
                   print("Yol üzerinde taş var")
                   return  False
       elif start_c== end_c :
           step= 1 if start_r< end_r else -1
           for row in range(start_r+step,end_r,step):
               if isinstance(board[row][start_c],Piece):
                   print("Yol üzerinde taş var")
                   return False
       elif abs(start_r-end_r) == abs(start_c-end_c):
           row_step=1 if end_r > start_r else -1
           col_step=1 if end_c > start_c else -1
           row,col=start_r+row_step,start_c+col_step
           while row!=end_r or col!=end_c:
               if isinstance(board[row][col],Piece):
                   print("Yol üzerinde taş var")
                   return False
               row += row_step
               col += col_step
       return func(self,start_r,start_c,end_r,end_c,board)
    return wp
#Parent class of all piece
class Piece:
    def __init__(self,color):
        self.color = color

    def symbol(self):
        #This func is controlling the Symbol of different pieces
        pass
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        #This func is arranging moving of pieces
        pass

class Queen(Piece):

    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        row_diff=abs(start_r-end_r)
        col_diff=abs(start_c-end_c)
        if row_diff==col_diff or row_diff==0 or col_diff==0:
            return True
        else:
            print("Vezirin hamlesi geçersiz!")
            return False

    def symbol(self):
        return "♛" if self.color =="white" else "♕"

class Rook(Piece):

    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        return start_r==end_r or start_c==end_c
    def symbol(self):
        return "♜" if self.color =="white" else "♖"

class Bishop(Piece):
    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        if abs(start_r-end_r)==abs(start_c-end_c):
            return True
        else:
            print("Filin çapraz hareketi geçersiz")
            return False
    def symbol(self):
        return "♝" if self.color =="white" else "♗"

class Knight(Piece):
    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        row_diff=abs(start_r-end_r)
        col_diff=abs(start_c-end_c)
        return (row_diff,col_diff) in [(2,1),(1,2)]
    def symbol(self):
        return "♞" if self.color =="white" else "♘"

class King(Piece):
    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        row_diff=abs(start_r-end_r)
        col_diff=abs(start_c-end_c)
        return row_diff<=1 and col_diff<=1
    def symbol(self):
        return "♚" if self.color =="white" else "♔"

class Pawn(Piece):
    @path_blocker
    def is_valid_move(self,start_r,start_c,end_r,end_c,board):
        direction = -1 if self.color =="white" else 1
        row_diff=end_r-start_r
        col_diff= abs(start_c-end_c)

        if col_diff==0:
            if row_diff == direction and board[end_r][end_c]=="  ":
                return True
            if row_diff==2*direction :
                if start_r in (1,6):
                    if board[start_r+direction][start_c]=="  " :
                        if board[end_r][end_c]=="  ":
                                return True

        elif col_diff==1 and row_diff == direction :
            target=board[end_r][end_c]
            if isinstance(target,Piece) and target.color != self.color:
                return True
        return False
    def symbol(self):
        return "♟" if self.color =="white" else "♙"

class Chess:
    def __init__(self):
        self.board=self.create_board()
        self.current_turn='white'

    def create_board(self):

        board=[["  " for i in range(8)] for i in range(8)]

        for i in range(8):
            board[1][i]=Pawn("black")
            board[6][i]=Pawn("white")

        piece_r=[Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
        for i , piece in enumerate(piece_r):
            board[0][i]=piece("black")
            board[7][i]=piece("white")
        return board

    def print_board(self):
        print("\n      A   B   C   D   E   F   G   H")
        print("    +---+---+---+---+---+---+---+---+")
        for i ,row in enumerate(self.board):
            print(f" {8-i}  | "+" | ".join(piece.symbol() if isinstance(piece,Piece) else " " for piece in row)+" |")
            print("    +---+---+---+---+---+---+---+---+")

    def make_move(self,start,end):
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

        piece = self.board[start_row][start_col]
        if not isinstance(piece,Piece):
            print("Burada taş yok")
            return False
        if piece.color != self.current_turn:
            print(f"{self.current_turn} bu taş size ait değil")
            return False

        if piece.is_valid_move(start_row, start_col, end_row, end_col, self.board)==False:
            return False







        self.board[end_row][end_col]=piece
        self.board[start_row][start_col]="  "
        self.current_turn = "black" if self.current_turn == "white" else "white"
        print(f"Sıra sizde {self.current_turn}")
        return True

    def play(self):
        while True:
            self.print_board()
            if not any(isinstance(piece, King) and piece.color == "black" for row in self.board for piece in row):
                print("oyunu beyaz kazandı")
                break
            if not any(isinstance(piece, King) and piece.color == "white" for row in self.board for piece in row):
                print("oyunu siyah kazandı")
                break
            print(f"{self.current_turn.capitalize()} sıra sizde... ")
            move=input("Hamlenizi giriniz:örn(e2 e4 veya stop:  ")
            if move=='stop':
                print("Oyun bitti.")
                break
            try:
                start,end=move.split()
                self.make_move(start,end)
            except ValueError:
                print("Geçersiz giriş formatı. Lütfen ör: e2 e4 gibi bir giriş yapın.")


play=Chess()
play.play()