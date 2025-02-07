#Importando e ajustando a janela do programa
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

#importações Kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy import platform
import random
from kivy.lang import Builder
from kivy.core.audio import SoundLoader


Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from transformacao import traformarcao_perpectiva, transformarcao, transformarcao_2D
    from acoes_usuarios import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed

    menu_widget = ObjectProperty()
    perpectiva_ponto_x = NumericProperty(0)
    perpectiva_ponto_y = NumericProperty(0)

    VERTICAL_NUMERO_LINHAS = 8
    VERTICAL_LINHAS_ESPACAMENTO = .4 # Porcetagem da largura da tela que aplicarei
    linhas_verticais = []

    HORIZONTAL_NUMERO_LINHAS = 15
    HORIZONTAL_LINHAS_ESPACAMENTO = .1 # Porcetagem da altura da tela que aplicarei
    linhas_horizontal = []


    VELOCIDADE = .4
    VELOCIDADE_X = 3.0
    velocidade_y = 0

    atual_offset_y = 0  
    atual_offset_X = 0

    atual_velocidade_x = 0
    atual_y_loop = 0

    numero_quadrados = 16
    quadrados = []
    quadrado_coordenadas = []

    nave = None
    NAVE_LARGURA = .1
    NAVE_ALTURA = 0.035
    NAVE_BASE_Y = 0.04
    nave_coordendas = [(0, 0), (0, 0), (0, 0)]

    estado_fim_de_jogo = False
    estado_game_esta_iniciado = False

    menu_title = StringProperty("Joguinho da Emanuela")
    menu_botao_title = StringProperty("iniciar")
    botao_largura = NumericProperty(0)
    potuacao_text = StringProperty()
    etapas_pontos_txt = StringProperty()

    audio_inicio = None
    audio_fim_de_jogo_impacto = None
    audio_game_over = None
    audio_reiniciar = None
    audio_musica_tema = None
    audio_tema_entrada = None
    audio_sound_jato = None
    audio_sound_vitoria = None

    avatar = None
    novoArte = None

    conta_blocos = 0
    level = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inicio_audio()
        self.inicio_linha_vertical()
        self.inicio_linha_horizontal()
        self.init_quandrados()
        self.init_nave()
        self.resetar_jogo()

        if self.e_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.atualizar, 1.0 / 60.0)
        self.audio_tema_entrada.play()

    def inicio_audio(self):
        self.audio_inicio = SoundLoader.load("audio/inicio_jogo.wav")
        self.audio_fim_de_jogo_impacto = SoundLoader.load("audio/fimdejo_impacto.wav")
        self.audio_game_over = SoundLoader.load("audio/game-over-voice.wav")
        self.audio_reiniciar = SoundLoader.load("audio/tentarnovamente.wav")
        self.audio_musica_tema = SoundLoader.load("audio/tema_musica.wav")
        self.audio_tema_entrada = SoundLoader.load("audio/tema_entrada.wav")
        self.audio_sound_jato = SoundLoader.load("audio/soud_jato.wav")
        self.audio_sound_vitoria = SoundLoader.load("audio/sound_vitoria.wav")

        self.audio_inicio.volume = .25
        self.audio_fim_de_jogo_impacto.volume = .6
        self.audio_game_over.volume = .25
        self.audio_reiniciar.volume = .25
        self.audio_musica_tema.volume = 1
        self.audio_tema_entrada.volume = .25
        self.audio_sound_jato.volume = 1
        self.audio_sound_vitoria.volume = 1
       
    
    def resetar_jogo(self):
        self.atual_offset_y = 0  
        self.atual_offset_X = 0
        self.atual_velocidade_x = 0
        self.atual_y_loop = 0
        self.quadrado_coordenadas = []
        self.potuacao_text = "Pontos: 0"
        self.etapas_pontos_txt = ""
        self.pre_preencher_coordenadas()
        self.gerar_coordendas_dos_quadrados()
        self.estado_fim_de_jogo = False
        self.botao_largura = .2
        self.level = 0
        
   
    def level_nivel(self, nivel):
        if nivel == 250:
            self.level = 0.02
        elif nivel == 500:
            self.level = 0.04
        elif nivel == 1000:
            self.level = 0.08
        elif nivel == 1250:
            self.level = 0.1
        elif nivel == 1500:
            self.level = 0.2
        elif nivel == 1750:
            self.level = 0.3
        elif nivel == 2000:
            self.level = 0.35
        elif nivel == 2250:
            self.level = 0.36
        elif nivel == 2500:
            self.level = 0.38
        elif nivel == 2750:
            self.level = 0.4
        elif nivel == 3000:
            self.level = 0.45

    def e_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False
    
    def init_nave(self):
        with self.canvas:
            Color(0, 0, 0, 0) #triagulo esta invisivel, ele é reposnsavel pela mecanica do jogo, pois o avatar e mero aspecto grafico 
            self.nave = Triangle()
            self.avatar = Image(source="img/avatar_veiculo_sem_fundo.png", size_hint=[.1, .2])
        

    def atualiza_nave(self):
        centro_tela_x = self.width / 2
        base_y = self.NAVE_BASE_Y * self.height
        nave_metade_da_largura = self.NAVE_LARGURA * self.width
        nave_altura = self.NAVE_ALTURA * self.height

        self.nave_coordendas[0] = (centro_tela_x - nave_metade_da_largura, base_y)
        self.nave_coordendas[1] = (centro_tela_x, base_y + nave_altura)
        self.nave_coordendas[2] = (centro_tela_x + nave_metade_da_largura, base_y)

        eixo_x_1, eixo_y_1 = self.transformarcao(*self.nave_coordendas[0])
        eixo_x_2, eixo_y_2 = self.transformarcao(*self.nave_coordendas[1])
        eixo_x_3, eixo_y_3 = self.transformarcao(*self.nave_coordendas[2])

        self.nave.points = [eixo_x_1, eixo_y_1, eixo_x_2, eixo_y_2, eixo_x_3, eixo_y_3] 
        
        avatar_eixo_x = (eixo_x_1 * 0.1) + eixo_x_1
        avatar_eixo_y = eixo_y_3 - (eixo_y_3 * 0.2)
        self.avatar.pos = (avatar_eixo_x, avatar_eixo_y)

    def verifica_nave_colisao(self):
        for coordenadas in range(0, len(self.quadrado_coordenadas)):
            lado_quadrado_x, lado_quadrado_y = self.quadrado_coordenadas[coordenadas]
            if lado_quadrado_y > self.atual_y_loop + 1:
                return False
            
            if self.verifica_nave_colisao_largura_quadrado(lado_quadrado_x, lado_quadrado_y):
                return True
            
        return False

    def verifica_nave_colisao_largura_quadrado(self, lado_quadrado_x, lado_quadrado_y):
        eixo_x_min, eixo_y_min = self.get_quadrado_coordenadas(lado_quadrado_x, lado_quadrado_y)
        eixo_x_max, eixo_y_max = self.get_quadrado_coordenadas(lado_quadrado_x + 1, lado_quadrado_y + 1)

        for coordenadas in range(0, 3):
            ponto_x, ponto_y = self.nave_coordendas[coordenadas]
            if eixo_x_min <= ponto_x <= eixo_x_max and eixo_y_min <= ponto_y <= eixo_y_max:
                return True
        return False
            


    def init_quandrados(self):
        with self.canvas:
            # RGB(238, 97, 170)
            Color((238/255), 97/255, 170/255)

            for i in range(0, self.numero_quadrados):
                self.quadrados.append(Quad())
    
    def pre_preencher_coordenadas(self):
        for i in range(0, 10):
            self.quadrado_coordenadas.append((0, i))
    
    def gerar_coordendas_dos_quadrados(self):
        ultimo_posicao_y = 0
        ultimo_posicao_x = 0
        # Limpar coordenas que saem fora da tela
        # lado_quandrado_y < sel.atual_loop_y
        for coordenada in range(len(self.quadrado_coordenadas) - 1, -1, -1):
            if self.quadrado_coordenadas[coordenada][1] < self.atual_y_loop:
                del self.quadrado_coordenadas[coordenada]

        if len(self.quadrado_coordenadas) > 0:
            ultimo_coordenda = self.quadrado_coordenadas[-1]
            ultimo_posicao_y = ultimo_coordenda[1] + 1
            ultimo_posicao_x = ultimo_coordenda[0]


        for i in range(len(self.quadrado_coordenadas), self.numero_quadrados):
                aleatorio = random.randint(0, 2)

                start_index = -int(self.VERTICAL_NUMERO_LINHAS / 2) + 1
                end_index = start_index + self.VERTICAL_NUMERO_LINHAS - 1

                if ultimo_posicao_x <= start_index:
                    aleatorio = 1
                
                if ultimo_posicao_x >= end_index:
                    aleatorio = 2

                self.quadrado_coordenadas.append((ultimo_posicao_x, ultimo_posicao_y))

                if aleatorio == 1:
                    ultimo_posicao_x += 1
                    self.quadrado_coordenadas.append((ultimo_posicao_x, ultimo_posicao_y))
                    ultimo_posicao_y += 1
                    self.quadrado_coordenadas.append((ultimo_posicao_x, ultimo_posicao_y))
                
                if aleatorio == 2:
                    ultimo_posicao_x -= 1
                    self.quadrado_coordenadas.append((ultimo_posicao_x, ultimo_posicao_y))
                    ultimo_posicao_y += 1
                    self.quadrado_coordenadas.append((ultimo_posicao_x, ultimo_posicao_y))

                ultimo_posicao_y += 1

    def inicio_linha_vertical(self):
        with self.canvas:
            Color(1, 1, 1)
            for linha in range(0, self.VERTICAL_NUMERO_LINHAS):
                self.linhas_verticais.append(Line())

    def get_line_x_from_index(self, index):
        centro_tela_eixo_x = self.perpectiva_ponto_x
        espaco_entre_linha = self.VERTICAL_LINHAS_ESPACAMENTO * self.width
        offset = index - 0.5
        line_x = centro_tela_eixo_x + offset * espaco_entre_linha + self.atual_offset_X
        return line_x

    def get_line_y_from_index(self, index):
        espaco_entre_linha_y = self.HORIZONTAL_LINHAS_ESPACAMENTO * self.height
        line_y = index * espaco_entre_linha_y - self.atual_offset_y
        return line_y

    def get_quadrado_coordenadas(self, lado_quadrado_x, lado_quandro_y):
        lado_quandro_y = lado_quandro_y - self.atual_y_loop
        eixo_x = self.get_line_x_from_index(lado_quadrado_x)
        eixo_y = self.get_line_y_from_index(lado_quandro_y)
        return eixo_x, eixo_y

    def atualiza_quadrado(self):
        for i in range(0, self.numero_quadrados):
            quadrado = self.quadrados[i]
            quadrado_coordenada = self.quadrado_coordenadas[i]
            eixo_x_min, eixo_y_min = self.get_quadrado_coordenadas(quadrado_coordenada[0], quadrado_coordenada[1])
            eixo_x_max, eixo_y_max = self.get_quadrado_coordenadas(quadrado_coordenada[0] + 1, quadrado_coordenada[1] + 1)

            eixo_x_1, eixo_y_1 = self.transformarcao(eixo_x_min, eixo_y_min)
            eixo_x_2, eixo_y_2 = self.transformarcao(eixo_x_min, eixo_y_max)
            eixo_x_3, eixo_y_3 = self.transformarcao(eixo_x_max, eixo_y_max)
            eixo_x_4, eixo_y_4 = self.transformarcao(eixo_x_max, eixo_y_min)

            quadrado.points = [eixo_x_1, eixo_y_1, eixo_x_2, eixo_y_2, eixo_x_3, eixo_y_3, eixo_x_4, eixo_y_4]


    def atualiza_linha_vertical(self):
        # 0 -1 1 2
        start_index = -int(self.VERTICAL_NUMERO_LINHAS / 2) + 1
        for linha in range(start_index, start_index + self.VERTICAL_NUMERO_LINHAS):
            linha_x = self.get_line_x_from_index(linha)

            eixo_x1, eixo_y1 = self.transformarcao(linha_x, 0)
            eixo_x2, eixo_y2 = self.transformarcao(linha_x, self.height)

            self.linhas_verticais[linha].points = [eixo_x1, eixo_y1, eixo_x2, eixo_y2]
    
    
    def inicio_linha_horizontal(self):
        with self.canvas:
            Color(1, 1, 1)
            for linha in range(0, self.HORIZONTAL_NUMERO_LINHAS):
                self.linhas_horizontal.append(Line())

    def atualiza_linha_horizontal(self):
        start_index = -int(self.VERTICAL_NUMERO_LINHAS / 2) + 1 
        end_index = start_index + self.VERTICAL_NUMERO_LINHAS - 1  

        eixo_x_minimo = self.get_line_x_from_index(start_index)
        eixo_x_maximo = self.get_line_x_from_index(end_index)

        for linha in range(0, self.HORIZONTAL_NUMERO_LINHAS):
            linha_y = self.get_line_y_from_index(linha)

            eixo_x1, eixo_y1 = self.transformarcao(eixo_x_minimo, linha_y)
            eixo_x2, eixo_y2 = self.transformarcao(eixo_x_maximo, linha_y)

            self.linhas_horizontal[linha].points = [eixo_x1, eixo_y1, eixo_x2, eixo_y2]
    
    def atualizar(self, delta):
        fator_tempo = delta * 60 # 60 é segundos, delta parametrorecebido la no INIT pela chamada do Clock
        self.atualiza_linha_vertical()
        self.atualiza_linha_horizontal()
        self.atualiza_quadrado()
        self.atualiza_nave()

        if not self.estado_fim_de_jogo and self.estado_game_esta_iniciado:
            velocidade_eixo_y = (self.VELOCIDADE + self.level) * self.height / 100 
            self.atual_offset_y += velocidade_eixo_y * fator_tempo + self.velocidade_y

            espaco_entre_linha_y = self.HORIZONTAL_LINHAS_ESPACAMENTO * self.height
            
            

            while self.atual_offset_y >= espaco_entre_linha_y:
                self.atual_offset_y -= espaco_entre_linha_y
                self.atual_y_loop += 1
                self.potuacao_text = "Pontos: " + str(self.atual_y_loop)

                

                if self.atual_y_loop in range(50, 10000, 50):
                    self.audio_sound_vitoria.play()
                    self.etapas_pontos_txt = "+" + str(self.atual_y_loop)

                if self.atual_y_loop in range(250, 6250, 250):
                    self.ids.img_vitoria_gif.opacity = 1
                    self.conta_blocos += 10
                    self.level_nivel(self.atual_y_loop)
                    
                else:
                    if self.conta_blocos > 0:
                        self.conta_blocos -= 1
                    elif self.conta_blocos == 0:
                        self.ids.img_vitoria_gif.opacity = 0
                    
                self.gerar_coordendas_dos_quadrados() 

        
            velocidade_eixo_x = self.atual_velocidade_x * self.width / 100
            self.atual_offset_X += velocidade_eixo_x * fator_tempo

        if not self.verifica_nave_colisao() and not self.estado_fim_de_jogo:
            self.estado_fim_de_jogo = True
            self.botao_largura = .4
            self.menu_title = "FIM   DE  JOGO"
            self.menu_botao_title = "Tentar Novamente"
            self.menu_widget.opacity =  1
            self.audio_musica_tema.stop()
            self.audio_fim_de_jogo_impacto.play()
            Clock.schedule_once(self.play_game_over_voice_sound, 1)
            

    def play_game_over_voice_sound(self, deltatime):
        if self.estado_fim_de_jogo:
            self.audio_game_over.play()

    def on_menu_botao_apertado(self):
        if self.estado_fim_de_jogo:
            self.audio_reiniciar.play()
        else:
            self.audio_inicio.play()
        self.audio_musica_tema.play()
        self.resetar_jogo()
        self.estado_game_esta_iniciado = True
        self.menu_widget.opacity =  0
        
        
        

class JoguinhoDaEmanuela(App):
    pass
    

JoguinhoDaEmanuela().run()