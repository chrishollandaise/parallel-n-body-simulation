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

import pickle
import os
import threading

class MainLayout(Widget):
    def _on_keyboard_down(self, *args):
        key = args[3]
        
        if key == 'w':
            self.sim.PARTICLE_SIZE += 1
        elif key == 's':
            if self.sim.PARTICLE_SIZE > 1:
                self.sim.PARTICLE_SIZE -= 1
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

        # UI Clock
        self.ui_clock = Clock.schedule_interval(self.update_ui, 1.0/60.0)

    def update_ui(self, dt):
        if self.sim.loader.is_alive():
            self.epochs_label.text = f"Epoch: N/A"
            self.nbodies_label.text = "N-Bodies: Loading..."
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

        # load the epochs from the pickle file
        self.loader = threading.Thread(target=self.load)
        self.loader.start()

        # gross increment starting from t0 of application
        self.INCREMENT = 0
        # current epoch
        self.CURRENT_EPOCH = 0
        # controls the speed of the simulation
        self.SPEED = 1
        # controls the particle scalar size
        self.PARTICLE_SIZE = 2.5
        # Controls whether the simulation is paused or not
        self.PAUSE = True
        # Controls whether the simulation has loaded the epochs or not
        self.LOADED = False
            
        with self.canvas:
            Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        if not self.loader.is_alive():
            self.simulate()
    
    def reset(self):
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
        self.SPEED = 1

    def simulate(self):
        self.CURRENT_EPOCH = self.INCREMENT % len(self.epochs)

        for idx, particle in enumerate(self.particles):
                particle.size = (self.PARTICLE_SIZE / self.scale, self.PARTICLE_SIZE / self.scale)
                if not self.PAUSE:
                    particle.pos = (self.epochs[self.CURRENT_EPOCH][idx][0] + self.height / 2, self.epochs[self.CURRENT_EPOCH][idx][1] + self.width / 2)
                
            # next epoch
        if not self.PAUSE:
            self.INCREMENT += self.SPEED

    def load(self):
        # load the epochs from the pickle file
        self.epochs = pickle.load(open(os.path.join(os.getcwd(), r'/Users/chris/parallel-n-body-simulation/profiles/1000steps_100_particles_2500spe.pkl'), 'rb'))
        # draw the starting positions of the particles
        self.draw_initial_state()
        self.LOADED = True

    def draw_initial_state(self):
         with self.canvas:
            self.particles = [Ellipse(size=(self.PARTICLE_SIZE, self.PARTICLE_SIZE),pos=(nbody[0], nbody[1])) for nbody in self.epochs[0]]
    

    def toggle_pause(self):
        self.PAUSE = not self.PAUSE

class MainApp(App):
    def build(self):
        # Layout
        self.title = 'N-Body Simulator'
        
        return MainLayout(self)

if __name__ == '__main__':
    MainApp().run()