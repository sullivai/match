
def printMatches(matched):
    print("\nMATCHED")
    for item in sorted(matched.keys()):
        print(item+": "+matched[item])



def printQuotas(quota):
    print("\nVACANCIES")
    for item in quota:
        print(item+": "+str(quota[item]))

