import pygame as pg
from button import Button

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 350
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
CONTROL_PANEL_WIDTH = 100
CONTROL_PANEL_HEIGHT = BOARD_HEIGHT
ALL_WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH + CONTROL_PANEL_WIDTH
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 30

def row2colFromIndex(idx):
    return idx//DIMENSION, idx%DIMENSION


def indexFromRowCol(r, c):
    return DIMENSION*r + c

class Drawing:
    """ """
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.images = {}
        self.loadImages()
        self.moveLogFont = pg.font.SysFont("Arial", 16, False, False)

    def loadImages(self):
        pieces = ['wp','wN','wB','wR','wQ','wK','bp','bN','bB','bR','bQ','bK']
        path = 'D:/Users/Owner/Development/Python/Projects/Pygame/funfish/'
        for piece in pieces:
            self.images[piece] = pg.transform.scale(pg.image.load(path + "images/" + piece + ".png").convert_alpha(), (SQ_SIZE, SQ_SIZE))

    def update(self, pos):
        self.pos = pos

    def drawBoard(self):
        colors = [pg.Color("skyblue"), pg.Color((88, 155, 209))]
        for i in range(DIMENSION * DIMENSION):
            r, c = row2colFromIndex(i)
            color = colors[((r + c) % 2)]
            pg.draw.rect(self.screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawPieces(self):
        for i, piece in enumerate(self.pos.board):
            r, c = row2colFromIndex(i)
            if piece != "--":
                self.screen.blit(self.images[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    def drawGameState(self, playerClicks, validMoves, movingSquares): #, validMoves, sqSelected, moveLogFont):
        self.drawBoard()
        self.highlightSquares(playerClicks, validMoves, movingSquares)
        self.drawPieces()
        self.drawMoveLog()
        return True

    def button(self, y_pos, text):
        button = Button(self.screen, CONTROL_PANEL_WIDTH, y_pos, text)
        return button

    def highlightSquares(self, playerClicks, validMoves, movingSquares):
        if len(playerClicks) == 1 and playerClicks[0] != 64:
            sq = playerClicks[0]
            r = sq // 8
            c = sq % 8
            if self.pos.board[sq][0] == ('w' if self.pos.whiteToMove else 'b'):
                s = pg.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100) # transparentcy value (0 == transparent 255 == opaque)
                s.fill(pg.Color('yellow'))
                self.screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
                s.fill(pg.Color('yellow'))
                for move in validMoves:
                    from_sq = move.startSq
                    if from_sq == sq:
                        target_sq = move.endSq
                        r_e = target_sq // 8
                        c_e = target_sq % 8
                        self.screen.blit(s, (c_e * SQ_SIZE, r_e * SQ_SIZE))
        elif len(movingSquares) > 0:
            sq = movingSquares[-1]
            r = sq[0][0] // 8
            c = sq[0][0] % 8
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparentcy value (0 == transparent 255 == opaque)
            s.fill(pg.Color('yellow'))
            self.screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pg.Color('yellow'))
            # sq = movingSquares[-1]
            r = sq[0][1] // 8
            c = sq[0][1] % 8
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparentcy value (0 == transparent 255 == opaque)
            s.fill(pg.Color('yellow'))
            self.screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pg.Color('yellow'))

    def drawMoveLog(self):
        moveLogRect = pg.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
        pg.draw.rect(self.screen, pg.Color('lightgray'), moveLogRect)
        moveLog = self.pos.moveLog
        moveTexts = []
        for i in range(0, len(moveLog), 2):
            moveString = str(i//2 + 1) + "." + moveLog[i].getChessNotation() #+ ","
            if i + 1 < len(moveLog):
                moveString += "," + moveLog[i + 1].getChessNotation() + "  "
            moveTexts.append(moveString)
        if self.pos.checkMate:
            moveTexts.append("...CHECKMATE!!")
        elif self.pos.staleMate:
            moveTexts.append("...STALEMATE!!")
        movesPerRow = 3
        padding = 5
        lineSpacing = 1
        textY = padding
        for i in range(0, len(moveTexts), movesPerRow):
            text = ""
            for j in range(movesPerRow):
                if i + j < len(moveTexts):
                    text += moveTexts[i + j]
            textObject = self.moveLogFont.render(text, True, pg.Color('black'))
            textLocation = moveLogRect.move(padding, textY)
            self.screen.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing


if __name__ == '__main__':
    pass