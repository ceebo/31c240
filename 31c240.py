import golly as g

class silverfish:
    time = 0
    timeline = []
    columns = []
    b_hep = g.parse("bo$3o$ob2o!", 7, 31)
    absorber = g.parse("2o$2o!", 50, 66)

    def __init__(self):
        self.add_column(0, 0, 3)
        self.add_column(116, 0, 3)
        self.add_column(176, 23, 1)
        self.add_column(232, 23, 1)
        self.add_column(292, 0, 3)
        self.add_column(408, 0, 3)
        
    def add_column(self, x, y, excess):
        self.columns.append((x,y,excess))
        self.left = min(x for x, _, _ in self.columns) - 30
        self.right = max(x for x, _, _ in self.columns) + 31
    
    def advance(self, t):
        self.time += t

    #will add a bheptomino at time t to column c
    def add_event(self, t, c):
        self.timeline.append((self.time+t, c))

    def add_rephaser(self):
        self.add_event(0, 0)
        self.add_event(419, 1)
        self.add_event(494, 2)
        self.add_event(514, 3)
        self.add_event(439, 4)
        self.add_event(20, 5)
    
    def add_forerake(self):
        self.add_event(0, 5)
        self.add_event(879, 4)
        self.add_event(954, 3)
        self.add_event(974, 2)
        self.add_event(899, 1)
        self.add_event(20, 0)
    
    def add_backrake(self):
        self.add_event(0, 0)
        self.add_event(19, 1)
        self.add_event(96, 2)
        self.add_event(116, 3)
        self.add_event(39, 4)
        self.add_event(20, 5)
    
    def construct(self):
        g.new('')
        g.setrule("LifeHistory")
        events = sorted(self.timeline, reverse=True)
        time = -240 * 20
        nextrow = time + 240
        top_y = 0
        for y in range(60):
            g.setcell(self.left, y, 6)
            g.setcell(self.right, y, 6)
        rephasing = [0] * len(self.columns)
        while events:
            if events[-1][0] < nextrow:
                t, c = events.pop()
                g.run(t-time)
                time = t
                x, y, excess = self.columns[c]
                #place bhep, reflecting in the odd columns
                g.putcells(self.b_hep,
                           x + (c%2),
                           rephasing[c] + y,
                           -1 if (c%2) else 1)
                #add blocks to absorb excess gliders
                for i in range(excess):
                    g.putcells(self.absorber,
                               x + (c%2),
                               rephasing[c] + y - 31 * i,
                               -1 if (c%2) else 1)
                    
                rephasing[c] += 31 - 9
            else:
                for x, y, _ in self.columns:
                    g.putcells(g.parse("2o$2o!", x, top_y+y))
                for _ in range(31):
                    top_y -= 1
                    g.setcell(self.left, top_y, 6)
                    g.setcell(self.right, top_y, 6)
                g.run(nextrow-time)
                time = nextrow
                nextrow += 240
                
s = silverfish()

s.add_rephaser()
s.advance(1964)
s.add_forerake()

s.construct()
