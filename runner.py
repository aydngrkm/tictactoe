import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

pygame.display.set_caption("Tic-Tac-Toe")

# Colors
black = (27, 27, 27)
white = (230, 230, 230)
lightWhite = (180, 180,180)
red = (230, 0, 0)
green = (0, 200, 0)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, lightWhite, (width / 8, height / 2, width / 4 + 3, 53))
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, lightWhite, (5*(width / 8), height / 2, width / 4 + 3, 53))
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Draw animated buttons
        ActivatedXButton = pygame.Rect((width / 8), (height / 2), width / 4 + 3, 53)
        ActivatedXRect = playX.get_rect()
        ActivatedXRect.center = ActivatedXButton.center

        ActivatedOButton = pygame.Rect(5*(width/8), (height /2), width / 4 + 3, 53)
        ActivatedORect = playO.get_rect()
        ActivatedORect.center = ActivatedOButton.center


        # Animate Buttons
        mouse = pygame.mouse.get_pos()
        if playXButton.collidepoint(mouse):
            pygame.draw.rect(screen, lightWhite, ActivatedXButton)
            screen.blit(playX, ActivatedXRect)
        if playOButton.collidepoint(mouse):
            pygame.draw.rect(screen, lightWhite, ActivatedOButton)
            screen.blit(playO, ActivatedORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            if playXButton.collidepoint(mouse):
                time.sleep(0.4)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.4)
                user = ttt.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)
                pygame.draw.line(screen, black, (width / 2 - 120, height / 2 - 120), (width / 2 - 120, height / 2 + 120), 4)
                pygame.draw.line(screen, black, (width / 2 - 120, height / 2 - 120), (width / 2 + 120, height / 2 - 120), 4)
                pygame.draw.line(screen, black, (width / 2 - 120, height / 2 + 118), (width / 2 + 120, height / 2 + 118), 4)
                pygame.draw.line(screen, black, (width / 2 + 118, height / 2 - 120), (width / 2 + 118, height / 2 + 120), 4)

                if board[i][j] != ttt.EMPTY:
                    if board[i][j] == ttt.X:
                        moveColor = red
                    elif board[i][j] == ttt.O:
                        moveColor = green
                    move = moveFont.render(board[i][j], True, moveColor)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title

        if user == ttt.X:
            userSymbol = "X"
            userColor = red
            AiSymbol = "O"
            AiColor = green
        elif user == ttt.O:
            userSymbol = "O"
            userColor = green
            AiSymbol = "X"
            AiColor = red

        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over, Winner Is: "
                userText = largeFont.render(AiSymbol, True, AiColor)
                userTextRect = userText.get_rect()
                userTextRect.topleft = (titleRect.right, titleRect.top)
                screen.blit(userText, userTextRect)
        elif user == player:
            title = f"Play as "
            userText = largeFont.render(userSymbol, True, userColor)
            userTextRect = userText.get_rect()
            userTextRect.topleft = (titleRect.right, titleRect.top)
            screen.blit(userText, userTextRect)
        else:
            title = f"Computer thinking..."

        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2) - 15, 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            backButton = pygame.Rect(width / 3, height - 65, width / 3 + 3, 53)
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            backButtonRect = againRect = again.get_rect()
            backButtonRect.center = backButton.center
            againRect.center = againButton.center
            pygame.draw.rect(screen, lightWhite, backButton)
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, backButtonRect)
            screen.blit(again, againRect)

            ActivatedAgainButton = pygame.Rect(width / 3, height - 65, width / 3 + 3, 53)
            ActivatedAgainRect = again.get_rect()
            ActivatedAgainRect.center = ActivatedAgainButton.center

            mouse = pygame.mouse.get_pos()
            click, _, _ = pygame.mouse.get_pressed()
            if againButton.collidepoint(mouse):
                pygame.draw.rect(screen, lightWhite, ActivatedAgainButton)
                screen.blit(again, ActivatedAgainRect)
            if click == 1:
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()
