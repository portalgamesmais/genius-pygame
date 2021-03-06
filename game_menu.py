#importa dependências
from support_classes import Button
from CONFIG import WIDTH,HEIGHT,COLORS, QUIT, INIT, GAME
import pygame
import os

#inicializa o pygame mixer
pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()

#instancia objeto Sound (música do menu)
music = pygame.mixer.Sound(os.path.join("sprites","korobeiniki.wav"))
music.set_volume(0.2)
def main_menu(window, manager):

    #cria o título do jogo
    font_path = os.path.join("sprites","PressStart2P-Regular.ttf")
    font = pygame.font.Font(font_path,80)
    text = font.render("LUCIANIUS",True,(255,255,80))

    #define as dimensões, coordenadas e cria botões
    b_width = 300
    b_height = 100
    y_pos0 = HEIGHT/2 + 100 -(40+b_height)
    x_pos0 = WIDTH/2-(40+b_width)
    y_pos1 = HEIGHT/2 + 40 +100
    x_pos1 = WIDTH/2 + 40
    classic_button = Button(COLORS[0],x_pos0,y_pos0,b_width,b_height,"CLASSIC GENIUS", 50) 
    fast_button = Button(COLORS[1],x_pos1,y_pos0,b_width,b_height,"FAST GENIUS", 50) 
    crazy_button = Button(COLORS[2],x_pos0,y_pos1,b_width,b_height,"CRAZY GENIUS", 50)
    lucianius_button = Button(COLORS[3],x_pos1,y_pos1,b_width,b_height,"LUCIANIUS", 50) 
    buttons = [classic_button,fast_button,crazy_button,lucianius_button]

    #toca música do Tetris infinitamente
    music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT
            elif event.type == pygame.MOUSEMOTION:
                #botão reconhece o mouse
                for button in buttons:
                    button.react_to_mouse(event.pos)
            #caso botão seja pressionado:
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #inicia o jogo com a dificuldade de acordo com o botão pressionado
                if classic_button.isOver(event.pos):
                    return go_to_game([False, False], manager)
                elif fast_button.isOver(event.pos):
                    return go_to_game([True, False], manager)
                elif crazy_button.isOver(event.pos):
                    return go_to_game([False, True], manager)
                elif lucianius_button.isOver(event.pos):
                    return go_to_game([True, True], manager)

        #apaga e atualiza o frame   
        window.fill((0,0,0))
        window.blit(text,(WIDTH/2 - text.get_width()/2,90))

        for button in buttons:
            button.draw(window,(180,180,180))
        pygame.display.update()

#configura a dificuldade do jogo escolhida e para a música
def go_to_game(difficulty, manager):
    manager.difficulty = difficulty
    music.stop()
    return GAME