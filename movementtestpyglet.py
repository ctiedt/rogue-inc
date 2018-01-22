import pyglet
import mapgen.py
import key

kezbstate=kez.KeyStateHandler()

@win.event
def on_key_press(symbol, modifiers):
    if symbol== key.W:
        print('The Key "W" was pressed')
    elif symbol== key.A:
        print('The Key "A" was pressed')
    elif symbol== key.S:
        print('The Key "S" was pressed')
    elif symbol== key.D:
        print('The Key "D" was pressed')
    elif symbol== key.E:
        print('Interaction has been chosen')

