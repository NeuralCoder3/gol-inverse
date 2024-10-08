# Game of Life Synthesis

Game of Life (GoL) is a [2d cellular automaton](https://en.wikipedia.org/wiki/Cellular_automaton).
If two Moore neighbours (out of all eight) are alive, the cell becomes alive.
If three are alive, the cell stays in its state.
Otherwise, it dies.
- 2: _ -> 1
- 3: x -> x
- _: _ -> 0

GoL is proven to be turing-complete.
Some interesting behaviors are for instance gliders that move along the grid.

Here, we model the propagation rules in SMT to allow inversing them / finding pattern with interesting properties.

We look at three kinds of patterns:

## Inverse

When inversing, we are looking for a pattern that produces a desired output.
There are usually many such patterns.

Sometimes, the inversion ends in a [garden of eden](https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton)). A structure that can never be reached by any other state.


## Glider

A glider is a structure that produces itself at a different position (the same position would be an oscillator/stationary life).

We experimented with common gliders:
A minimal in a 5x5 grid with period 4 to move 1 in both directions:
```
##.
..#
###
```

The next [larger glider](https://conwaylife.com/wiki/C/2_orthogonal) moves orthogonally 2 cells to the right with a period of 4 (it flips in 2 moves moving 2 cells).
In that, it is a C/2 (half the speed of light) period 4 glider.
```
.####
#...#
....#
#..#.
```

Lastly, we synthesized a real c/2 glider of near minimal size.
This glider moves 1 cell in 2 steps.
It looks like a spaceship and is quite close to the [64P2H1V0](https://conwaylife.com/wiki/64P2H1V0) structure.
We used a 35x15 grid for the synthesis. Interestingly, the structure is not symmetric.
```
...............##....
##...#..#..##..#...##
....#....#..###.#....
#...#.##.#.#.##.#...#
.##.#....#.#....#.##.
..#.#.#..#.#..#.#.#..
...##.#.##.##.#.##...
....#.#.......#.#....
.......#.....#.......
.....#.........#.....
.....#...#.#...#.....
......#..#.#..#......
.......###.###.......
```


## Mirror

Mirrors are structures that 
- produce their mirrored result
- are not symmetric

We showcase a few discoveries:
11x11 period 2
```
...###...
.#..###..
#....#..#
####..###
.....#...
##.#.#.##
#.##.##.#
```

9x9 period 3
```
.##.##.
#.##..#
##....#
.#...#.
#....##
#..##.#
.##.##.
```


## Flip

A flipper is like a mirror but instead of just mirroring it, it moves to the side.
I.d. the structure moves into its mirrored image.
It flips onto the side.
Therefore, the right side is free at the start and contains the mirrored structure at the end.

We postulate that such a structure does not exists.
So far, we tested odd symmetry axis with grids up to 11x11 and steps up to 7.


## Other

There are further possibly interesting aspects:
- Explosions: Minimal structures that produce a lot of alive cells
- Breeders: Glider producers

For more, see [LifeWiki](https://conwaylife.com/wiki/Main_Page)