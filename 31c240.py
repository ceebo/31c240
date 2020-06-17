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

    def add_row(self, ts, offset=0):
        for i, t in enumerate(ts):
            self.add_event(offset+t, i)

    def add_standard_row(self, delta, offset=0):
        self.add_row([0, 656-delta, 731-delta, 751-delta, 676-delta, 20], offset)

    def add_forerake(self, offset=0):
        self.add_row([20, 899, 974, 954, 879, 0], offset)
    
    def add_backrake(self, offset=0):
        self.add_row([0, 19, 96, 116, 39, 20], offset)

    def add_rephaser(self, offset=0):
        self.add_standard_row(237, offset)

    def add_R4L8F(self):
        # first backrake
        self.add_backrake()
        # second backrake
        self.add_backrake(1532)
        # R2L23F:
        # block puffer
        self.add_standard_row(10, 2774)
        # teardrop puffer
        self.add_standard_row(-7, 4558)

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
                    g.putcells(g.parse("2o$2o!", x, 2*top_y+y))
                    g.putcells(g.parse("2o$2o!", x, 2*top_y-31+y))
                for _ in range(31):
                    top_y -= 1
                    g.setcell(self.left, top_y, 6)
                    g.setcell(self.right, top_y, 6)
                g.run(nextrow-time)
                time = nextrow
                nextrow += 240
                
s = silverfish()

# sample bi-block puffer
# s.add_backrake()
# s.advance(2048)
# s.add_forerake()
# s.advance(3000)
s.add_R4L8F()

s.construct()
