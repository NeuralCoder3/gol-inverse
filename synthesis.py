from z3 import *
import time
import sys

# width and height of the grid
w,h = 11,11
# how many iterations to simulate
steps = 2


# kind = "mirror"
# kind = "flip"
kind = "glider"
ox,oy=0,1
# kind = "inverse"
# org_grid = """
# ......
# ..###.
# ..###.
# ..###.
# ..###.
# ..###.
# ......
# """.strip().split('\n')
# org_grid = [[1 if c == '#' else 0 for c in row] for row in org_grid]

def evolve(grid):
    h = len(grid)
    w = len(grid[0])
    sum_grid = []
    for y in range(h):
        sum_row = []
        for x in range(w):
            summed = 0
            for yo in [-1,0,1]:
                for xo in [-1,0,1]:
                    if xo == 0 and yo == 0:
                        continue
                    if 0 <= y+yo < h and 0 <= x+xo < w:
                        summed += grid[y+yo][x+xo]
            sum_row.append(summed)
        sum_grid.append(sum_row)
    out_grid = []
    for y in range(h):
        out_row = []
        for x in range(w):
            if sum_grid[y][x] == 3:
                out_row.append(1)
            elif sum_grid[y][x] == 2:
                out_row.append(grid[y][x])
            else:
                out_row.append(0)
        out_grid.append(out_row)
    return out_grid
    

s = Solver()

def step(grid, prefix):
    h = len(grid)
    w = len(grid[0])
    sum_vars = [[Int(f'{prefix}_sum_{x}_{y}') for x in range(w)] for y in range(h)]
    out_vars = [[Int(f'{prefix}_grid_{x}_{y}') for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            summed = 0
            for yo in [-1,0,1]:
                for xo in [-1,0,1]:
                    if xo == 0 and yo == 0:
                        continue
                    if 0 <= y+yo < h and 0 <= x+xo < w:
                        summed += grid[y+yo][x+xo]
            s.add(sum_vars[y][x] == summed)
    # evolve state
    # 3 -> create cell
    # 2 -> keep cell
    # _ -> kill cell
    for y in range(h):
        for x in range(w):
            s.add(out_vars[y][x] == If(sum_vars[y][x] == 3, 1, If(sum_vars[y][x] == 2, grid[y][x], 0)))
    return out_vars

in_vars  = [[Int(f'in_{x}_{y}') for x in range(w)] for y in range(h)]

# only 0 or 1
for y in range(h):
    for x in range(w):
        s.add(Or(in_vars[y][x] == 0, in_vars[y][x] == 1))
        
# border around the grid
for y in range(h):
    s.add(in_vars[y][0] == 0)
    s.add(in_vars[y][w-1] == 0)
for x in range(w):
    s.add(in_vars[0][x] == 0)
    s.add(in_vars[h-1][x] == 0)

# non-empty grid
insum = 0
for y in range(h):
    for x in range(w):
        insum += in_vars[y][x]
s.add(insum > 0)
        
# simulate steps
grid = in_vars
grids = []
for i in range(steps):
    grid = step(grid, f'step_{i}')
    grids.append(grid)
    
    
    
    
# grid is the same as in_vars but mirrored
if kind == "mirror" or kind == "flip":
    for y in range(h):
        for x in range(w):
            s.add(grid[y][x] == in_vars[y][w-1-x])
        
    if kind == "mirror":
        diff = []
        for y in range(h):
            for x in range(w):
                diff.append(grid[y][x] != in_vars[y][x])
        # out is not in => not symmetric 
        # could also be formulated on one of them individually
        s.add(Or(diff))

    # right side empty in in_vars
    if kind == "flip":
        for y in range(h):
            for x in range((w+1)//2, w):
                s.add(in_vars[y][x] == 0)


elif kind == "glider":
    for y in range(h):
        for x in range(w):
            oldx = x-ox
            oldy = y-oy
            if 0 <= oldx < w and 0 <= oldy < h:
                s.add(grid[y][x] == in_vars[oldy][oldx])
            else:
                s.add(grid[y][x] == 0)
                
    for y in range(h):
        for x in range(w):
            nx,ny = x+ox,y+oy
            if 0 <= nx < w and 0 <= ny < h:
                continue
            # out of bounds => empty
            s.add(in_vars[y][x] == 0)
            
            
elif kind == "inverse":
    # assert out_vars to coincide with grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            s.add(org_grid[y][x] == grid[y][x])

else:
    raise ValueError(f"Unknown kind {kind}")
        

result = s.check()
if result == sat:
    m = s.model()
    for y in range(h):
        print(''.join('#' if m[in_vars[y][x]].as_long() else '.' for x in range(w)))
    print()
    
    for i, grid in enumerate(grids):
        print(f'Step {i+1}')
        for y in range(h):
            print(''.join('#' if m[grid[y][x]].as_long() else '.' for x in range(w)))
        print()
        
    sol = [[m[in_vars[y][x]].as_long() for x in range(w)] for y in range(h)]
        
    # export in_vars as image
    from PIL import Image
    img = Image.new('RGB', (w,h), color = 'white')
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            iv = sol[y][x]
            pixels[x,y] = (255,255,0) if iv == 1 else (0,0,0)
    img.save(f'gol_${kind}_{w}x{h}_s{steps}.png')
    
    # to find all solutions:
    # s.add(Or([in_vars[y][x] != sol[y][x] for y in range(h) for x in range(w)]))
else:
    print("No solution found")
    print(result)
    sys.exit(1)
