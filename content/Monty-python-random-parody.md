Title: How to randomly generate a Monty Python parody
Date: 2011-11-16
Category: Programming
Tags: Python

If you always wanted to write texts in the way of Monty Python, I have what you need !
In this post, I am going to show you mathematical techniques to analyse a text, in order to randomly generate look-alike texts.

## Introduction to basic concepts

First essential question: what is a text?

From a mathematical point of view, a text of length _n_ simply is the concatenation of _n_ symbols, all taken from a finite alphabet _A_.
In our context, the alphabet is generally composed of all lowercase and uppercase letters, punctuation signs, etc.

In a real-life situation, **the symbols sucession is not random, but depends of the previous symbols**. Indeed, if the 3 last symbols are _" "_, _"t"_ and _"h"_, it is highly probable that the next one will be _"e"_, because the world _"the"_ is fairly common.

The whole problem can thus be resumed to obtaining a transition probability matrix between strings of fixed length and all smbols of the alphabet.

*Example* : Let's assume that the three last symbols are _" "_, _"t"_, and _"h"_, and that the probability of the next symbol being _"e"_ (written $p("e" / " th")$ ) is 0.6, an _"a"_ is 0.3 and _"u"_ is 0.1.
We would then obtain a line of the matrix of transition probability between _" th"_ and all alphabet symbols:

_" th"_ —> a: 0.3, b: 0, c: 0, ..., e: 0.6, ..., u: 0.1, ...

The probability $p("e" / " th")$ is called a conditional probability.

## Markov chain of order $k$

We are going to model our data text (here, the "Monthy Python and the Holy Grail" script) with a Markov chain of order $k$. This barbarian name refers to :

> "a mathematical system that undergoes transitions from one state to another (from a finite or countable number of possible states) in a chain-like manner
   --
   [Source : Wikipedia](http://en.wikipedia.org/wiki/Markov_chain "Wikipedia")"

That means that the following state is conditioned by the $k$ previous ones.

If we deal with a Markov chain of order 3, the probability of occurence of the next symbol will only depends on the 3 previous symbols. From previous tests, I can say that **$k=10$ is a good place to start**. (More on that later)

## Text Alphabet

We've just fixed the value of k, which was the first step of the process. Now, we need to to create a list of all encountered symbols (ie: the alphabet).

First, we read the data file, and join all the lines in a single string.

```python
f = open('../data/monty.txt')
f_lines = ' '.join(f.readlines())
```


Then, we create the alphabet list:

```python
def alphabet(datafile_lines):
    """
    Returns all used characters in a given text
    """
    alph = []
    for letter in datafile_lines:
        if letter not in alph:
            alph.append(letter)
    return sorted(alph)
```

## Finding all exiting K-tuples in the source text

Now, **we need to identify all distinct strings of length $k=10$ in the text**.

This can seem a bit tedious, but list comprehensions and sets will do a lovely work.

```python
# -- split text in ak chunks of length k
ak_chunks = [datafile_lines[i:i+k] for i in xrange(len(datafile_lines))]

# -- remove final chunk if not of size k
if len(ak_chunks[-1]) != k:
    ak_chunks.remove(ak_chunks[-1])

# -- Extract unique values from list
ak_chunks = list(set(ak_chunks)) #set: reduce to unique values
```

## Empirical probabilities of transition

Now comes the hard work. So far, we have

 * a text,
 * its alphabet,
 * a HUGE list of all distincts strings of length $k=10$ contained in the text

What we then need is a way to calculate the empirical probability of transition between each string of length 10 and symbols of the alphabet ("empirical" in the way that these probabilities will only apply to the text we study).

Let's formalize a bit the problem:

  * $a^k$ : string of length $k$ (here, 10)
  * $b$ : symbol located after $a^k$
  * $n_(a^k)$ : number of times that the string $a^k$ is encountered in the text
  * $n_(b/a^k)$ = number of times that the string $a^k$ is followed by the symbol $b$

We can now express the empirical probability $p(b/a^k) = n\_(b/a^k) / n\_(a^k)$
(number of times that the string $a^k$ is followed by the symbol $b$ / number of times that the string $a^k$ is encountered in the text)

*Example* : if our text is ABCABDABC, $a^k = AB$ and $b = C$:

* $n\_(AB) = 3$
* $n\_(C/AB) = 2$
* $p(C/AB) = 2/3 = 0.667$

Let's write all that in Python:

```python
def conditional_empirical_proba(chain, ak, symbol, n_ak): # p(b/a^k)
    """
    Returns the proportion of symbols after the ak string (contained
    in chain string and of length k) which are equal to the value
    of given parameter 'symbol'
    Ex:conditional_empirical_proba('ABCABD', 2, 'AB', 'C', n_ak)-> 0.5
    """
    nb_ak = n_b_ak(chain, ak, symbol)
    if n_ak != 0:
        return float(nb_ak)/n_ak
    else:
        return 0

def n_b_ak(chain, ak, symbol): # n_(b/a^k)
    """
    Given a string chain, returns the number of
    times that a given symbol is found
    right after a string ak inside the chain
    """
    return chain.count(ak+symbol)

def n_ak(chain, ak): # n_(a^k)
    """
    Given a string chain and a string ak, returns
    the number of times ak is found in chain
    """
    return chain.count(ak)
```

Now, the only remaning thing to do is to calculate the empirical conditional probability for each k-tuple and for each symbol.

A few remarks are necessary:

  * We will only store empirical conditional probabilities > 0 (more on that later)
  * We will store accumulative empirical conditional probabilities (more on that later)
  * The matrix will be created with a dictionnary of dictionnaries


```python
# Initialization of matrix
prob = {}
for ak in ak_chunks:
    # New matrix line
    prob[ak] = {}

    # -- calculate p(b/a^k) for each symbol of alphabet
    pbak_cumul = 0
    for symb in alpha:
        pbak = conditional_empirical_proba(datafile_lines, ak, symb, nak)

        # cumulative probabilities
        pbak_cumul += pbak

        # if sucession ak+symb is encountered in text, add probability to matrix
        if pbak != 0.0: # Very important, if pbak = 0.0, the combination ak+symb will not be randomly generated
            prob[ak][symb] = pbak_cumul

with open('../results/distribs/distrib_k%d.txt' % (k), 'w') as proba_file
    pickle.dump(prob, proba_file)
```

## Random text generation

Close your eyes for a second, and think about what we just did. **We calculated empirical transition probabilities between all existing strings of length 10 and all symbols of the alphabet, and stored the non nil acumulative probabilities in a matrix**. (The non-nil part has two main advatages : it implies less storage cost, and we only store combinations that occured in the text. This way, random generation becomes really easy !)

It is now extremely easy to generate a text using these accumulative probabilities! Let's consider a quick example.

*Example* : $a^k = AB$, $p(A/AB)=0.2$, $p(B/AB)=0.5$, $p(C/AB)=0.5$. We then store these acumulative values in the matrix:

  * $p(A/AB)=0.2$
  * $p(B/AB)=0.7$
  * $p(C/AB)=1$

That way, we only have to pick a random float between 0 and 1 using a uniform distribution to match this float with a symbol. `random(0,1) = 0.678 --> symbol = B`

For this technique to work, the first $k=10$ symbols of the generated text must directly come from the original text (and hence will be contained in the matrix). This will give us a valid initial condition.

Let's now generate the text :

```python
def random_text(size, k):
    """
    Given a result size and an integer k,
    returns a randomly generated text using
    probability distributions of markov chains
    of order k dumped in ../results/distribs/distrib_kX.txt
    files
    """
    # -- Initial string
    with open('../data/monty.txt','r') as f
        initial_string = ' '.join(f.readlines())[:k]
        out = initial_string

    # -- Import probability distribution
    try:
        p = open('../results/distribs/distrib_k%d.txt'%(k),'r')
    except IOError as err:
        print err
        exit(2)

    distrib_matrix = pickle.load(p)
    p.close()

    # -- Generate text following probability distribution
    kuple = initial_string
    for x in xrange(size):
        p = random.uniform(0,1)
        i = 0
        char = ''

        # read distribution specific to k-tuple string
        dist = distrib_matrix[kuple]

        for symbol in dist:
            char = symbol
            i = dist[symbol]
            if i > p:
                break

        out += symbol
        kuple = kuple[1:]+symbol # update k-tuple

    return out

```

 Done ! Now, you only have to call the function `random_text(len_text, 10)` and BOOM !

## Example of generated text with $k = 10$

```
"KING ARTHUR: Will you ask your master that we have been charged by God with a sacred quest. If he will give us food and shelter for the week.
ARTHUR: Will you ask your master if he wants to join my court at Camelot?!
SOLDIER #1: You're using coconuts!
ARTHUR: Ohh.
BEDEVERE: Uh, but you are wounded!
GALAHAD: What are you doing in England?
FRENCH GUARDS: [whispering] Forgive me that' and 'I'm not worth"
```

## What if we change $k$ ?

k can be interpreted as the quantity of context you take into account to calculate a symbol occurence probability. We chose $k = 10$, because a context of 10 symbols allows the program to generate a text with apparent sense (limited by the randomness of the process, and by the fact that THIS IS MONTY FREAKING PYTHON).

The more context you add, the more alike the generated and original texts will be, up to a point where they will be identical.

If you decrease k, you can find a interesting case where you generate words, but where the context is senseless.

Example, for $k=5$:

```
"KING ARTHUR: Yes!
VILLAGER #3: A bit.
VILLAGER #1: You saw saw saw it, did you could
separate, and master that!
ARTHUR: Will you on Thursday.
CUSTOMER: What do you can you think kill your every
good people. It's one.)
OTHER FRENCH GUARDS: [whispering]"
```

If you decrease $k$ even more, you will only generate rubbish.

## Conclusion

We have seen a pretty simple text analysis technique which allows us to randomly generate a text, based on statistical analysis of the data text. This technique is based on the fact that the probability of occurence of a letter depends on its local "past".

Playing with the value of the "past length", you can generate text more or less alike to the original, and with more or less "sense".

This simple technique does not use the nltk python module, or a set of texts to generate "theoretical" rules on a language. Its is purely empirical.

All source code available on [GitHub](https://github.com/brouberol/Generate-Monty-Pyhon-Dialog "GitHub repository").

**EDIT** : A nice comment from reddit:

> "This approach was first proposed by Claude Shannon in his landmark paper "A Mathematical Theory of Communication"… in 1948.
   Gotta love how people keep reinventing the same things over and over again. But this time, in Python!"
