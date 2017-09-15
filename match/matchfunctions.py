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

def couplesToEnd(couple, freeling):
    while couple:
        p1, p2 = couple.popitem()
        freeling.insert(0, p1)


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
        #notMid = [shift for shift, num in quota.items() if "shift does not start with M")


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
            if ling in leftovers:
                leftovers.remove(ling)
            quota[vacancy] -= 1



# Place LWOP on a shift
def assignLWOP(leftovers, lwop, quota, matched):    
    print(leftovers)
    leftovers.extend(lwop)
    #print("---------------------------------")
    #print(leftovers)
    while leftovers:
        #print("---------------------------------")
        #print(leftovers)
        for shift in quota:
            if leftovers and quota[shift] > 0:
                ling = leftovers.pop()
                matched[ling] = shift
                quota[shift] -= 1




def getRank(p, shiftpreflist):
    try:
        return shiftpreflist.index(p)
    except:
        return -1

def doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples={}, rebalance=[]):
    while freeling:
        # Get first linguist
        ling = freeling.pop()
        
        # Get linguist's nth shift choice (if no choice left, add ling to leftovers)
        try:
            shift = lingpref[ling].pop()
        except:
            print("NO MATCH POSSIBLE... Add "+ling+" to leftovers")
            leftovers.append(ling)
            if ling in couples:
                print("Add partner "+couples[ling]+" to leftovers")
                leftovers.append(couples[ling])
                if couples[ling] in freeling:
                    freeling.remove(couples[ling])
            continue
        
        print(ling + " trying " + shift + "...", end=" ")
        
        # Reject linguist if not in shift preferences
        if ling not in shiftpref[shift]:
            print("REJECTED")
            freeling.append(ling)
            continue

        # Reject linguist if part of couple and partner not in shift preferences
        if ling in couples and couples[ling] not in shiftpref[shift]:
            print("partner REJECTED")
            freeling.append(ling)
            continue

        # Otherwise accept    
        print("ACCEPTED")    
        matched[ling] = shift
        quota[shift] -= 1

        if ling in couples:
            matched[couples[ling]] = shift
            if couples[ling] in freeling:
                freeling.remove(couples[ling])
            quota[shift] -= 1
            print(couples[ling] + " assigned to " + shift + " with partner")
   
        # If too many people assigned to this shift, drop the worst one(s)
        hold = '' 
        while quota[shift] < 0:
        #if quota[shift] < 0:
            worstling = getWorst(getMatched(shift, matched), shiftpref[shift])
            matched.pop(worstling)
            quota[shift] += 1
            freeling.append(worstling)
            print(worstling + " bumped from " + shift)

            # If part of a couple drop partner and add shift to rebalance list
            if worstling in couples: 
                matched.pop(couples[worstling])
                quota[shift] += 1
                if shift not in rebalance:
                    rebalance.append(shift)
                print(couples[worstling] + " bumped from " + shift)
                if hold != '':
                    freeling.remove(hold)
                    matched[hold] = shift
                    quota[shift] -= 1
            else:
                hold = worstling

          
        # If no more of this slot available, pare down the pref list
        if quota[shift] == 0:
            worstling = getWorst(getMatched(shift, matched), shiftpref[shift])
            #if worstling not in couples:
            i = shiftpref[shift].index(worstling)
            #del shiftpref[shift][(i+1):]
            del shiftpref[shift][:i]
            #print(shiftpref[shift])







    '''
    #check stability
    for ling in matched:
        print("\n"+ling+" "+matched[ling])
        lpreflist = lingpref[ling]
        lpreflist.append(matched[ling])
        #x = lingpref[l] #.index(matched[l])

        preferredshifts = list(set(quota.keys()) - set(lpreflist))
        print(preferredshifts)
        
        for sh in preferredshifts:
            lingrank = getRank(ling,shiftpref[sh])
            
            print(sh +" (" + str(lingrank) +")")
            assignedlings = [ling for ling, shift in matched.items() if shift == sh]
            #print(v)
            #if s prefers ling to matched[s]
            for name in assignedlings:
                assignedrank = getRank(name,shiftpref[sh])

                if lingrank < assignedrank:
                    ghj = ''
                
                    #print("OK")
                else:
                    print(name +": "+str(assignedrank),end=" ")
                    print("PROBLEM")
    '''
    '''
    while rebalance:
        shift = rebalance.pop()
        print("========> "+shift)
        #for item in shiftpref[shift]:
        #    print(item)
        worst = getWorst(getMatched(shift, matched), shiftpref[shift])
        
        i = getRank(getWorst(getMatched(shift, matched), shiftpref[shift]), shiftpref[shift])
        print(shift)
        for item in shiftpref[shift][(i+1):]:
            print(item)
            #assrank = getRank(item,shiftpref[sh])
            #lingrank = getRank(matched
            #freeling.append(item)
            try:
                qq = matched.pop(item)
                
            except:
                continue
            freeling.append(item)
            quota[qq] += 1
            if item in couples:
                try:
                    qq = matched.pop(couples[item])
                    quota[qq] += 1
                except:
                    pass
            if qq not in rebalance:
                rebalance.append(qq)

            #processCouples(couple, freeling)
            #processLWOP(lwop, freeling)
            #for name in merit:
            #    try:
            #        freeling.remove(name)
            #    except:
            #        continue 
            #for name in manual:
            #    try:
            #        freeling.remove(name)
            #    except:
            #        continue 
     
        doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota)
    
    '''












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