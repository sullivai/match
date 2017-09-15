import csv

def getLingPref(file):
    lingpref = {}
    with open(file) as f:
        reader = csv.reader(f)
        next(reader)
        lingpref = dict(reader)
    

def preservePref(list):
    backup = list[:]
    return backup


def processPreflist(preflist):
    backup = {}
    for item in preflist:
        preflist[item].reverse()    
        backup[item] = preservePref(preflist[item])
    return backup


def restorePref(list, backup):
    for item in backup:
        list[item] = preservePref(backup[item])   









def printMatches(matched):
    print("\nMATCHED")
    for item in sorted(matched.keys()):
        print(item+": "+matched[item])



def printQuotas(quota):
    print("\nVACANCIES")
    for item in quota:
        print(item+": "+str(quota[item]))

