#_d Project: Rogue Inc.
#_d Class: Map Generator
#Sprint I
#_d Clemens Tiedt

import random, zipfile, json, os

#Verschiedene allgemeine Utensilien

dist_manhattan = lambda x, y: sum(abs(p - q) for p, q in zip(x, y))
dist_euclidean = lambda x, y: (sum((p - q)**2 for p, q in zip(x, y)))**0.5

OPPOSITE_DIRECTIONS = {"n":"s", "s":"n", "e":"w", "w":"e"}

class MapGenerator:

    def __init__(self, path=None, debug=False):
        self.debug=debug
        if path is None:
            self.mp = [[1 for y in range(45)] for x in range(45)] #Erstelle einen 2D-Array 45x45 aus Einsen; die Karte hat *immer* die Größe 45x45
            self.enemies = [] #Liste der Positionen, an denen Feinde gespawnt werden
            self.gold = [] #Liste der Positionen, an denen Goldstücke liegen
            self.path = self.gen_path()
            self.end = None #Muss hierhin, weil es sonst die Änderung in self.generate_rooms() überschreibt...
            self.generate_rooms()
            #Metadaten:
            self.start = ((self.path[1][0] * 15) + 7, (self.path[1][1] * 15) + 7)
            self.name = self.generate_name()
        else:
            self.load(path)

    def generate_name(self):
        """Generiert einen Bezeichner für die Map"""
        type_ = random.choice(("Dungeon", "Lair", "Caves", "Labyrinth"))
        #syllables = ["An", "Ab", "Ar", "Ur", "Un", "Kan", "Lor", "Wun", "Wil", "Har", "Hor", "Ko", "Luz", "Laz", "Ban"]
        syllables = [i + j for i in "BCDFGHJKLMNPQRSTVWXYZ" for j in "aeiou"] + [i + j for i in "AEIOU" for j in "bcdfghjklmnpqrstvwxyz"]
        owner = random.choice(syllables) + random.choice(("", "-")) + random.choice(syllables).lower()
        title = random.choice(("Abominable", "Cruel", "Cunning", "Crazy", "Reasonable", "Traitor", "Regent"))
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
            if mv in [(-1, 0), (1, 0)]: #Bewegungen nach l/r können mehrmals hintereinander stattfinden
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
        """Generiert einen Raum mit Eingängen/Ausgängen an den gegebenen Seiten, der bei (sx|sy) beginnt"""
        enemy_spawned = False
        gold_spawned = False
        if "n" in entrances:
            for x in range(5, 10):
                for y in range(10):
                    self.mp[sx+x][sy+y] = 0
            if not enemy_spawned and random.randint(0, 1):
                self.enemies.append((sx + 7, sy + 5))
                enemy_spawned = True
        if "e" in entrances:
            for x in range(5, 15):
                for y in range(5, 10):
                    self.mp[sx+x][sy+y] = 0
            if not enemy_spawned and random.randint(0, 1):
                self.enemies.append((sx + 10, sy + 7))
                enemy_spawned = True
        if "s" in entrances:
            for x in range(5, 10):
                for y in range(5, 15):
                    self.mp[sx+x][sy+y] = 0
            if not enemy_spawned and random.randint(0, 1):
                self.enemies.append((sx + 7, sy + 10))
                enemy_spawned = True
        if "w" in entrances:
            for x in range(10):
                for y in range(5, 10):
                    self.mp[sx+x][sy+y] = 0
            if not enemy_spawned and random.randint(0, 1):
                self.enemies.append((sx + 5, sy + 7))
                enemy_spawned = True

    def generate_rooms(self):
        """Generiert zusammenhängend alle Räume, die auf dem Weg liegen müssen"""
        cpos = self.path[1]
        for i, letter in enumerate(self.path[0]): #Gehe den Weg durch
            if self.debug: 
                print(i)
            spos = [cpos[0]*15, cpos[1]*15]
            entrances = ""
            entrances += letter #Ein Ausgang ist durch den Weg gegeben
            if i > 0:
                entrances += OPPOSITE_DIRECTIONS[self.path[0][i-1]] #Alle Räume außer dem ersten besitzen einen Eingang gegenüber dem Nachbarraum
            self.generate_room(entrances, spos[0], spos[1])
            if i == len(self.path[0]) - 1:
                self.end = (spos[0] + 7, spos[1] + 7) #Legt für Metadaten fest, wo das Ziel des Levels liegt
            if letter == "s": #Gehe der Richtung entsprechend nach unten, rechts, oder links
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
            meta = json.dumps({k: self.__dict__[k] for k in self.__dict__ if k != "mp"})
            zf.writestr("/meta.json", meta)

    def load(self, path):
        """Lädt die Karte aus einer Zip-Datei"""
        try:
            with zipfile.ZipFile(path) as zf:
                with zf.open("/map.txt") as mapfile:
                    self.mp = self.convert_string_map(mapfile.read().decode())
                with zf.open("/meta.json") as metafile:
                    contents = metafile.read().decode()
                    for k in json.loads(contents):
                        if k not in self.__dict__.keys():
                            self.__dict__[k] = json.loads(contents)[k]
        except FileNotFoundError as err:
            print(err)
