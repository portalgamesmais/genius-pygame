import pygame
import pygame.gfxdraw
from random import randint
from math import pi,sin,cos
from support_classes import Circle, Note
from CONFIG import HEIGHT,WIDTH, DRAW_RADIUS, COLORS, FREQUENCIES, QUIT, END, INIT,FPS
import os


class GeniusGame:
    def __init__(self, window, manager):
        self.window = window
        self.manager = manager
        self.luci = pygame.image.load(os.path.join("sprites","Lucy High Tech.png")).convert_alpha()
        self.luci_sound = pygame.mixer.Sound(os.path.join("sprites","scream.ogg"))
        self.buzzer_sound = pygame.mixer.Sound(os.path.join("sprites","buzzer.wav"))

    def start_game(self):
        #reseta valor de propriedades para comecar um novo jogo
        self.sequence = []
        self.input_sequence = []
        self.circles = []
        self.actions_list = []
        self.current_index = 0
        self.awaiting_input = False
        self.difficulty = self.manager.difficulty
        self.waiting_time = 300
        self.flash_time = 1000
        self.game_over = False
        #inicia um jogo
        return self.game_loop()

    #adciona um botao na sequencia
    def increment_sequence(self):
        round = len(self.sequence)
        if self.difficulty[1] and round % 4 == 0 and round !=0 and len(self.circles) < 8:
            next_i = len(self.circles)
            self.circles.append(Circle(50,COLORS[next_i],FREQUENCIES[next_i]))
            print(round)
            print(COLORS[round])
            self.calculate_scene()
            self.draw_scene()

        if self.difficulty[0] and round % 2 == 0 and round !=0:
            self.flash_time = int(self.flash_time * (0.85 if self.flash_time > 300 else 1))
            self.waiting_time = int(self.waiting_time * (0.95 if self.waiting_time > 200 else 1))
        
        self.sequence.append(randint(0, len(self.circles)-1))
        self.play_sequence()
        

   #reproduz a sequencia correta
    def play_sequence(self):
        actions = []
        for i in self.sequence:
            action = {"function": self.circles[i].flash, "arguments": (self.window, self.flash_time), "delay": self.waiting_time}
            action2 = {"function": self.draw_scene, "delay": self.flash_time}
            
            actions.append(action)
            actions.append(action2)
        await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
        self.actions_list += actions + [await_input]

    #lida com input nos botes
    def new_input(self, circle):
        self.enable_input(False)
        #caso o tenha pressionado o botao correto
        if self.circles.index(circle) == self.sequence[self.current_index]:
            #pisquarr o botao
            circle.flash(self.window, 300)
            await_input = {"function": self.enable_input, "arguments": (True,), "delay": 0}
            action = {"function": self.draw_scene, "delay":300}
            self.actions_list += [action,await_input]
            #esperar proximo input ou inicar proxima rodada
            self.current_index += 1
            if self.current_index == len(self.sequence):
                self.current_index = 0
                action = {"function": self.increment_sequence, "delay":500}
                self.actions_list.append(action)
        else:
            #caso tenha pressionado botao incorreto encerrar jogo
            self.end_game()
            


    
    def enable_input(self,enable):
        self.awaiting_input = enable

    #posiciona os botes ao redor de uma circuferencia imaginaria com raio
    # DRAW_RADIUS e com espacamentos em angulo iguais
    def calculate_scene(self):
        for i, circle in enumerate(self.circles):
            angle = i*2*pi/len(self.circles) + pi/4
            x = int(WIDTH/2 + cos(angle) * DRAW_RADIUS)
            y = int(HEIGHT/2 + sin(angle) * DRAW_RADIUS)
            circle.move_to((x, y))

    #desenha os elementos da cena na tela
    def draw_scene(self):
        self.window.fill((0, 0, 0))
        for circle in self.circles:
            circle.draw(self.window)
        font = pygame.font.SysFont(None, 48)
        text = font.render("Rodada: {}".format(len(self.sequence)), 1, (255, 255, 255))
        self.window.blit(text, (20, 20))

    # encerra o jogo
    def end_game(self):
        #aparece tela vermelha por 1.5 segundos
        self.window.fill((255,0,0))
        action = {"function":self.set_game_over,"arguments":(True,),"delay":1500}
        self.actions_list.append(action)
        #caso modo seja lucianius aparece imagem e toca som de grito
        if self.difficulty == [True, True]:
            self.window.blit(self.luci,(WIDTH/2-self.luci.get_width()/2, HEIGHT/2-self.luci.get_height()/2))
            self.luci_sound.play()
        else:
            #caso contrario toca som de buzina
            self.buzzer_sound.play()


    def set_game_over(self,over):
        self.game_over = over

    #loop de jogo
    def game_loop(self):
        #cria botoes inicias
        for i in range(4):
            self.circles.append(Circle(50,COLORS[i], FREQUENCIES[i]))
            print(COLORS[i])
        self.calculate_scene()
        self.draw_scene()
        #adiciona primerio circulo a sequencia correta 
        self.increment_sequence()

        #variaveis para sistema de delay de funcoes
        running_action = False
        delay = 0
        timer = 0
        clock = pygame.time.Clock()

        while True:
            # ----- Trata eventos
            dt = clock.tick(FPS)
            # ir para tela game over caso jogo tenha acabado
            if self.game_over == True:
                return END

            #sistema de delay que nao deixa jogo irresponsivel
            if not running_action and len(self.actions_list) > 0:
                delay = self.actions_list[0]["delay"]
                timer = 0
                running_action = True

            if running_action:
                timer += dt
                if timer >= delay:
                    action = self.actions_list[0]
                    if "arguments" in action:
                        action["function"](*action["arguments"])
                    else:
                        action["function"]()
                    if len(self.actions_list) > 0:
                        del self.actions_list[0]
                    running_action = False

            # tratar dos eventos
            for event in pygame.event.get():
                #fechar jogo caso feche a janela
                if event.type == pygame.QUIT:
                    return QUIT
                #ir para menu principal caso aperte esc
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return INIT
                #lidar com botao pressionado
                elif self.awaiting_input and event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            
                            for circle in self.circles:
                                if circle.colision(event.pos):
                                    self.new_input(circle)                
            
            pygame.display.update()  # Mostra o novo frame para o jogador
