#Project: Rogue Inc.
#Class: Map Generator
#Sprint I
#Clemens Tiedt

import random, zipfile

#Verschiedene allgemeine Utensilien

dist_manhattan = lambda x, y: sum(abs(p - q) for p, q in zip(x, y))
dist_euclidean = lambda x, y: (sum((p - q)**2 for p, q in zip(x, y)))**0.5

class MapGenerator:

    def __init__(self, debug=False):
        self.debug=debug
        self.mp = [[0 for y in range(48)] for x in range(48)] #Erstelle einen 2D-Array 48x48 aus Nullen; die Karte hat *immer* die Größe 48x48
        self.path = self.gen_path()
        self.name = self.generate_name()

    def generate_name(self):
        """Generiert einen Bezeichner für die Map"""
        type_ = random.choice(("Dungeon", "Lair", "Caves", "Labyrinth"))
        syllables = ["An", "Ab", "Ar", "Ur", "Un", "Kan", "Lor", "Wun", "Wil", "Har", "Hor", "Ko", "Luz", "Laz", "Ban"]
        owner = random.choice(syllables) + random.choice(("", "-")) + random.choice(syllables).lower()
        title = random.choice(("Abominable", "Cruel", "Cunning", "Crazy", "Reasonable", "Traitor"))
        return "{} of {} the {}".format(type_, owner, title)

    def gen_path(self):
        """Generiert einen Weg durch die Map auf einem 3x3-Gitter"""
        cpos = [random.randint(0, 2), 0]
        start = cpos.copy()
        path = ""
        while cpos[1] < 3: #Generator "bewegt" sich, bis er den y-Wert 3 erreicht nach unten 
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
        return path[:-1], start #Da der letzte Schritt im Pfad einen Schritt zu weit nach unten geht, wird er entfernt.

    def map_as_string(self): #2D-Array in String mit Zeilenenden umwandeln
        return "\n".join(["".join(str(e) for e in row) for row in self.mp])

    def convert_string_map(self, text): #String in 2D-Array umwandeln
        return [[int(text[x + y]) for y in range(48) if text[x + y] != "\n"] for x in range(48)]

    def save(self, path): #Karte in der Datei Path speichern
        """Save the map to a zip file"""
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("/map.txt", self.map_as_string())

    def load(self, path): #Karte aus der Datei path laden
        """Loads the map from a zip file"""
        #TODO: Abfrage, ob Datei schon existiert
        #TODO: Überprüfen, ob Archiv nötige Dateien enthält
        with zipfile.ZipFile(path) as zf:
            with zf.open("/map.txt") as mapfile:
                self.mp = self.convert_string_map(mapfile.read().decode())
