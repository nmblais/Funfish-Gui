# import transposition as trans
from struct import unpack; from os import urandom

# responsible of storing all the information about the current state of a chess
# responsible for determining the valid moves at the current
# also will keep a move log
ZOBRIST = [[unpack("!Q", urandom(8))[0] for x in range(64)] for x in range(13)]
SIDEKEY = unpack("!Q", urandom(8))[0]
CASTLEKEY = [unpack("!Q", urandom(8))[0] for x in range(16)]
pieceID = {'wp':1,'wN':2,'wB':3,'wR':4,'wQ':5,'wK':6,'bp':7,'bN':8,'bB':9,'bR':10,'bQ':11,'bK':12}

class GameState():
    """ """
    SQTONAMES = {0:'a8', 1:'b8', 2:'c8', 3:'d8', 4:'e8', 5:'f8', 6:'g8', 7:'h8',
                 8:'a7', 9:'b7',10:'c7',11:'d7',12:'e7',13:'f7',14:'g7',15:'h7',
                16:'a6',17:'b6',18:'c6',19:'d6',20:'e6',21:'f6',22:'g6',23:'h6',
                24:'a5',25:'b5',26:'c5',27:'d5',28:'e5',29:'f5',30:'g5',31:'h5',
                32:'a4',33:'b4',34:'c4',35:'d4',36:'e4',37:'f4',38:'g4',39:'h4',
                40:'a3',41:'b3',42:'c3',43:'d3',44:'e3',45:'f3',46:'g3',47:'h3',
                48:'a2',49:'b2',50:'c2',51:'d2',52:'e2',53:'f2',54:'g2',55:'h2',
                56:'a1',57:'b1',58:'c1',59:'d1',60:'e1',61:'f1',62:'g1',63:'h1'}

    NAMETOSQ = {v: k for k, v in SQTONAMES.items()}

    CASTLE_MASK = (  7, 15, 15, 15,  3, 15, 15, 11,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    13, 15, 15, 15, 12, 15, 15, 14)

    pst = {
        'p': (   0,   0,   0,   0,   0,   0,   0,   0,
                78,  83,  86,  73, 102,  82,  85,  90,
                7,  29,  21,  44,  40,  31,  44,   7,
                -17,  16,  -2,  15,  14,   0,  15, -13,
                -26,   3,  10,   9,   6,   1,   0, -23,
                -22,   9,   5, -11, -10,  -2,   3, -19,
                -31,   8,  -7, -37, -36, -14,   3, -31,
                0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
                -3,  -6, 100, -36,   4,  62,  -4, -14,
                10,  67,   1,  74,  73,  27,  62,  -2,
                24,  24,  45,  37,  33,  41,  25,  17,
                -1,   5,  31,  21,  22,  35,   2,   0,
                -18,  10,  13,  22,  18,  15,  11, -14,
                -23, -15,   2,   0,   2,   0, -23, -20,
                -74, -23, -26, -24, -19, -35, -22, -69),
        'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
                -11,  20,  35, -42, -39,  31,   2, -22,
                -9,  39, -32,  41,  52, -10,  28, -14,
                25,  17,  20,  34,  26,  25,  15,  10,
                13,  10,  17,  23,  17,  16,   0,   7,
                14,  25,  24,  15,   8,  25,  20,  15,
                19,  20,  11,   6,   7,   6,  20,  16,
                -7,   2, -15, -12, -14, -15, -10, -10),
        'R': (  35,  29,  33,   4,  37,  33,  56,  50,
                55,  29,  56,  67,  55,  62,  34,  60,
                19,  35,  28,  33,  45,  27,  25,  15,
                0,   5,  16,  13,  18,  -4,  -9,  -6,
                -28, -35, -16, -21, -13, -29, -46, -30,
                -42, -28, -42, -25, -25, -35, -26, -46,
                -53, -38, -31, -26, -29, -43, -44, -53,
                -30, -24, -18,   5,  -2, -18, -31, -32),
        'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
                14,  32,  60, -10,  20,  76,  57,  24,
                -2,  43,  32,  60,  72,  63,  43,   2,
                1, -16,  22,  17,  25,  20, -13,  -6,
                -14, -15,  -2,  -5,  -1, -10, -20, -22,
                -30,  -6, -13, -11, -16, -11, -16, -27,
                -36, -18,   0, -19, -15, -15, -21, -38,
                -39, -30, -31, -13, -31, -36, -34, -42),
        'K': (   4,  54,  47, -99, -99,  60,  83, -62,
                -32,  10,  55,  56,  56,  55,  10,   3,
                -62,  12, -57,  44, -67,  28,  37, -31,
                -55,  50,  11,  -4, -19,  13,   0, -49,
                -55, -43, -52, -28, -51, -47,  -8, -50,
                -47, -42, -43, -79, -64, -32, -29, -32,
                -4,   3, -14, -50, -57, -18,  13,   4,
                17,  30,  -3, -14,   6,  -1,  40,  18),
        }

    flip = (
        56,  57,  58,  59,  60,  61,  62,  63,
        48,  49,  50,  51,  52,  53,  54,  55,
        40,  41,  42,  43,  44,  45,  46,  47,
        32,  33,  34,  35,  36,  37,  38,  39,
        24,  25,  26,  27,  28,  29,  30,  31,
        16,  17,  18,  19,  20,  21,  22,  23,
        8,   9,  10,  11,  12,  13,  14,  15,
        0,   1,   2,   3,   4,   5,   6,   7)

    MOVETABLE = (( 64, 64,  1,  9,  8, 64, 64, 64),
        ( 64, 64,  2, 10,  9,  8,  0, 64),
        ( 64, 64,  3, 11, 10,  9,  1, 64),
        ( 64, 64,  4, 12, 11, 10,  2, 64),
        ( 64, 64,  5, 13, 12, 11,  3, 64),
        ( 64, 64,  6, 14, 13, 12,  4, 64),
        ( 64, 64,  7, 15, 14, 13,  5, 64),
        ( 64, 64, 64, 64, 15, 14,  6, 64),
        (  0,  1,  9, 17, 16, 64, 64, 64),
        (  1,  2, 10, 18, 17, 16,  8,  0),
        (  2,  3, 11, 19, 18, 17,  9,  1),
        (  3,  4, 12, 20, 19, 18, 10,  2),
        (  4,  5, 13, 21, 20, 19, 11,  3),
        (  5,  6, 14, 22, 21, 20, 12,  4),
        (  6,  7, 15, 23, 22, 21, 13,  5),
        (  7, 64, 64, 64, 23, 22, 14,  6),
        (  8,  9, 17, 25, 24, 64, 64, 64),
        (  9, 10, 18, 26, 25, 24, 16,  8),
        ( 10, 11, 19, 27, 26, 25, 17,  9),
        ( 11, 12, 20, 28, 27, 26, 18, 10),
        ( 12, 13, 21, 29, 28, 27, 19, 11),
        ( 13, 14, 22, 30, 29, 28, 20, 12),
        ( 14, 15, 23, 31, 30, 29, 21, 13),
        ( 15, 64, 64, 64, 31, 30, 22, 14),
        ( 16, 17, 25, 33, 32, 64, 64, 64),
        ( 17, 18, 26, 34, 33, 32, 24, 16),
        ( 18, 19, 27, 35, 34, 33, 25, 17),
        ( 19, 20, 28, 36, 35, 34, 26, 18),
        ( 20, 21, 29, 37, 36, 35, 27, 19),
        ( 21, 22, 30, 38, 37, 36, 28, 20),
        ( 22, 23, 31, 39, 38, 37, 29, 21),
        ( 23, 64, 64, 64, 39, 38, 30, 22),
        ( 24, 25, 33, 41, 40, 64, 64, 64),
        ( 25, 26, 34, 42, 41, 40, 32, 24),
        ( 26, 27, 35, 43, 42, 41, 33, 25),
        ( 27, 28, 36, 44, 43, 42, 34, 26),
        ( 28, 29, 37, 45, 44, 43, 35, 27),
        ( 29, 30, 38, 46, 45, 44, 36, 28),
        ( 30, 31, 39, 47, 46, 45, 37, 29),
        ( 31, 64, 64, 64, 47, 46, 38, 30),
        ( 32, 33, 41, 49, 48, 64, 64, 64),
        ( 33, 34, 42, 50, 49, 48, 40, 32),
        ( 34, 35, 43, 51, 50, 49, 41, 33),
        ( 35, 36, 44, 52, 51, 50, 42, 34),
        ( 36, 37, 45, 53, 52, 51, 43, 35),
        ( 37, 38, 46, 54, 53, 52, 44, 36),
        ( 38, 39, 47, 55, 54, 53, 45, 37),
        ( 39, 64, 64, 64, 55, 54, 46, 38),
        ( 40, 41, 49, 57, 56, 64, 64, 64),
        ( 41, 42, 50, 58, 57, 56, 48, 40),
        ( 42, 43, 51, 59, 58, 57, 49, 41),
        ( 43, 44, 52, 60, 59, 58, 50, 42),
        ( 44, 45, 53, 61, 60, 59, 51, 43),
        ( 45, 46, 54, 62, 61, 60, 52, 44),
        ( 46, 47, 55, 63, 62, 61, 53, 45),
        ( 47, 64, 64, 64, 63, 62, 54, 46),
        ( 48, 49, 57, 64, 64, 64, 64, 64),
        ( 49, 50, 58, 64, 64, 64, 56, 48),
        ( 50, 51, 59, 64, 64, 64, 57, 49),
        ( 51, 52, 60, 64, 64, 64, 58, 50),
        ( 52, 53, 61, 64, 64, 64, 59, 51),
        ( 53, 54, 62, 64, 64, 64, 60, 52),
        ( 54, 55, 63, 64, 64, 64, 61, 53),
        ( 55, 64, 64, 64, 64, 64, 62, 54))

    def __init__(self, fen ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"):
        self.board = []
        self.whiteToMove = None
        self.enPassant = 0
        self.castle = 0
        self.score = 0
        self.fifty = 0
        self.hply = 0
        self.whiteKingLocation = 60
        self.blackKingLocation = 4
        self.kingInCheck = False
        self.checkMate = False
        self.staleMate = False
        self.posKey = 0
        self.historyLog = []
        self.info = None
        self.fenStr = fen
        self.readFenString(self.fenStr)
        self.ep = self.enPassant # for nullmove
        self.ply = 0
        self.moveLog = []
        self.rayTable = []
        # self.initRayTable()
        # print(self.rayTable[27][3])

    def initRayTable(self):
        for f in range(64):
            self.rayTable.append([])
            for t in range(64):
                self.rayTable[f].append(t)
                for d in range(8):
                    sq = self.MOVETABLE[f][d]
                    while sq != 64:
                        if sq == t:
                            self.rayTable[f][t] = d
                            break
                        sq = self.MOVETABLE[sq][d]

    def getHashCode(self):
        self.posKey = 0
        for i, piece in enumerate(self.board):
            if piece != '--':
                self.posKey ^= ZOBRIST[pieceID[piece]][i]

        if self.enPassant != 64:
            self.posKey ^= ZOBRIST[0][self.enPassant]

        self.posKey ^= CASTLEKEY[self.castle]

        if self.whiteToMove:
            self.posKey ^= SIDEKEY

    def isThreeFoldRep(self):
        count = 0
        index = self.hply - self.fifty
        while index < self.hply:
            if self.posKey == self.historyLog[index].key:
                count += 1
                if count == 2:
                    return True
            index += 1
        
        return False

    def initialize(self, fen ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"):
        self.whiteToMove = True
        self.enPassant = 0
        self.castle = 0
        self.score = 0
        self.fifty = 0
        self.hply = 0
        self.whiteKingLocation = 60
        self.blackKingLocation = 4
        self.kingInCheck = False
        # self.checkMate = False
        # self.staleMate = False
        self.posKey = 0 # to be computed
        self.historyLog = []
        self.info = None
        self.fenstr = fen
        self.readFenString(self.fenstr)

    def prPosStatus(self):
        print("Status:")
        print("white to move: ", self.whiteToMove)
        print("white King sq: ", self.whiteKingLocation)
        print("black King sq: ", self.blackKingLocation)
        print("castle flag: ", self.castle)
        print("score: ", self.score)
        if self.enPassant != 64:
            print("en passant sq: ", self.SQTONAMES[self.enPassant])
        else:
            print("en passant sq: --")
        print("history ply: ", self.hply)
        print("fifty moves counter: ", self.fifty)
        print("hash key: ", self.posKey)
        print("King in check? ", self.kingInCheck)

    def getValidMoves(self):
        moves = []
        for m in self.genPseudoMoves():
            if self.makeMove(m):
                self.undoMove()
                moves.append(m)
        # self.isGameOver(moves)
        return moves

    def isGameOver(self, moves):
        if len(moves) == 0:
            if self.inCheck("w" if self.whiteToMove else "b"):
                self.checkMate = True
                return True
            else:
                self.staleMate = True
                return True
        return False

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        self.whiteToMove = not self.whiteToMove
        self.score = -self.score
        self.ep = self.enPassant
        # return Position(
        #     self.board[::-1].swapcase(), -self.score,
        #     self.bc, self.wc, 0, 0)
    def undoNullMove(self):
        self.whiteToMove = not self.whiteToMove
        self.score = -self.score
        self.enPassant = self.ep

    def makeMove(self, move):
        if move == None:
            return False
        f = move.startSq
        t = move.endSq
        pce = move.pieceMoved
        cap = move.pieceCaptured
        promo = move.piecePromotion
        ep = self.enPassant

        self.info = PosInfo(move, self.whiteToMove, self.score, self.enPassant, self.fifty, self.castle, self.whiteKingLocation, self.blackKingLocation, self.posKey)
        self.historyLog.append(self.info)

        self.score += (self.value(move) if self.whiteToMove else -self.value(move))

        # play move
        self.board[t] = pce
        self.board[f] = "--"

        if cap == "--" and pce[1] != "p" and move.flag != 2:
            self.fifty += 1
        else:
            self.fifty = 0

        if pce == "wK":
            self.whiteKingLocation = t
        elif  pce == "bK":
            self.blackKingLocation = t

        if move.flag == 2:
            self.fifty = 0
            if self.whiteToMove:
                if (move.endSq % 8) > 4:
                    self.board[self.NAMETOSQ["f1"]] = self.board[self.NAMETOSQ["h1"]]
                    self.board[self.NAMETOSQ["h1"]] = "--"
                else:
                    self.board[self.NAMETOSQ["d1"]] = self.board[self.NAMETOSQ["a1"]]
                    self.board[self.NAMETOSQ["a1"]] = "--"
            else:
                if (move.endSq % 8) > 4:
                    self.board[self.NAMETOSQ["f8"]] = self.board[self.NAMETOSQ["h8"]]
                    self.board[self.NAMETOSQ["h8"]] = "--"
                else:
                    self.board[self.NAMETOSQ["d8"]] = self.board[self.NAMETOSQ["a8"]]
                    self.board[self.NAMETOSQ["a8"]] = "--"

        self.castle &= self.CASTLE_MASK[f] & self.CASTLE_MASK[t]

        # promotion
        if move.flag & 4:
            self.board[t] =  move.piecePromotion

        # en passant capture
        if move.flag == 8:
            r, c = ep // 8, ep % 8
            sq = 8*((r+1) if self.whiteToMove else (r-1)) + c
            self.board[sq] = "--"

        self.enPassant = 64

        if move.flag == 1: # pawn moved two squares
            r = ((move.startSq // 8) + (move.endSq // 8)) // 2
            self.enPassant = (8 * r + (move.startSq % 8))

        self.ply += 1
        self.hply += 1

        if self.inCheck(pce[0]):
            self.undoMove()
            return False

        self.whiteToMove = not self.whiteToMove

        self.kingInCheck = self.inCheck("w" if self.whiteToMove else "b")

        self.getHashCode()
        
        return True


    def undoMove(self):

        self.ply -= 1
        self.hply -= 1

        if self.historyLog:
            self.info = self.historyLog.pop()
        else:
            self.ply = 0
            self.hply = 0
            return

        move, self.whiteToMove, self.score, self.enPassant, self.fifty, self.castle, self.whiteKingLocation, self.blackKingLocation, self.posKey = self.info.recall()
    
        f = move.startSq
        t = move.endSq
        cap = move.pieceCaptured
        pce = move.pieceMoved
        ep = self.enPassant

        # undo move

        self.board[f] = pce

        if cap != "--":
            self.board[t] = cap
        else:
            self.board[t] = "--"

        # en passant cpature
        if move.flag == 8:
            if pce == "wp":
                self.board[ep+8] = "bp"
            else:
                self.board[ep-8] = "wp"

        if move.flag == 2:
            if self.whiteToMove:
                if (move.endSq % 8) > 4:
                    self.board[self.NAMETOSQ["h1"]] = self.board[self.NAMETOSQ["f1"]]
                    self.board[self.NAMETOSQ["f1"]] = "--"
                else:
                    self.board[self.NAMETOSQ["a1"]] = self.board[self.NAMETOSQ["d1"]]
                    self.board[self.NAMETOSQ["d1"]] = "--"
            else:
                if (move.endSq % 8) > 4:
                    self.board[self.NAMETOSQ["h8"]] = self.board[self.NAMETOSQ["f8"]]
                    self.board[self.NAMETOSQ["f8"]] = "--"
                else:
                    self.board[self.NAMETOSQ["a8"]] = self.board[self.NAMETOSQ["d8"]]
                    self.board[self.NAMETOSQ["d8"]] = "--"

    def clearBoard(self):
        for sq, _ in enumerate(self.board):
            self.board[sq] = "--"

    def readFenString(self, fen):
        """ translate a string into a position """
        pieces = ['wp','wN','wB','wR','wQ','wK','bp','bN','bB','bR','bQ','bK']
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.fenStr = fen
        s = fen.split()
        print(s[0])
        self.board = []
        sq = 0
        for i, ch in enumerate(s[0]):
            if ch == "P": self.board.append("wp"); sq += 1
            elif ch == "N": self.board.append("wN"); sq += 1
            elif ch == "B": self.board.append("wB"); sq += 1
            elif ch == "R": self.board.append("wR"); sq += 1
            elif ch == "Q": self.board.append("wQ"); sq += 1
            elif ch == "K": self.board.append("wK"); self.whiteKingLocation = sq; sq += 1
            elif ch == "p": self.board.append("bp"); sq += 1
            elif ch == "n": self.board.append("bN"); sq += 1
            elif ch == "b": self.board.append("bB"); sq += 1
            elif ch == "r": self.board.append("bR"); sq += 1
            elif ch == "q": self.board.append("bQ"); sq += 1
            elif ch == "k": self.board.append("bK"); self.blackKingLocation = sq; sq += 1
            elif ch in numbers: 
                for k in range(int(ch)): self.board.append("--")
                sq += int(ch)

        self.whiteToMove = True
        if s[1] == "b": self.whiteToMove = False

        self.castle = 0
        for ch in s[2]:
            if ch == "-": self.castle = 0
            elif ch == "K": self.castle = 1
            elif ch == "Q": self.castle += 2
            elif ch == "k": self.castle += 4
            elif ch == "q": self.castle += 8

        self.enPassant = 64
        
        if s[3] != "-":
            self.enPassant = self.NAMETOSQ[s[3]]

        self.getHashCode()

        self.kingInCheck = self.inCheck(("w" if self.whiteToMove else "b"))
        self.checkMate = False
        self.staleMate = False
        self.prPosStatus()


    def writeFenString(self):
        """ Translate a chess position to a string """
        if not self.fenStr:
            return ""
        
        temp = ""
        k = 0
        for sq, piece in enumerate(self.board):
            if sq and sq % 8 == 0:
                temp += "/"
            if self.board == "--":
                k += 1
            else:
                if piece[0] == "b":
                    temp += piece[1].lower()
                else:
                    temp += piece[1].upper()

        fen = ""
        k = 0
        for i in range(len(temp)):
            if temp[i] == "-":
                k += 1
            else:
                if k:
                    fen += str(k)
                    k = 0
                fen += temp[i]
        
        fen += " "

        if self.whiteToMove:
            fen += "w"
        else:
            fen += "b"

        fen += " "

        if self.castle:
            if self.castle & 8:
                fen += "K"
            if self.castle & 4:
                fen += "Q"
            if self.castle & 2:
                fen += "k"
            if self.castle & 1:
                fen += "q"
        else:
            fen += "-"
        
        fen += " "

        fen += self.SQTONAMES[self.enPassant]

        return fen
    
    def value(self, move):
        i = move.startSq
        j = move.endSq
        # print(i, j)
        p, q = move.pieceMoved[1], move.pieceCaptured[1]
        cp, cq = move.pieceMoved[0], move.pieceCaptured[0]
        # Actual move
        if cp == 'w':
            score = self.pst[p][j] - self.pst[p][i]
        elif cp == 'b':
            score = self.pst[p][self.flip[j]] - self.pst[p][self.flip[i]]
        # capture
        if cq == 'b':
            score += self.pst[q][j]
        elif cq == 'w':
            score += self.pst[q][self.flip[j]]
        # Special pawn stuff
        if p == 'P' and cp == 'w':
            if 0 <= j <= 7:
                score += self.pst['Q'][j] - self.pst['P'][j]
            if j == self.enPassant:
                score += self.pst['P'][j+8]
        elif p == 'P' and cp == 'b':
            if 56 <= j <= 63:
                score += self.pst['Q'][self.flip[j]] - self.pst['P'][self.flip[j]]
            if j == self.enPassant:
                score += self.pst['P'][self.flip[j]-8]
        # Castling check detection
        if cp == 'w':
            if abs(j-self.whiteKingLocation) < 2:
                score += self.pst['K'][j]
            # Castling
            if p == 'K' and abs(i-j) == 2:
                score += self.pst['R'][(i+j)//2]
                score -= self.pst['R'][56 if j < i else 63]
        elif cp == 'b':
            if abs(self.flip[j]-self.flip[self.blackKingLocation]) < 2:
                score += self.pst['K'][self.flip[j]]
            # Castling
            if p == 'K' and abs(i-j) == 2:
                score += self.pst['R'][self.flip[(i+j)//2]]
                score -= self.pst['R'][56 if self.flip[j] < self.flip[i] else 63]
            
        return score

    
    def inCheck(self, kingColor):
        if kingColor == "w":
            return self.squareUnderAttack(self.whiteKingLocation, "b")
        return self.squareUnderAttack(self.blackKingLocation, "w")


    def squareUnderAttack(self, sq, attackingColor):
        for i, piece in enumerate(self.board):
            if piece[0] == attackingColor:
                if piece[1] == 'p':
                    if attackingColor == "w":
                        if (i % 8) != 0 and i - 9 == sq:
                            return True
                        if (i % 8) != 7 and i - 7 == sq:
                            return True
                    else:
                        if (i % 8) != 0 and i + 7 == sq:
                            return True
                        if (i % 8) != 7 and i + 9 == sq:
                            return True
                elif piece[1] == 'N':
                    knightMoves = ((-2,-1), (-2,1), (2,-1), (2,1), (-1,-2), (-1,2), (1,-2), (1,2))
                    r = i // 8
                    c = i % 8
                    for m in knightMoves:
                        endRow = r + m[0]
                        endCol = c + m[1]
                        if 0 <= endRow < 8 and 0 <= endCol < 8:
                            endSq = 8 * endRow + endCol
                            if endSq == sq:
                                return True
                elif piece[1] == 'B':
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1))
                    r = i // 8
                    c = i % 8
                    for d in directions:
                        for k in range(1, 8):
                            endRow = r + d[0] * k
                            endCol = c + d[1] * k
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                if endSq == sq:
                                    return True
                                if self.board[endSq] != "--":
                                    break
                            else:
                                break
                elif piece[1] == 'R':
                    directions = ((-1,0), (0,1), (1,0), (0,-1))
                    r = i // 8
                    c = i % 8
                    for d in directions:
                        for k in range(1, 8):
                            endRow = r + d[0] * k
                            endCol = c + d[1] * k
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                if endSq == sq:
                                    return True
                                elif self.board[endSq] != "--":
                                    break
                            else:
                                break
                elif piece[1] == 'Q':
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1), (-1,0), (0,-1), (1,0), (0,1))
                    r = i // 8
                    c = i % 8
                    for d in directions:
                        for k in range(1, 8):
                            endRow = r + d[0] * k
                            endCol = c + d[1] * k
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                if endSq == sq:
                                    return True
                                if self.board[endSq] != "--":
                                    break
                            else:
                                break
                elif piece[1] == 'K':
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1), (-1,0), (0,-1), (1,0), (0,1))
                    r = i // 8
                    c = i % 8
                    for d in directions:
                        endRow = r + d[0]
                        endCol = c + d[1]
                        if 0 <= endRow < 8 and 0 <= endCol < 8:
                            endSq = 8 * endRow + endCol
                            if endSq == sq:
                                return True
        return False




    def genPseudoMoves(self, castling=True, pawn=True, bishop=True, knight=True, rook=True, queen=True, king=True):
        if self.whiteToMove:
            if self.castle & 1 and self.board[self.NAMETOSQ["f1"]] == "--" and self.board[self.NAMETOSQ["g1"]] == "--":
                    if not self.squareUnderAttack(self.NAMETOSQ["e1"], "b") and not self.squareUnderAttack(self.NAMETOSQ["f1"], "b") and not self.squareUnderAttack(self.NAMETOSQ["g1"], "b"):
                        yield Move(self.whiteKingLocation, self.NAMETOSQ["g1"], "", 2, self.board)
            if self.castle & 2 and self.board[self.NAMETOSQ["d1"]] == "--" and self.board[self.NAMETOSQ["c1"]] == "--" and self.board[self.NAMETOSQ["b1"]] == "--":
                    if not self.squareUnderAttack(self.NAMETOSQ["d1"], "b") and not self.squareUnderAttack(self.NAMETOSQ["c1"], "b") and not self.squareUnderAttack(self.NAMETOSQ["e1"], "b"):
                        yield Move(self.whiteKingLocation, self.NAMETOSQ["c1"], "", 2, self.board)
            for sq , piece in enumerate(self.board):
                if piece == "wp":
                    r = sq // 8
                    c = sq % 8
                    idx = 8 * (r-1) + c
                    if self.board[idx] == "--":
                        if r == 1:
                            yield Move(sq, idx, "wQ", 4, self.board)
                            yield Move(sq, idx, "wR", 4, self.board)
                            yield Move(sq, idx, "wB", 4, self.board)
                            yield Move(sq, idx, "wN", 4, self.board)
                        else:
                            yield Move(sq, idx, "", 0, self.board)
                            if r == 6:
                                idx = 8 * (r-2) + c
                                if self.board[idx] == "--":
                                    yield Move(sq, idx, "", 1, self.board)
                    # capture
                    if c-1 >= 0:
                        idx = 8 * (r-1) + (c-1)
                        if self.board[idx][0] == 'b' and self.board[idx][1] != "K":
                            if 0 <= idx < 8:
                                yield Move(sq, idx, "wQ", 4, self.board)
                                yield Move(sq, idx, "wR", 4, self.board)
                                yield Move(sq, idx, "wB", 4, self.board)
                                yield Move(sq, idx, "wN", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx + 8] == "bp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                    if c+1 <= 7:
                        idx = 8 * (r-1) + (c+1)
                        if self.board[idx][0] == 'b' and self.board[idx][1] != "K":
                            if 0 <= idx < 8:
                                yield Move(sq, idx, "wQ", 4, self.board)
                                yield Move(sq, idx, "wR", 4, self.board)
                                yield Move(sq, idx, "wB", 4, self.board)
                                yield Move(sq, idx, "wN", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx + 8] == "bp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                if piece == "wN":
                    d1 = (0,2,4,6)
                    d2 = ((1,7),(1,3),(3,5),(7,5))
                    for i, d in enumerate(d1):
                        tt = self.MOVETABLE[sq][d]
                        if tt == 64: continue
                        for z in range(2):
                            t = self.MOVETABLE[tt][d2[i][z]]
                            if t != 64:
                                cap = self.board[t]
                                if cap == "--":
                                    yield Move(sq, t, "", 0, self.board)
                                elif cap[0] == 'b' and cap[1] != 'K':
                                    yield Move(sq, t, "", 0, self.board)
                if piece == "wB":
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break # square occupied by friendly piece or a king
                            else: # outside the board
                                break
                if piece == "wR":
                    directions = ((-1,0), (0,-1), (1,0), (0,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "wQ":
                    directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "wK":
                    for d in range(8):
                        t = self.MOVETABLE[sq][d]
                        if t != 64:
                            # if self.squareUnderAttack(t, 'b'): continue
                            cap = self.board[t]
                            if cap == "--":
                                yield Move(sq, t, "", 0, self.board)
                            elif self.whiteToMove and cap[0] == 'b' and cap[1] != 'K':
                                yield Move(sq, t, "", 0, self.board)
        else:
            if self.castle & 4 and self.board[self.NAMETOSQ["f8"]] == "--" and self.board[self.NAMETOSQ["g8"]] == "--":
                    if not self.squareUnderAttack(self.NAMETOSQ["e8"], "w") and not self.squareUnderAttack(self.NAMETOSQ["f8"], "w") and not self.squareUnderAttack(self.NAMETOSQ["g8"], "w"):
                        yield Move(self.blackKingLocation, self.NAMETOSQ["g8"], "", 2, self.board)
            if self.castle & 8 and self.board[self.NAMETOSQ["d8"]] == "--" and self.board[self.NAMETOSQ["c8"]] == "--" and self.board[self.NAMETOSQ["b8"]] == "--":
                    if not self.squareUnderAttack(self.NAMETOSQ["d8"], "w") and not self.squareUnderAttack(self.NAMETOSQ["c8"], "w") and not self.squareUnderAttack(self.NAMETOSQ["e8"], "w"):
                        yield Move(self.blackKingLocation, self.NAMETOSQ["c8"], "", 2, self.board)
            for sq , piece in enumerate(self.board):
                if piece == "bp":
                    r = sq // 8
                    c = sq % 8
                    idx = 8 * (r+1) + c
                    if self.board[idx] == "--":
                        if r == 6:
                            yield Move(sq, idx, "bQ", 4, self.board)
                            yield Move(sq, idx, "bR", 4, self.board)
                            yield Move(sq, idx, "bB", 4, self.board)
                            yield Move(sq, idx, "bN", 4, self.board)
                        else:
                            yield Move(sq, idx, "", 0, self.board)
                            if r == 1:
                                idx = 8 * (r+2) + c
                                if self.board[idx] == "--":
                                    yield Move(sq, idx, "", 1, self.board)
                    # capture
                    if c-1 >= 0:
                        idx = 8 * (r+1) + (c-1)
                        if self.board[idx][0] == 'w' and self.board[idx][1] != "K":
                            if 56 <= idx < 64:
                                yield Move(sq, idx, "bQ", 4, self.board)
                                yield Move(sq, idx, "bR", 4, self.board)
                                yield Move(sq, idx, "bB", 4, self.board)
                                yield Move(sq, idx, "bN", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx - 8] == "wp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                    if c+1 <= 7:
                        idx = 8 * (r+1) + (c+1)
                        if self.board[idx][0] == 'w' and self.board[idx][1] != "K":
                            if 56 <= idx < 64:
                                yield Move(sq, idx, "bQ", 4, self.board)
                                yield Move(sq, idx, "bR", 4, self.board)
                                yield Move(sq, idx, "bB", 4, self.board)
                                yield Move(sq, idx, "bN", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx - 8] == "wp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                if piece == "bN":
                    d1 = (0,2,4,6)
                    d2 = ((1,7),(1,3),(3,5),(7,5))
                    for i, d in enumerate(d1):
                        tt = self.MOVETABLE[sq][d]
                        if tt == 64: continue
                        for z in range(2):
                            t = self.MOVETABLE[tt][d2[i][z]]
                            if t != 64:
                                cap = self.board[t]
                                if cap == "--":
                                    yield Move(sq, t, "", 0, self.board)
                                elif not self.whiteToMove and cap[0] == 'w' and cap[1] != 'K':
                                    yield Move(sq, t, "", 0, self.board)
                if piece == "bB":
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break # square occupied by friendly piece or a king
                            else: # outside the board
                                break
                if piece == "bR":
                    directions = ((-1,0), (0,-1), (1,0), (0,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "bQ":
                    directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece == "--":
                                    yield Move(sq, endSq, "", 0, self.board)
                                elif endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "bK":
                    for d in range(8):
                        t = self.MOVETABLE[sq][d]
                        if t != 64:
                            # if self.squareUnderAttack(t, 'w'): continue
                            cap = self.board[t]
                            if cap == "--":
                                yield Move(sq, t, "", 0, self.board)
                            elif not self.whiteToMove and cap[0] == 'w' and cap[1] != 'K':
                                yield Move(sq, t, "", 0, self.board)

    def genPseudoCaptures(self, pawn=True, bishop=True, knight=True, rook=True, queen=True, king=True):
        if self.whiteToMove:
            for sq , piece in enumerate(self.board):
                if piece == "wp":
                    r = sq // 8
                    c = sq % 8
                    idx = 8 * (r-1) + c
                    # capture
                    if c-1 >= 0:
                        idx = 8 * (r-1) + (c-1)
                        if self.board[idx][0] == 'b' and self.board[idx][1] != "K":
                            if 0 <= idx < 8:
                                yield Move(sq, idx, "wQ", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx + 8] == "bp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                    if c+1 <= 7:
                        idx = 8 * (r-1) + (c+1)
                        if self.board[idx][0] == 'b' and self.board[idx][1] != "K":
                            if 0 <= idx < 8:
                                yield Move(sq, idx, "wQ", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                if piece == "wN":
                    d1 = (0,2,4,6)
                    d2 = ((1,7),(1,3),(3,5),(7,5))
                    for i, d in enumerate(d1):
                        tt = self.MOVETABLE[sq][d]
                        if tt == 64: continue
                        for z in range(2):
                            t = self.MOVETABLE[tt][d2[i][z]]
                            if t != 64:
                                cap = self.board[t]
                                if cap[0] == 'b' and cap[1] != 'K':
                                    yield Move(sq, t, "", 0, self.board)
                if piece == "wB":
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break # square occupied by friendly piece or a king
                            else: # outside the board
                                break
                if piece == "wR":
                    directions = ((-1,0), (0,-1), (1,0), (0,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "wQ":
                    directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "b" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "wK":
                    for d in range(8):
                        t = self.MOVETABLE[sq][d]
                        if t != 64:
                            cap = self.board[t]
                            if self.whiteToMove and cap[0] == 'b' and cap[1] != 'K':
                                yield Move(sq, t, "", 0, self.board)
        else:
            for sq , piece in enumerate(self.board):
                if piece == "bp":
                    r = sq // 8
                    c = sq % 8
                    idx = 8 * (r+1) + c
                    # capture
                    if c-1 >= 0:
                        idx = 8 * (r+1) + (c-1)
                        if self.board[idx][0] == 'w' and self.board[idx][1] != "K":
                            if 56 <= idx < 64:
                                yield Move(sq, idx, "bQ", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                        # en passant
                        if self.enPassant == idx and self.board[idx] == "--" and self.board[idx - 8] == "wp":
                            yield Move(sq, self.enPassant, "", 8, self.board)
                    if c+1 <= 7:
                        idx = 8 * (r+1) + (c+1)
                        if self.board[idx][0] == 'w' and self.board[idx][1] != "K":
                            if 56 <= idx < 64:
                                yield Move(sq, idx, "bQ", 4, self.board)
                            else:
                                yield Move(sq, idx, "", 0, self.board)
                if piece == "bN":
                    d1 = (0,2,4,6)
                    d2 = ((1,7),(1,3),(3,5),(7,5))
                    for i, d in enumerate(d1):
                        tt = self.MOVETABLE[sq][d]
                        if tt == 64: continue
                        for z in range(2):
                            t = self.MOVETABLE[tt][d2[i][z]]
                            if t != 64:
                                cap = self.board[t]
                                if not self.whiteToMove and cap[0] == 'w' and cap[1] != 'K':
                                    yield Move(sq, t, "", 0, self.board)
                if piece == "bB":
                    directions = ((-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break # square occupied by friendly piece or a king
                            else: # outside the board
                                break
                if piece == "bR":
                    directions = ((-1,0), (0,-1), (1,0), (0,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "bQ":
                    directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (1,-1), (-1,1), (1,1))
                    r = sq // 8
                    c = sq % 8
                    for d in directions:
                        for i in range(1, 8):
                            endRow = r + d[0] * i
                            endCol = c + d[1] * i
                            if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endSq = 8 * endRow + endCol
                                endPiece = self.board[endSq]
                                if endPiece[0] == "w" and endPiece[1] != "K":
                                    yield Move(sq, endSq, "", 0, self.board)
                                    break
                                else:
                                    break
                            else:
                                break
                if piece == "bK":
                    for d in range(8):
                        t = self.MOVETABLE[sq][d]
                        if t != 64:
                            cap = self.board[t]
                            if not self.whiteToMove and cap[0] == 'w' and cap[1] != 'K':
                                yield Move(sq, t, "", 0, self.board)


class PosInfo():
    def __init__(self, move, whiteToMove, score, enPassant, fifty, castle, whiteKingLocation, blackKingLocation, key):
        self.move = move
        self.whiteToMove = whiteToMove
        self.enPassant = enPassant
        self.fifty = fifty
        self.score = score
        self.castle = castle
        self.whiteKingLocation = whiteKingLocation
        self.blackKingLocation = blackKingLocation
        self.key = key
    
    def recall(self):
        return self.move, self.whiteToMove, self.score, self.enPassant, self.fifty, self.castle, self.whiteKingLocation, self.blackKingLocation, self.key


class Move():
    """ maps keys to values -> Key : value """
    ranksToRows = {"1": 7,"2": 6,"3": 5,"4": 4,
                   "5": 3,"6": 2,"7": 1,"8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,
                   "e": 4,"f": 5,"g": 6,"h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    promoToId = {"Q": 1, "R": 2, "B": 3, "N": 4, "0": 0}
    pceId = {"--": 0, "wQ":1, "wR":2, "wB":3, "wN":4, "bQ":5, "bR":6, "bB":7, "bN":8}

    # flag: normal = 0, pawn move two sq = 1, castle = 2, promo = 4, capture en passant = 8
    def __init__(self, startSq, endSq, promoPiece, flag, board):
        self.startSq = startSq
        self.endSq = endSq
        self.pieceMoved = board[self.startSq]
        self.pieceCaptured = board[self.endSq]
        self.piecePromotion = promoPiece
        self.flag = flag
        self.moveID = self.startSq * 100 + self.endSq

    def getChessNotation(self):
        startRow, startCol = self.startSq//8, self.startSq%8
        endRow, endCol = self.endSq//8, self.endSq%8
        pce = self.pieceMoved[1]
        if self.pieceCaptured != "--" and self.flag != 4:
            if pce == "p":
                return self.getRankFile(startRow, startCol) + "x" + self.getRankFile(endRow, endCol)
            else:
                return pce + self.getRankFile(startRow, startCol) + "x" + self.getRankFile(endRow, endCol)
        if self.flag == 2:
            if (self.endSq % 8) > 4:
                return "O-O"
            else:
                return "O-O-O"
        if self.flag == 4:
            if self.pieceCaptured == "--":
                return self.getRankFile(startRow, startCol) + self.getRankFile(endRow, endCol) + self.piecePromotion[1]
            else:
                return self.getRankFile(startRow, startCol) + "x" + self.getRankFile(endRow, endCol) + self.piecePromotion[1]
        if self.flag == 8:
            return self.getRankFile(startRow, startCol) + self.getRankFile(endRow, endCol) + "ep"

        if pce == "p":
            return self.getRankFile(startRow, startCol) + self.getRankFile(endRow, endCol)
        else:
            return pce + self.getRankFile(startRow, startCol) + self.getRankFile(endRow, endCol)

        # return self.getRankFile(startRow, startCol) + self.getRankFile(endRow, endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            if (self.flag & 4) == 0:
                return self.moveID == other.moveID
            elif self.piecePromotion == other.piecePromotion:
                return self.moveID == other.moveID

        return False

    def __str__(self):
        # castling
        if self.flag == 2:
            return "O-O" if self.endSq % 8 > 4 else "O-O-O"
        
