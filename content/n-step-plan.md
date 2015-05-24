Title: My n-step plan to become a better programmer
Date: 2015-05-24
Category: Programming

One of the main selling points of Python are its multi-paradigm philosophy. You can code in imperative, object-oriented or aspect-oriented style, use meta-programming techniques, etc. It also has an immense amount of libraries available. Finally, it's both a simple language to pick up for beginners, and a powerful language for more experienced programmers.

I've been programming for the last six or seven years, and I feel that my main strength is also my main weakness: I've been mainly coding in Python since the beginning. It means that I can now use Python's features and standard library pretty well, but it also means that I tend to think of every problem in terms of Python features and libraries (standard or not).

A proverb programmers are taught quite early is

> If all you have is a hammer, everything looks like a nail.
  ([Source](https://en.wiktionary.org/wiki/if_all_you_have_is_a_hammer,_everything_looks_like_a_nail))

It means that if you're only comfortable with a single tool, then you'll try to use it in every situation, even in one where it's not appropriate. I strongly feel that to become a better programmer, I now need to learn other programming languages and even other paradigms. I was initially thinking of functional languages, like [Haskell](https://www.haskell.org/) or [oCaml](http://ocaml.org/), but then I remembered something [Fredrik](http://blaag.haard.se/) told me a while ago, at a EuroPython after-party: reading "Structure and Interpretation of Computer Programs" immediately made him a better programmer. I remember being curious as to why.

It so happens that the books is written under a Creative Common license, and can be downloaded [here](https://github.com/ieure/sicp/downloads), AND uses [Scheme](https://en.wikipedia.org/wiki/Scheme_%28programming_language%29) as a teaching language. It thus combines three things I strive for: a new language, a new programming paradigm and more insight into the art of programming itself.

I'm thus laying out my n-step plan to become a better programmer:

1. Read the book thoroughly
2. Solve the exercises
3. Stop conceiving every solution in Python

Behold, one of my first Scheme programs, a pavement in the road of my improvement.

    :::scheme
    ; Implementation of cubic root Newton approximation technique in Scheme

    (define (square x) (* x x))

    (define (cubic-root x)
        (define (improve guess)
            (/ (+ (/ x (square guess)) (* guess 2)) 3))

        (define (good-enough? new-guess old-guess)
            (< (abs (/ (- new-guess old-guess) old-guess)) 0.001))

        (define (try new-guess old-guess)
            (if (good-enough? new-guess old-guess)
                new-guess
                (try (improve new-guess) new-guess)))

        (try 1.0 x)
    )

    (cubic-root 9)
