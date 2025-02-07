from kivy.uix.relativelayout import RelativeLayout

def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard.unbind(on_key_up=self.on_keyboard_up)
        self.keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.atual_velocidade_x = self.VELOCIDADE_X
    elif keycode[1] == 'right':
        self.atual_velocidade_x = -self.VELOCIDADE_X
    elif keycode[1] == 'up':
        self.audio_musica_tema.volume = .25
        self.audio_sound_jato.volume = 1
        self.audio_sound_jato.play()
        self.velocidade_y += 1
        
        
    return True


def on_keyboard_up(self, keyboard, keycode):
    self.atual_velocidade_x = 0
    self.velocidade_y = 0
    self.audio_musica_tema.volume = 1
    self.audio_sound_jato.stop()

def on_touch_down(self, touch):
    if not self.estado_fim_de_jogo and self.estado_game_esta_iniciado:
        lado_2_inicio = ((self.width * 0.9) / 2) * 1.2
        if touch.x < (self.width * 0.9) / 2:
            #print(" <==")
            self.atual_velocidade_x = self.VELOCIDADE_X
        elif touch.x > lado_2_inicio and touch.x < self.width:
            #print(" ==>")
            self.atual_velocidade_x = -self.VELOCIDADE_X
        else:
            #print("frente")
            self.velocidade_y += 1
            self.audio_musica_tema.volume = .25
            self.audio_sound_jato.volume = 1
            self.audio_sound_jato.play()
    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    #print("UP")
    self.atual_velocidade_x = 0
    self.velocidade_y = 0
    self.audio_musica_tema.volume = 1
    self.audio_sound_jato.stop()