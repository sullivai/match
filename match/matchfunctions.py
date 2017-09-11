# Process manual overrides
def processOverrides(manual, quota, freeling, shiftpref):
    overridden = {}
    for name in manual:
        # Assign match in manual override dict
        overridden[name] = manual[name]
        quota[manual[name]] -= 1

        # Remove linguist from matching process
        try:
            freeling.remove(name)
        except:
            continue
        
        # If too many overrides assigned, go back and fix quotas manually
        if quota[manual[name]] < 0:
            print("ERROR: NOT ENOUGH SLOTS FOR "+ manual[name] + "!")
            print("FAILURE ON MANUAL OVERRIDES")
            exit(1)
        
        # If this uses up all of one slot, remove everyone from slot's pref list
        if quota[manual[name]] == 0:
            del shiftpref[manual[name]][:]
    return overridden


# Process merit list
def processMeritlist(merit, overridden, lingpref, quota, freeling, shiftpref):
    for name in merit:
        # Assign match in manual override dict
        overridden[name] = lingpref[name].pop()
        quota[overridden[name]] -= 1

        # Remove linguist from matching process
        try:
            freeling.remove(name)
        except:
            continue  

        # If too many overrides assigned, go back and fix quotas manually
        if quota[overridden[name]] < 0:
            print("ERROR: NOT ENOUGH SLOTS FOR " + overridden[name] + "!")
            print("FAILURE ON MERIT LIST")
            exit(1)   

        # If this uses up all of one slot, remove everyone from slot's pref list
        if quota[overridden[name]] == 0:
            del shiftpref[overridden[name]][:]


# Remove people on LWOP from matching process; they will be processed after leftovers
def processLWOP(lwop, freeling):
    for name in lwop:
        try:
            freeling.remove(name)
        except:
            continue


# Remove couples from matching process; they will be processed after first round
def processCouples(couple, freeling):
    couples = {}
    for name in couple:
        partner = couple[name]
        couples[name] = partner
        couples[partner] = name

        try:
            freeling.remove(name)
        except:
            pass
        try:
            freeling.remove(partner)
        except:
            continue   
    return couples 


# Process medical waivers
def processWaivers(shiftpref, medical):
    for item in shiftpref:
        # Delete names of medical waivers from all non-day-shift preference lists
        if not item.startswith("D"):
            shiftpref[item] = [name for name in shiftpref[item] if name not in medical]

 

# Place leftovers on a shift
def assignLeftovers(leftovers, quota, shiftpref, matched):
    flag = True

    while leftovers and flag:
        # find shift(s) with most vacancies
        maxVacancies = [shift for shift, num in quota.items() if quota[shift] == max(quota.values())]
        vacancy = maxVacancies.pop()
        
        # pop names from shiftpref til one on leftover list is found
        ling = ''
        while True:
            try:
                ling = shiftpref[vacancy].pop()
                if ling in leftovers:
                    break
            except:
                flag = False
                break
        if quota[vacancy] > 0:        
            matched[ling] = vacancy
            leftovers.remove(ling)
            quota[vacancy] -= 1



# Place LWOP on a shift
def assignLWOP(leftovers, lwop, quota, matched):    
    print(leftovers)
    leftovers.extend(lwop)
    print("---------------------------------")
    print(leftovers)
    while leftovers:
        print("---------------------------------")
        print(leftovers)
        for shift in quota:
            if leftovers and quota[shift] > 0:
                ling = leftovers.pop()
                matched[ling] = shift
                quota[shift] -= 1

















# return a list of linguist names already matched to a particular shift
def getMatched(shift, matches):
    return [ling for ling, sh in matches.items() if sh == shift]


# return linguist ranked last for a certain shift among matches
def getWorst(matched, shiftpreflist): 
    worst = None
    rank = len(shiftpreflist)  #0
    for ling in matched:
        try:
            if shiftpreflist.index(ling) < rank:
            #if shiftpreflist.index(ling) >= rank:  # valueError if not in list
                rank = shiftpreflist.index(ling)
                worst = ling
        except:
            continue
    return worst
























'''
def getMatchedRanks(matched, shiftpreflist):
    s = []
    w = {}
    for name in matched:
        print(name+"------"+str(shiftpreflist.index(name)))
        w[name] = shiftpreflist.index(name)

    return sorted(w.values())
'''