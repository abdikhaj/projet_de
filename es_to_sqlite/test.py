import itertools
a = [(1, "aaaaaa"), (1, "bbbbbb"), (2, "ccccc"), (2, "ddddd")]

n = []
for l in [list(g) for k, g in itertools.groupby(a, lambda x: x[0])]:
    z = ""
    for t in l:
        z += t[1] + '. '
    n.append((t[0], z))
print(n)