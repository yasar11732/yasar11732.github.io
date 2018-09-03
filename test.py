
def recur(j, i):
    j1 = ((5 * j) + 1) % i
    while j1 != j:
        print j1
        j1 = ((5 * j1) + 1) % i