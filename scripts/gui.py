from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color

class MainBoxLayout(BoxLayout):
    pass

class MainCanvas(Widget):
    def __init__(self, **kwargs):
        super(MainCanvas, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 0, 0, 1)
            self.rect = Rectangle(pos=(0, 0), size=(20, 20))

class MainApp(App):
    def build(self):
        self.title = 'N-Body Simulator'

main = MainApp()
main.run()