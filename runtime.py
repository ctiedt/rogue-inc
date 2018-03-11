#Laufzeitumgebung von Rogue Inc.

import pyglet, functools
from pyglet.window import key, mouse
import mapgen, character, enemy

DEBUG = False

def iodec(func):
    if DEBUG:
        @functools.wraps(func)
        def _iodec(*args, **kwargs):
            output = func(*args, **kwargs)
            print("{0}({1}, {2}): {3}".format(func.__name__, args, kwargs, output))
            return output
        return _iodec
    else:
        return lambda *args, **kwargs: func(*args, **kwargs)

class GameWindow(pyglet.window.Window):

    @iodec
    def __init__(self, path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = pyglet.text.Label("", x=0, y=self.height-10, font_name="Courier New", font_size=10, multiline=True, width=2000)
        self.char_label = pyglet.text.Label("", x=0, y=self.height-10, font_name="Courier New", font_size=10, multiline=True, width=2000, color=(255, 0, 0, 255))
        self.meta_label = pyglet.text.Label("", x=720, y=self.height-10, font_name="Courier New", font_size=10, multiline=True, width=2000)
        self.notifications_label = pyglet.text.Label("No notifications yet\n", x=0, y=self.height - 720, font_name="Courier New", font_size=10, multiline=True, width=2000)
        self.mg = mapgen.MapGenerator(path)
        self.pos = list(reversed(self.mg.start))
        self.Character = character.Character(*self.pos, "Maiq")
        self.enemies = [enemy.Enemy(*p) for p in self.mg.enemies]

    @iodec
    def translate_map(self, mp):
        output = ""
        for x in range(45):
            for y in range(44):
                if (x, y) == (self.Character.x, self.Character.y):
                    output += "@"
                elif (y, x) in self.mg.enemies:
                    output += "§"
                elif [x, y] == list(reversed(self.mg.end)):
                    output += "G" #chr(1758)
                else:
                    output += "#" if mp[y][x] == 1 else "."
                output += " "
            output += "#\n" if mp[y+1][x] == 1 else ".\n"
        return output

    def translate_chars(self, mp):
        output = ""
        for x in range(45):
            for y in range(44):
                if (x, y) == (self.Character.x, self.Character.y):
                    output += "@ "
                if (y, x) in [(en.x, en.y) for en in self.enemies]:
                    output += "§ "
                output += "  "
            output += "\n"
        return output

    def generate_meta(self):
        output = "Map: " + self.mg.name + "\n"
        output += "Name: " + self.Character.name + "\n"
        output += "Health: " + str(self.Character.health) + "\n"
        output += "Level: " + str(self.Character.level) + "\n"
        output += "Position: " + str((self.Character.x, self.Character.y)) + "\n"
        return output
    
    @iodec
    def on_draw(self):
        self.clear()
        self.label.text = self.translate_map(self.mg.mp)
        self.char_label.text = self.translate_chars(self.mg.mp)
        self.meta_label.text = self.generate_meta()
        self.label.draw()
        self.char_label.draw()
        self.meta_label.draw()
        self.notifications_label.draw()
        
    @iodec
    def on_key_press(self, symbol, modifiers):
        args = {"map":self.mg.mp, "input":(0, 0), "atk":self.enemies, "player":self.Character}
        if symbol == key.RIGHT:
            args["input"] = (0, 1)
        if symbol == key.LEFT:
            args["input"] = (0, -1)
        if symbol == key.UP:
            args["input"] = (-1, 0)
        if symbol == key.DOWN:
            args["input"] = (1, 0)
        self.update(args)
        self.Character.update(args)

    def update(self, args):
        if "input" in args.keys():
            if args["input"] == key.ESCAPE:
                self.close()
        if (self.Character.x, self.Character.y) == tuple(reversed(self.mg.end)):
            self.notifications_label.text += "Congratulations! You reached the goal\n"
        for en in self.enemies:
            self.notifications_label.text += str((en.y, en.x)) + ": " + str(en.health)
        self.notifications_label.text += "\n"

if __name__ == "__main__":
    path = None
##    if input("Please specify if you would like to [l]oad an existing map or create a [n]ew one: ") == "l":
##        path = input("Please specify the file path: ")
    win = GameWindow(path, fullscreen=True)
    pyglet.app.run()
