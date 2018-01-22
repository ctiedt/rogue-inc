import pyglet
from pyglet.window import key

win=pyglet.window.Window()
label=pyglet.text.Label("Guten Tag Welt")
keybstate=key.KeyStateHandler() #keybstate für Keyboardstate
##win.push_handlers(keybstate)

@win.event
def on_draw():
    win.clear()
#    label.draw()

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

@win.event
def update(dt):
    # @keybstate(key.W)
    print("MINE!")

##print(keybstate[key.W])


pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
