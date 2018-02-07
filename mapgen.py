#_d Project: Rogue Inc.
#_d Class: Map Generator
#Sprint I
#_d Clemens Tiedt

import random
import zipfile

#Verschiedene allgemeine Utensilien

dist_manhattan = lambda x, y: sum(abs(p - q) for p, q in zip(x, y))
dist_euclidean = lambda x, y: (sum((p - q)**2 for p, q in zip(x, y)))**0.5

OPPOSITE_DIRECTIONS = {"n":"s", "s":"n", "e":"w", "w":"e"}

class MapGenerator:

    def __init__(self, debug=False):
        self.debug=debug
        self.mp = [[1 for y in range(45)] for x in range(45)] #Erstelle einen 2D-Array 45x45 aus Nullen; die Karte hat *immer* die Größe 45x45
        self.path = self.gen_path()
        self.generate_rooms()
        #Metdaten:
        self.start = (self.path[1][0] + 7, self.path[1][1] + 7)
        self.end = None
        self.name = self.generate_name()

    def generate_name(self):
        """Generiert einen Bezeichner für die Map"""
        type_ = random.choice(("Dungeon", "Lair", "Caves", "Labyrinth"))
        #syllables = ["An", "Ab", "Ar", "Ur", "Un", "Kan", "Lor", "Wun", "Wil", "Har", "Hor", "Ko", "Luz", "Laz", "Ban"]
        syllables = [i + j for i in "BCDFGHJKLMNPQRSTVWXYZ" for j in "aeiou"] + [i + j for i in "AEIOU" for j in "bcdfghjklmnpqrstvwxyz"]
        owner = random.choice(syllables) + random.choice(("", "-")) + random.choice(syllables).lower()
        title = random.choice(("Abominable", "Cruel", "Cunning", "Crazy", "Reasonable", "Traitor"))
        return "{} of {} the {}".format(type_, owner, title)

    def gen_path(self):
        """Generiert einen Weg durch die Map auf einem 3x3-Gitter"""
        cpos = [random.randint(0, 2), 0]
        start = cpos.copy()
        path = ""
        while cpos[1] < 3: #_d Generator "bewegt" sich, bis er den y-Wert 3 erreicht nach unten 
            movements = [(0, 1)] #Bewegung nach unten ist immer erlaubt
            if cpos[0] > 0: #Wenn möglich, Bewegung nach links erlauben
                    movements.append((-1, 0))
                    movements.append((-1, 0))
            if cpos[0] < 2: #Wenn möglich, Bewegung nach rechts erlauben
                    movements.append((1, 0))
                    movements.append((1, 0))
            mv = random.choice(movements) #Bewegung nach l/r sind zweimal so wahrscheinlich, wie Bewegung nach unten
            if mv in [(-1, 0), (1, 0)]: #Bewegungen nach l/r können in einer Reihe stattfinden
                    while cpos[0] + mv[0] < 2 and cpos[0] + mv[0] > 0 and random.randint(0, 1):
                            cpos = [cpos[0] + mv[0], cpos[1] + mv[1]] #Aktualisiere Position
                            if mv == (-1, 0):
                                    path += "w" #Wenn eine Bewegung ausgeführt wird, wird sie dem Weg hinzugefügt
                            else:
                                    path += "e"
            else:
                    cpos = [cpos[0] + mv[0], cpos[1] + mv[1]]
                    path += "s"
        return path[:-1], start #_d Da der letzte Schritt im Pfad einen Schritt zu weit nach unten geht, wird er entfernt.

    def generate_room(self, entrances, sx, sy):
        """Generates a room with entrances/exits in the specified directions starting at (sx|sy)"""
        if "n" in entrances:
            for x in range(5, 10):
                for y in range(10):
                    self.mp[sx+x][sy+y] = 0
        if "e" in entrances:
            for x in range(5, 15):
                for y in range(5, 10):
                    self.mp[sx+x][sy+y] = 0
        if "s" in entrances:
            for x in range(5, 10):
                for y in range(5, 15):
                    self.mp[sx+x][sy+y] = 0
        if "w" in entrances:
            for x in range(10):
                for y in range(5, 10):
                    self.mp[sx+x][sy+y] = 0

    def generate_rooms(self):
        cpos = self.path[1]
        for i, letter in enumerate(self.path[0]):
            spos = [cpos[0]*15, cpos[1]*15]
            entrances = ""
            entrances += letter
            if i > 0:
                entrances += OPPOSITE_DIRECTIONS[self.path[0][i-1]]
            self.generate_room(entrances, spos[0], spos[1])
            if i == len(self.path[0]) - 1:
                self.end = (spos[0] + 7, spos[1] + 7)
            if letter == "s":
                cpos = [cpos[0], cpos[1]+1]
            if letter == "e":
                cpos = [cpos[0]+1, cpos[1]]
            if letter == "w":
                cpos = [cpos[0]-1, cpos[1]]

    def map_as_string(self):
        """2D-Array in String mit Zeilenenden umwandeln"""
        return "\n".join(["".join(str(e) for e in row) for row in self.mp])

    def convert_string_map(self, text):
        """String in 2D-Array umwandeln"""
        return [[int(text[x + y]) for y in range(45) if text[x + y] != "\n"] for x in range(45)]

    def save(self, path):
        """Speichert die Karte als Zip-Datei"""
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("/map.txt", self.map_as_string())

    def load(self, path):
        """Lädt die Karte aus einer Zip-Datei"""
        #_d TODO: Abfrage, ob Datei tatsächlich existiert
        #_d TODO: Überprüfen, ob Archiv nötige Dateien enthält
        with zipfile.ZipFile(path) as zf:
            with zf.open("/map.txt") as mapfile:
                self.mp = self.convert_string_map(mapfile.read().decode())
