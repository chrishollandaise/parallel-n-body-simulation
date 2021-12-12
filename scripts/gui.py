from kivy.config import Config
# Configure the window. before importing Window
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.clock import Clock
from kivy.lang.builder import Builder

import pickle
import os
import threading

class MainLayout(Widget):
    def _on_keyboard_down(self, *args):
        key_code, key = args[2], args[3]
        
        if key is not None and key.isnumeric():
            self.TYPING = True
            self.sim.PAUSE = True
            self.increment_string += key

            if(int(self.increment_string)) > self.sim.MAX_EPOCH:
                self.increment_string = str(self.sim.MAX_EPOCH)
                self.sim.offset_epoch(int(self.increment_string))
                self.TYPING = False

        elif key_code == 42:
            self.increment_string = self.increment_string[:-1]
        elif key_code == 40:
            if len(self.increment_string) <= 0:
                return
            self.sim.PAUSE = True
            self.sim.offset_epoch(int(self.increment_string))
            self.increment_string = ""
            self.TYPING = False
        if key == 'w':
            self.sim.PARTICLE_SIZE += 1
        elif key == 's':
            if self.sim.PARTICLE_SIZE > 1:
                self.sim.PARTICLE_SIZE -= 1
        elif key == 'd':
            self.sim.increase()
        elif key == 'h':
            self.toggle_help()
        elif key == 'a':
            self.sim.decrease()
        elif key == 'q':
            self.app.stop()
        elif key == ' ':
            self.sim.toggle_pause()
        elif key == 'r':
            self.sim.reset()
        elif key == 'b':
            self.sim.reverse()
        elif key == 'f':
            self.sim.forward()

    def __init__(self, app, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        
        # Bindings
        Window.bind(on_key_down=self._on_keyboard_down)
        self.app = app

        # ids
        self.sim = self.ids.sim
        self.epochs_label = self.ids.epoch
        self.nbodies_label = self.ids.n_bodies
        self.help_label = self.ids.help
        self.speed_label = self.ids.speed

        # variables
        self.increment_string = ""
        self.TYPING = False
        self.HELP_ON = False
        self.HELP_TEXT = '''HELP: 
                          \n\tf: Move simulation forward   | \tb: Move simulation backward
                          \n\tw: Increase particle size    | \ts: Decrease particle size
                          \n\td: Increase simulation speed | \ta: Decrease simulation speed
                          \n\tr: Reset simulation          | \tSPACE: Pause simulation
                          \n\th: Toggle help               | \tq: Quit      
                          \nAdditionally, typing an epoch number and pressing enter will jump to that epoch.
                          '''
        self.help_label.text = self.HELP_TEXT
        # UI Clock
        self.ui_clock = Clock.schedule_interval(self.update_ui, 1.0/60.0)
    
    def toggle_help(self):
        print(self.help_label.color)
        self.HELP_ON = not self.HELP_ON
        self.help_label.color = [0, 1, 0, int(self.HELP_ON)]

    def update_ui(self, dt):
        if not self.sim.LOADED:
            self.epochs_label.text = f"Epoch: N/A"
            self.nbodies_label.text = "N-Bodies: Loading..."
        else:
            self.speed_label.text = "X" + str(self.sim.SPEED)
            if self.TYPING:
                self.epochs_label.text = f"Epoch: {self.increment_string}"
            else:
                self.epochs_label.text = f"Epoch: {self.sim.CURRENT_EPOCH}"
                self.nbodies_label.text = f"N-Bodies: {len(self.sim.epochs[0])}"

class Simulation(Scatter):
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                self.scale = self.scale * 1.1
            elif touch.button == 'scrollup':
                self.scale = self.scale * 0.9
        else:
            super(Simulation, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        # Disable the default touch handler
        pass

    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)

        # path to the pickle file
        self.path = self.get_chosen_profile()

        # load the epochs from the pickle file
        self.loader = threading.Thread(target=self.load)
        self.loader.start()

        # gross increment starting from t0 of application
        self.INCREMENT = 400_000
        # current epoch
        self.CURRENT_EPOCH = 0
        # max epoch, will be set when loaded
        self.MAX_EPOCH = 0
        # controls the speed of the simulation
        self.SPEED = 1
        # max speed of the simulation
        self.MAX_SPEED = 256
        # controls the particle scalar size
        self.PARTICLE_SIZE = 2.5
        # Controls whether the simulation is paused or not
        self.PAUSE = True
        # Controls whether the simulation has loaded the epochs or not
        self.LOADED = False
        # FPS
        self.FPS = 60.0
            
        with self.canvas:
            self.sim_clock = Clock.schedule_interval(self.update, 1.0/self.FPS)

    def update(self, dt):
        if self.LOADED:
            self.simulate()
    
    def offset_epoch(self, epoch_offset):
        self.INCREMENT = epoch_offset

    def reset(self):
        self.SPEED = 1

        with self.canvas:
            self.canvas.clear()
        
        self.CURRENT_EPOCH = 0 if self.SPEED >= 0 else len(self.epochs) - 1
        self.INCREMENT = self.CURRENT_EPOCH
        
        if not self.LOADED:
            self.loader = threading.Thread(target=self.load)
            self.loader.start()
        else:
            self.draw_initial_state()
    
    def reverse(self):
        self.SPEED *= -1
    
    def forward(self):
        self.SPEED = abs(self.SPEED)
    
    def increase(self):
        if abs(self.SPEED) < self.MAX_SPEED:
            self.SPEED *= 2
    
    def decrease(self):
        if abs(self.SPEED) > 1:
            self.SPEED //= 2
            
    def simulate(self):
        self.CURRENT_EPOCH = self.INCREMENT % len(self.epochs)

        for idx, particle in enumerate(self.particles):
                particle.size = (self.PARTICLE_SIZE / self.scale, self.PARTICLE_SIZE / self.scale)
                if not self.PAUSE:
                    particle.pos = (self.epochs[self.CURRENT_EPOCH][idx][0] + self.height / 2, self.epochs[self.CURRENT_EPOCH][idx][1] + self.width / 2)
                
            # next epoch
        if not self.PAUSE:
            self.INCREMENT += self.SPEED

    def get_chosen_profile(self):
        path = os.path.join(os.getcwd(), 'profiles')
        profiles = os.listdir(path)
        
        for idx, profile in enumerate(profiles):
            if profile.endswith('.pkl'):
                print(f"{idx}: {profile}")
                
        choice = int(input("Choose a profile: "))

        return os.path.join(path, profiles[choice])

    def load(self):
        # load the epochs from the pickle file
        self.epochs = pickle.load(open(self.path, 'rb'))
        # draw the starting positions of the particles
        self.draw_initial_state()
        self.LOADED = True
        self.MAX_EPOCH = len(self.epochs) - 1

    def draw_initial_state(self): 
         with self.canvas:
            self.particles = [Ellipse(size=(self.PARTICLE_SIZE, self.PARTICLE_SIZE),pos=(nbody[0], nbody[1])) for nbody in self.epochs[0]]
    
    def toggle_pause(self):
        self.PAUSE = not self.PAUSE

class MainApp(App):
    def build(self):
        # Layout
        self.title = 'N-Body Simulator'
        Builder.load_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui.kv'))

        return MainLayout(self)

if __name__ == '__main__':
    MainApp().run()