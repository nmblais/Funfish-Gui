import sys
from enum import Enum, auto
import pygame as pg
from chessboard import *
from paint import Drawing
from multiprocessing import Process, Queue
import sunfish_old
from button import Button


BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 350
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
CONTROL_PANEL_WIDTH = 100
CONTROL_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 30

""" maps keys to values -> Key : value """
ranksToRows = {"1": 7,"2": 6,"3": 5,"4": 4,
                "5": 3,"6": 2,"7": 1,"8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,
                "e": 4,"f": 5,"g": 6,"h": 7}
colsToFiles = {v: k for k, v in filesToCols.items()}

sqN = {
    "a8": 0,"b8": 1,"c8": 2,"d8": 3,"e8": 4,"f8": 5,"g8": 6,"h8": 7,
    "a7": 8,"b7": 9,"c7":10,"d7":11,"e7":12,"f7":13,"g7":14,"h7":15,
    "a6":16,"b6":17,"c6":18,"d6":19,"e6":20,"f6":21,"g6":22,"h6":23,
    "a5":24,"b5":25,"c5":26,"d5":27,"e5":28,"f5":29,"g5":30,"h5":31,
    "a4":32,"b4":33,"c4":34,"d4":35,"e4":36,"f4":37,"g4":38,"h4":39,
    "a3":40,"b3":41,"c3":42,"d3":43,"e3":44,"f3":45,"g3":46,"h3":47,
    "a2":48,"b2":49,"c2":50,"d2":51,"e2":52,"f2":53,"g2":54,"h2":55,
    "a1":56,"b1":57,"c1":58,"d1":59,"e1":60,"f1":61,"g1":62,"h1":63,
}

nSq = {v: k for k, v in sqN.items()}


class game:
    """ """
    def __init__(self, title, width, height):
            self.title = title
            self.window_width = width
            self.window_height = height
            self.move_log_panel_width = MOVE_LOG_PANEL_WIDTH
            self.control_panel_width = CONTROL_PANEL_WIDTH


class StateOption(Enum):
    player_plays_both = auto()
    player_plays_white = auto()


class StateEvent(Enum):
    exit = auto()
    move_maid = auto()
    button_pressed = auto()
    

def row2colFromIndex(idx):
    return idx//DIMENSION, idx%DIMENSION


def indexFromRowCol(r, c):
    return DIMENSION*r + c


def convertStringToMove(pos, s, validMoves):
    f = sqN[s[:2]]
    t = sqN[s[-2:]]
    move = Move(f, t, "", 0, pos.board)
    for i, m in enumerate(validMoves):
        if move == m:
            return m
    return move


def convertMoveToString(pos, m):
    f = m.startSq
    t = m.endSq
    sm = nSq[f] + nSq[t]
    if m.piecePromotion in ('QRBN'):
        if pos.whiteToMove:
            sm += 'Q'
        else:
            sm += 'q'
    return sm


def undo_move(pos):
    global movingSquares, validMoves, gameOver, spos_log, movePlayed, movingSquares
    if len(movingSquares) > 0 and len(pos.moveLog) > 0:
        pos.undoMove()
        validMoves = pos.getValidMoves()
        gameOver = False
        pos.moveLog.pop()
        movingSquares.pop()
        movePlayed = None


def new_game():
    global gameOver, pos, sqSelected, playerClicks, sunfish_old, spos, sfm, movingSquares
    global spos_log, movePlayed, validMoves
    pos.initialize()
    validMoves = pos.getValidMoves()
    spos_log.clear()
    spos = sunfish_old.Position(sunfish_old.initial, 0, (True,True), (True,True), 0, 0)
    if pos.whiteToMove:
        print(' '.join(spos.board))
    else:
        print(' '.join(spos.rotate().board))
    sfmove = ''
    sqSelected = 64
    playerClicks = []
    pos.moveLog.clear()
    movingSquares.clear()
    movePlayed = None
    # del movingSquares[:]
    # movingSquares = []
    gameOver = False
    return spos


def Computer_move(sunfish, pos, spos):
    global option, movePlayed, AIThinKing, validMoves, option, spos_log
    if not AIThinKing: # and option == StateOption.player_plays_white:
        AIThinking = True
        returnQueue = Queue()
        moveFinderProcess = Process(target=sunfish.search, args=(spos, returnQueue))
        moveFinderProcess.start()
        moveFinderProcess.join()
        if not moveFinderProcess.is_alive():
            smove = returnQueue.get()
            if not pos.whiteToMove:
                sm = sunfish.render(119-smove[0]) + sunfish.render(119-smove[1])
            else:
                sm = sunfish.render(smove[0]) + sunfish.render(smove[1])
            # sm = sunfish.render(119-smove[0]) + sunfish.render(119-smove[1])
            spos_log.append(spos)
            spos = spos.move(smove)
            if not pos.whiteToMove:
                print(' '.join(spos.board))
            else:
                print(' '.join(spos.rotate().board))
            m = convertStringToMove(pos, sm, validMoves)
            pos.moveLog.append(m)
            temp = []
            temp.append(m.startSq)
            temp.append(m.endSq)
            movingSquares.append([temp])
            pos.makeMove(m)
            movePlayed = None
            pos.isGameOver(validMoves)
            aIThinking = False
    return spos


def Computer_hint(sunfish, spos):
    global option, AIThinKing, ValidMoves, pos
    if not AIThinKing:
        AIThinking = True
        returnQueue = Queue()
        moveFinderProcess = Process(target=sunfish.search, args=(spos, returnQueue))
        moveFinderProcess.start()
        moveFinderProcess.join()
        if not moveFinderProcess.is_alive():
            smove = returnQueue.get()
            if not pos.whiteToMove:
                sm = sunfish.render(119-smove[0]) + sunfish.render(119-smove[1])
            else:
                sm = sunfish.render(smove[0]) + sunfish.render(smove[1])
            m = convertStringToMove(pos, sm, validMoves)
            temp = []
            temp.append(m.startSq)
            temp.append(m.endSq)
            movingSquares.append([temp])
            aIThinking = False


def get_event():
    global pos, sqSelected, playerClicks, movingSquares, validMoves, gameOver, option
    global movePlayed, exitButton, newButton, hintButton, undoButton
    global aiOnButton, aiOffButton, goButton, option, sunfish, spos, buttonStates
    global spos_log

    for e in pg.event.get():
        if e.type == pg.QUIT:
            return StateEvent.exit
        elif e.type == pg.MOUSEBUTTONDOWN:
            if (exitButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[exitButton] = True
                return StateEvent.button_pressed
            elif (newButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[newButton] = True
                return StateEvent.button_pressed
            elif (hintButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[hintButton] = True
                return StateEvent.button_pressed
            elif (undoButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[undoButton] = True
                return StateEvent.button_pressed
            elif (aiToggleButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[aiToggleButton] = True
                return StateEvent.button_pressed
            elif (goButton.checkForInput(pg.mouse.get_pos())):
                resetButtonStates()
                buttonStates[goButton] = True
                return StateEvent.button_pressed
            elif option == StateOption.player_plays_both or \
                option == StateOption.player_plays_white and pos.whiteToMove:
                location = pg.mouse.get_pos()
                col = location[0]//SQ_SIZE
                if col >= 8: continue
                row = location[1]//SQ_SIZE
                sq = indexFromRowCol(row, col)

                if sqSelected == sq:
                    sqSelected = 64
                    playerClicks = []
                else:
                    sqSelected = sq
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    if 0 <= playerClicks[0] < 64 and 0 <= playerClicks[1] < 64:
                        row = playerClicks[1] // 8
                        if pos.whiteToMove and pos.board[playerClicks[0]] == "wp" and row == 0:
                            move = Move(playerClicks[0], playerClicks[1], "wQ", 4, pos.board)
                        elif not pos.whiteToMove and pos.board[playerClicks[0]] == "bp" and row == 7:
                            move = Move(playerClicks[0], playerClicks[1], "bQ", 4, pos.board)
                        else:
                            move = Move(playerClicks[0], playerClicks[1], "", 0, pos.board)
                        for i, m in enumerate(validMoves):
                            if move == m:
                                sm = convertMoveToString(pos, m)
                                smove = sunfish.parse(sm[0:2]), sunfish.parse(sm[2:4])
                                ssmove = list(smove)
                                if not pos.whiteToMove:
                                    ssmove[0] = 119-ssmove[0]
                                    ssmove[1] = 119-ssmove[1]
                                spos_log.append(spos)
                                spos = spos.move(ssmove)
                                if not pos.whiteToMove:
                                    print(' '.join(spos.board))
                                else:
                                    print(' '.join(spos.rotate().board))
                                pos.moveLog.append(m)
                                pos.makeMove(m)
                                movePlayed = m                                
                                temp = []
                                temp.append(m.startSq)
                                temp.append(m.endSq)
                                movingSquares.append([temp])
                                sqSelected = 64
                                playerClicks = []
                                return StateEvent.move_maid
                else:
                    playerClicks = [sqSelected]
                
        # elif e.type == pg.KEYDOWN:
        #     if e.key == pg.K_u:
        #         return StateEvent.move_undo
        #     elif e.key == pg.K_n:
        #         return StateEvent.new_game
    

def process_event(e):
    global validMoves, pos, spos, sunfish, option, paint, buttonStates, spos_log
    if e == StateEvent.exit:
        return False
    elif e == StateEvent.move_maid:
        validMoves = pos.getValidMoves()
        pos.isGameOver(validMoves)
        paint.update(pos)
    elif e == StateEvent.button_pressed:
        if buttonStates[exitButton]:
            return False
        elif buttonStates[newButton]:
            spos = new_game()
        elif buttonStates[hintButton]:
            Computer_hint(sunfish, spos)
        elif buttonStates[undoButton]:
            undo_move(pos)
            if len(spos_log) > 0:
                spos = spos_log[-1]
                spos_log.pop()
                paint.update(pos)
                gameOver = False
        elif buttonStates[aiToggleButton]:
            aiToggleButton.toggleColor()
            if option == StateOption.player_plays_both:
                option = StateOption.player_plays_white
                # return StateEvent.play_comp
            else:
                option = StateOption.player_plays_both
                # return StateEvent.play_manual
        elif buttonStates[goButton]:
            # sav_option = option
            # option == StateOption.player_plays_white
            spos = Computer_move(sunfish, pos, spos)
            validMoves = pos.getValidMoves()
            pos.isGameOver(validMoves)
            paint.update(pos)
            # print(' '.join(spos.rotate().board))
            # option = sav_option                
    elif movePlayed != None and option == StateOption.player_plays_white:
        # if not pos.whiteToMove:
        spos = Computer_move(sunfish, pos, spos)
        validMoves = pos.getValidMoves()
        pos.isGameOver(validMoves)
        paint.update(pos)
    if pos.checkMate or pos.staleMate:
        gameOver = True
    return True


def paint_update():
    global paint, exitButton, newButton, hintButton
    global undoButton, aiToggleButton, goButton
    paint.drawGameState(playerClicks, validMoves, movingSquares)
    exitButton.update()
    newButton.update()
    hintButton.update()
    undoButton.update()
    aiToggleButton.update()
    goButton.update()
    pg.display.flip()
    clock.tick(MAX_FPS)

def resetButtonStates():
    global buttonStates
    for k, _ in buttonStates.items():
        buttonStates[k] = False

def main():
    global pos, validMoves, sqSelected, playerClicks, movingSquares, gameOver
    global movePlayed, AIThinKing, exitButton, newButton, hintButton, undoButton
    global aiToggleButton, goButton, option, sunfish, spos, paint
    global clock, buttonStates, spos_log
    #------------------------------
    chess_game = game("funfish", BOARD_WIDTH, BOARD_HEIGHT)
    #------------------------------
    pg.init()
    screen = pg.display.set_mode((chess_game.window_width + chess_game.move_log_panel_width + chess_game.control_panel_width, chess_game.window_height))
    pg.display.set_caption("FunFish 2021")
    clock = pg.time.Clock()
    screen.fill(pg.Color((20, 110, 161)))     
    #------------------------------
    exitButton = Button(screen, 'red', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 460, "EXIT")
    newButton = Button(screen, 'green', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 50, "NEW")
    hintButton = Button(screen, 'green', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 100, "HINT")
    undoButton = Button(screen, 'green', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 150, "UNDO")
    aiToggleButton = Button(screen, 'gray', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 200, "AI")
    goButton = Button(screen, 'skyblue', BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 250, "GO")
    buttonStates = {exitButton: False, 
                    newButton: False, 
                    hintButton: False, 
                    undoButton: False,
                    aiToggleButton: False,
                    goButton: False}
    #------------------------------
    pos = GameState()
    #------------------------------
    sunfish = sunfish_old
    spos = sunfish.Position(sunfish.initial, 0, (True,True), (True,True), 0, 0)
    print(' '.join(spos.rotate().board))
    sfmove = ''
    spos_log = []
    #------------------------------
    paint = Drawing(screen, pos)
    validMoves = pos.getValidMoves()
    sqSelected = 64
    playerClicks = []
    movingSquares = []
    movePlayed = None
    gameOver = False
    #------------------------------
    option = StateOption.player_plays_both
    #------------------------------
    AIThinKing = False
    running = True
    #------------------------------
    while running:
        e = get_event()
        running = process_event(e)
        paint_update()
    #------------------------------        
    pg.quit()
    sys.exit


if __name__ == '__main__':
    main()
