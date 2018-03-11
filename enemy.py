
dist = lambda p, q: sum(abs(x - y) for x, y in zip(p, q)) #Manhattan-Abstand

class Enemy:
        def __init__(self, x, y, health=10, damage=1, range_=1):
                self.health = health
                self.damage = damage
                self.level = 0
                self.gold = 0
                self.x = x
                self.y = y
                self.range = range_
                
        def move(self, dx, dy):
                self.x += dx #self.x = self.x + dx
                self.y += dy
                
        def attack(self, enemy):
                if dist((self.x, self.y), (enemy.x, enemy.y)) < self.range:
                        enemy.health -= self.damage
                        if enemy.health == 0:
                                enemy.on_killed()
                                self.level += 1
                        
        def on_killed(self):
                return "{0} DIED".format(id(self))
                
        def update(self, args):
                #self.move(args["input"])
                p = args["player"]
                if dist((p.y, p.x), (self.x, self.y)) == 1:
                        self.attack(args["player"])
                        if args["player"].health == 0:
                                args["player"].on_killed()
