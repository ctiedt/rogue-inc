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

    def gen_path(self):
        m = [[0 for x in range(3)] for y in range(3)]
        start, stop = random.sample(m, 2)
        path = []
        if self.debug:
            print(str(start)+", "+str(stop))
        mdists = [[dist_manhattan((x, y), stop) for y in range(3)] for x in range(3)]
        cpos = start
        while cpos != stop:
            neighbours = []
            if cpos[0] > 0:
                neighbours.append((cpos[0] - 1, cpos[1]))
            if cpos[0] < 2:
                neighbours.append((cpos[0] + 1, cpos[1]))
            if cpos[1] > 0:
                neighbours.append((cpos[0], cpos[1] - 1))
            if cpos[1] < 2:
                neighbours.append((cpos[0], cpos[1] + 1))
            dists = [mdists[n[0]][n[1]] for n in neighbours]
            if self.debug:
                print(neighbours)
                print(dists)
            nextn = neighbours[dists.index(min(dists))]
            if nextn[0] - cpos[0] > 0:
                m[cpos[0]][cpos[1]] = "e"
            if nextn[0] - cpos[0] < 0:
                m[cpos[0]][cpos[1]] = "w"
            if nextn[1] - cpos[1] > 0:
                m[cpos[0]][cpos[1]] = "m"
            if nextn[1] - cpos[1] < 0:
                m[cpos[0]][cpos[1]] = "s"
            cpos = nextn
        return m

    def map_as_string(self): #2D-Array in String mit Zeilenenden umwandeln
        return "\n".join(["".join(str(e) for e in row) for row in self.mp])

    def convert_string_map(self, text): #String in 2D-Array umwandeln
        return [[int(text[x + y]) for y in range(48) if text[x + y] != "\n"] for x in range(48)]

    def save(self, path): #Karte in der Datei Path speichern
        """Loads the map from a zip file"""
        #TODO: Abfrage, ob Datei schon existiert
        #TODO: Überprüfen, ob Archiv nötige Dateien enthält
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("/map.txt", self.map_as_string())

    def load(self, path): #Karte aus der Datei path laden
        with zipfile.ZipFile(path) as zf:
            with zf.open("/map.txt") as mapfile:
                self.mp = self.convert_string_map(mapfile.read().decode())
