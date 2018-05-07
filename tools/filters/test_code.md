Some python code, I always wanted to share

```
def fun(arg):
    #some bug is about to happen
    <mark>answer = 41</mark>
    #but we ignore it
    return 42
```

``` {.python}
def bar(arg):
    #no bug
    return 42
```

the default example for `fenced_code_blocks`

~~~~~~~
if (a > 3) {
  moveShip(5 * gravity, DOWN);
}
~~~~~~~

the default example for `fenced_code_attributes`

~~~~ {#mycode .haskell .numberLines startFrom="100"}
qsort []     = []
qsort (x:xs) = qsort (filter (< x) xs) ++ [x] ++
               qsort (filter (>= x) xs)
~~~~
