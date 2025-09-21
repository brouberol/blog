Title: Solution to Advent of Code "Day 3: Spiral Memory"
Date: 2017-12-31
Category: Programming
Tags: rust

After an unsuccessful attempt at learning Rust earlier this year (I mainly read through the documentation without applying it in any project), I recently started to tackle the [2017 edition of Advent of Code](https://adventofcode.com/2017/), in order to practice Rust for real.

The 3rd challenge, [_Spiral Memory_](https://adventofcode.com/2017/day/3) is interesting because you can [bruteforce](https://gist.github.com/pawlos/0cefa9d753bd6416e6cc9a456ed787f7) it, or solve it with math. I ended up doing the latter, even though math is really not my strong suit.

We're asked to calculate the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry) between a given point and the center, in a spiral reference. The problem amounts to finding the coordinates of any point $P$ in this spiral reference, as once we have the point coordinates, calculating the Manhattan distance is easy:

\begin{align*}
D_P &= |X_P - X_0| + |Y_P - Y_0| \\
    &= |X_P| + |Y_P|
\end{align*}


## Nested shells

My approach was the following: a spiral has nested "shells", all centered around the center. In this image, the first shell is outlined in grey, and the second one in purple. Each of these spirals has a first value, called $S_i$, where $i$ is the index of the spiral.

![spiral](
images/memory-spiral.jpg)

For any point $(X_P, Y_P)$ of value $V$, we know that it is located somewhere on the shell located right before the first shell with start value $S$ such as $S > V$. For example, if the input value was 23, we know that it's located on the second shell as $S_2 ≤ 23 < S_3$.

![spiral](
images/spiral-shells.jpg)

We need to know the number of elements a shell of index $i$ is composed of, noted $Δ_i$ On this representation, the first shell is a square of side of length 3, the second shell is a square of side of length 5. We can generalize this to $L = 2i + 1$, where $i$ is the index of the shell. For any index $i$, the shell is composed of the following number of elements

\begin{align*}
Δ_i &= (2i + 1)^2 - (2(i -1) + 1)^2 \\
    &= 4i^2 + 4i + 1 - 4i^2 +4i - 1 \\
    &= 8i
\end{align*}


## Coordinates of the first element of a shell

Once we know on which shell a given point $P$ is located, we need to know the coordinates of the first point $S_i$ of this shell, so we can infer $P$'s coordinates. This first point will always be located after the center point, and all points composing the previous shells. We can thus infer

\begin{equation*}
V_{S_{{}_i}} = 2 + \sum_{x=1}^{i-1}Δ_i
\end{equation*}

We now need to get the coordinates of any given first shell point. By simply looking at the spiral itself, we can deduce that

\begin{equation*}
(X_{S_{{}_i}}, Y_{S_{{}_i}}) = (n, -n + 1)
\end{equation*}


## Navigating the spiral

The final piece of the puzzle is to infer the coordinates of the point $P$ given the coordinates of the start point $S_i$ of the shell it belongs to. To do that, we need to look at how the coordinates evolve along a shell.

![spiral](
images/shell-coordinates.jpg)

We can see that:

* on the first quarter of the shell, $Y$ coordinates increase by 1 for each increasing value
* on the second quarter of the shell, $X$ coordinates decrease by 1 for each increasing value
* on the third quarter of the shell, $Y$ coordinates decrease by 1 for each increasing value
* on the fourth quarter of the shell, $X$ coordinates increase by 1 for each increasing value

To calculate the coordinates of the point $P$, we just need to locate it on the shell, start from $(X_{S_{{}_i}}, Y_{S_{{}_i}})$ and increase/decrease the $X$ and $Y$ coordinates until we reach the target value.


## The implementation

The strategy is:

* calculate the values of the first shell points until we find a value greater than our target point
* backtrack to the previous shell
* compute the coordinates of the first point of the shell we backtracked to
* increase/decrease the $X$ and $Y$ coordinates until we reach the target value
* calculate the Manhattan distance using these coordinates

```rust
// advent_day03.rs

fn nb_elements_in_outer_level(level: i32) -> i32{
    8 * level
}

fn start_element(level: i32) -> i32 {
    if level == 0 {
        1
    } else {
        let mut out = 0;
        for i in 1..level {
            out += nb_elements_in_outer_level(i);
        }
        out + 2
    }
}

fn first_element_coordinates(level: i32) -> (i32, i32) {
    (level, -level + 1)
}


fn number_coordinates(number: i32) -> (i32, i32) {
    let mut level = 0;
    let mut start: i32;

    // Increase level until we found a starting value greater than
    // input value. When such a value is found, backtrack a step.
    loop {
        start = start_element(level);
        if start >= number {
            level -= 1;
            println!("{:?} is found on level {:?} of the spiral", number, level);
            start = start_element(level);
            break
        } else {
            level += 1;
        }
    }

    // At this point, we've found the starting point of the spiral
    // level we number belongs to.
    let delta = number - start;
    let (mut x, mut y) = first_element_coordinates(level);

    if delta > 2 * level {
        y += 2 * level;
    } else {
        y += delta;
        return (x, y)
    }

    if delta > 4 * level {
        x -= 2 * level;
    } else {
        x -= delta - (2 * level);
        return (x, y)
    }

    if delta > 6 * level {
        y -= 2 * level;
    } else {
        y -= delta - (4 * level);
        return (x, y)
    }

    x += delta - (6 * level);
    (x, y)
}

fn manhattan_distance(x: i32, y: i32) -> i32{
    x.abs() + y.abs()
}

fn main() {
    let number = 312051;
    let (x, y) = number_coordinates(number);
    println!("{:?} has coordinates {:?}", number, (x, y));
    let distance = manhattan_distance(x, y);
    println!("{:?} is at a distance of {:?} from the center", number, distance);
}
```

## The solution

```
312051 is found on level 279 of the spiral
312051 has coordinates (-152, -278)
312051 is at a distance of 430 from the center
```
