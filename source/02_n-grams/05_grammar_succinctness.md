**Prerequisites**

- functions(basics, function growth)

# Succinctness and choosing between grammars

Thanks to all the math we have put to good use, we now have three expressively equivalent models of phonotactics:

1. fixed negative n-gram grammars, and
1. mixed negative n-gram grammars, and
1. fixed positive n-gram grammars.

By "expressively equivalent" we mean that every string language that can be generated by a grammar of one of those tree types can also be generated by grammars of the other two types.
Or in other words, we can freely translate between these three grammar types as we see fit.
But this also means that we cannot distinguish between these three types of grammars based purely on typological data.
There is no empirical phenomenon that allows us to advocate, say, for fixed negative n-gram grammars and against the other two types.
However, we should not conflate expressive equivalence with total equivalence.
These three grammar types can still differ in other respects, and one of them is succinctness: how many n-grams does the grammar need to capture a given phenomenon?

## Differences in grammar size

The three grammar types above vary hugely in how compactly they can model specific phenomena.
You already saw a glimpse of this in earlier exercises, but the true extent only becomes evident once we consider a few artificial examples.

::: example
Suppose our alphabet contains the symbols *a*, *b*, *c*, *d* (and nothing else).
Now consider the language $L$ that contains *ab*, *aab*, *aaab*, and so on (more succinctly, we can write $L$ as *a~+~b*).
This is very easy to express as a positive grammar:

1. {{{L}}}a
1. aa
1. ab
1. b{{{R}}}

The smallest mixed negative grammar for this language isn't much bigger:

1. c
1. d
1. {{{L}}}{{{R}}}
1. {{{L}}}b
1. ba
1. bb
1. a{{{R}}}

And the fixed negative grammar is huge by comparison:

1. {{{L}}}{{{R}}}
1. {{{L}}}b
1. {{{L}}}c
1. {{{L}}}d
1. ac
1. ad
1. ba
1. bb
1. bc
1. bd
1. a{{{R}}}
1. b{{{R}}}
1. c{{{R}}}
:::

::: example
Suppose that our alphabet still contains only *a*, *b*, *c*, *d*, but $L$ now follows a more general pattern: 1 or more instances of *a*, followed by exactly one instance of *b* or *c* or *d*.
Hence $L$ contains *ab*, *ac*, *ad*, *aab*, *aac*, *aad*, *aaab*, *aaac*, *aaad*, and so on.

The positive grammar is still fairly small.

1. {{{L}}}a
1. aa
1. ab
1. ac
1. ad
1. b{{{R}}}
1. c{{{R}}}
1. d{{{R}}}

The mixed negative grammar, by comparison, grows a lot in size: 

1. {{{L}}}{{{R}}}
1. {{{L}}}b
1. {{{L}}}c
1. {{{L}}}d
1. ba
1. bb
1. bc
1. bd
1. ca
1. cb
1. cc
1. cd
1. da
1. db
1. dc
1. dd
1. a{{{R}}}

In fact, this also happens to be the fixed negative grammar.
For $L$, allowing n-grams of variable length does not help at all.
:::

::: example
Now suppose our alphabet is $\setof{a}$ and consider the language $L$ that contains all strings over *a* whose length is at least 2 (i.e. *aa*, *aaa*, and so on).
The mixed negative grammar is incredibly small:

1. {{{L}}}{{{R}}}
1. {{{L}}}a{{{R}}}

The fixed negative grammar looks slightly different, but has the same size.

1. {{{L}}}{{{L}}}{{{R}}}
1. {{{L}}}a{{{R}}}

This time the positive grammar is the largest:

1. {{{L}}}{{{L}}}a
1. {{{L}}}aa
1. aaa
1. aa{{{R}}}
1. a{{{R}}}{{{R}}}
:::

::: example
Finally, assume that the alphabet $\Sigma$ is $\setof{a,b,c,d,e,f}$ and that $L$ contains all strings over this alphabet except that no string may have 5 or more instances of *a* in a row.
For instance, *baaaab* and *caaadaaaf* are well-formed, but not *baaaaab* or *ffaaaaaaacabec*.
The negative grammar for this is maximally simple:

1. aaaaa

The positive grammar, on the other hand, is enormous.
It contains all n-grams in $\Sigma_E^5$ except *aaaaa*.
That's $32,767$ n-grams: since there are 6 symbols in $\Sigma$ and 2 edge markers, $\Sigma_E^5$ contains $8^5 = 32,768$ 5-grams.
:::

Overall, there doesn't seem to be much regularity.
Sometimes a positive grammar is smaller, sometimes a negative grammar one, and sometimes it matters whether the negative grammar is mixed or fixed while in other cases the two look exactly the same.
Sometimes the differences is only one or two n-grams, sometimes it's tens of thousands.
So is this a case of anything goes where one can never be quite sure how things will pan out?
No, quite to the contrary.

## Upper bounds and rates of growth

Even though it is difficult to tell how things may pan out for a specific phenomenon or string language, that does not mean that there are no regularities.
It's just that these regularities are a bit more abstract in nature as they take the form of **upper bounds**.
Since every fixed-length grammar, whether positive or negative, is built from members of $\Sigma_E^n$ for some alphabet $\Sigma$ and some choice of $n$, its size cannot exceed that of $\Sigma_E^n$.
And that size is easy to calculate.
Each $n$-gram furnishes $n$ positions, each one of which must be a symbol from $\Sigma$ or one of the two edge markers.
So if $\Sigma$ contains $m$ symbols, there are $m+2$ choices for each position, and since there are $n$ positions, this means there are $(m+2)^n$ different combinations.
Hence the size of $\Sigma_E^n$ is $(m+2)^n$, and that's a fixed upper bound on the size of any $n$-gram grammar over $\Sigma$.

::: example
Suppose $\Sigma \is \setof{a,b}$.
Then $\Sigma_E^2$ has $(2+2)^2 = 4^2 = 16$ members.
We can list them all:

1. {{{L}}}{{{L}}}
1. {{{L}}}{{{R}}}
1. {{{L}}}a
1. {{{L}}}b
1. a{{{L}}}
1. a{{{R}}}
1. aa
1. ab
1. b{{{L}}}
1. b{{{R}}}
1. ba
1. bb
1. {{{R}}}{{{L}}}
1. {{{R}}}{{{R}}}
1. {{{R}}}a
1. {{{R}}}b
:::

::: exercise
For $n \geq 2$, no grammar ever needs to contain every member of $\Sigma_E^n$.
Explain why.
:::

This insight provides us with a fixed upper bound for any given choice of $\Sigma$ and $n$ such that no grammar can be bigger than that.
But that by itself isn't really that interesting, we want to know how that upper bound changes as we vary $\Sigma$ and $n$.
We can make this more visual by drawing a table, where rows indicate the size of the alphabet (plus both edge markers) and columns indicate the length of the $n$-grams.

|       | 1    | 2         | 3           | 4             | 5              |
| --:   | --:  | --:       | --:         | --:           | --:            |
| 3     | 3    | 9         | 27          | 81            | 243            |
| 4     | 4    | 16        | 64          | 256           | 1024           |
| 5     | 5    | 25        | 125         | 625           | 3125           |
| 6     | 6    | 36        | 216         | 1296          | 7776           |
| 7     | 7    | 49        | 343         | 2401          | 16807          |
| 8     | 8    | 64        | 512         | 4096          | 32768          |
| 9     | 9    | 81        | 729         | 6561          | 59049          |
| 10    | 10   | 100       | 1,000       | 10,0000       | 100,000        |
| 100   | 100  | 10,000    | 1,000,000   | 100,000,000   | 10,000,000,000 |

As you can see, the numbers grow quite a bit from the top to the bottom, but much faster from left to right.
In other words, $n$ plays a much bigger role in determining the size $\Sigma_E^n$.
The number of bigrams over an alphabet with 100 symbols (including edge markers) is still smaller than the number of 5-grams over an alphabet with 7 symbols.
Our upper bound grows **exponentially** with $n$, but only **polynomially** with $\Sigma$.

What does this tell us?
While we can freely choose between fixed negative grammars, mixed negative grammars, and positive grammars because they are interchangeable, grammar size can vary a lot depending on the phenomenon.
This does not matter too much as long as $\Sigma$ and $n$ are both small, but as we increase the size of the alphabet and the length of the $n$-grams, it becomes more noticeable.
In fact, we do not even need to worry too much about $\Sigma$ as $n$ has a much bigger impact on this.
Even with very small alphabets, $\Sigma_E^n$ is giant for $n > 5$.

::: example
For an alphabet with just two symbols, $\Sigma_E^6$ is 4,096, and $\Sigma_E^10$ is 1,048,576.
That's more than the number of trigrams over an alphabet with close to 100 symbols.
:::

## Recap

- Depending on the phenomenon at hand, a positive or a negative grammar may be more succinct.
- The difference in grammar size may not always be very pronounced, but it can be.
- The difference cannot exceed the size of $\Sigma_E^n$, which grows polynomially with $\Sigma$ and exponentially with $n$.