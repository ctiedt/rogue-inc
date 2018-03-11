#_d Charakterklasse für Rgoue Inc.
#_d Jonas Tresper
#2. Sprint

dist = lambda p, q: sum(abs(x - y) for x, y in zip(p, q)) #Manhattan-Abstand

class Character:
        def __init__(self, x, y, name, health=10, damage=1, range_=1):
                self.health = health
                self.damage = damage
                self.name = name
                self.level = 0
                self.gold = 0
                self.x = x
                self.y = y
                self.range = range_
                
        def move(self, dx, dy, map_):
                if map_[self.y + dy][self.x + dx] != 1:
                    self.x += dx
                    self.y += dy
                
        def attack(self, enemy):
                if dist((self.x, self.y), (enemy.x, enemy.y)) < self.range:
                        enemy.health -= self.damage
                        if enemy.health == 0:
                                enemy.on_killed()
                                self.level += 1
                        
        def on_killed(self):
                return "YOU DIED"
                
        def update(self, args):
                self.damage = self.level + 1
                self.move(*[int(i) for i in args["input"]], args["map"])
                if "atk" in args:
                        for en in args["atk"]:
                                self.attack(en)
