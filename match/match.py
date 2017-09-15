from matchfunctions import *
from utilityfunctions import *
from conf import *




    

#def getWorse(p1, p2, shiftpreflist):
#    worse = p1 if shiftpreflist.index(p1) > shiftpreflist.index(p2) else p2
#    return worse





 


    
#######################################################
##                        MAIN                       ##
#######################################################    
if __name__ == "__main__":

    #get lingpref
    #get shiftpref
    #get freeling
    #get manual overrides
    #get merit list
    #get LWOP
    #get couples
    #get medicals
    #get quota
        
    #process pref lists
    lbackup = processPreflist(lingpref)
    sbackup = processPreflist(shiftpref)

    # Process special cases
    overridden = processOverrides(manual, quota, freeling, shiftpref)
    couples = processCouples(couple, freeling)
    processMeritlist(merit, overridden, lingpref, quota, freeling, shiftpref)
    processWaivers(shiftpref, medical)
    processLWOP(lwop, freeling)

    matched = {}
    leftovers = [] 
    rebalance = []

    # Match
    print("Match Round 1")
    couplesToEnd(couple, freeling)
    doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)

    # Rebalance
    print("Rebalance")   

    #for shift in rebalance:
    while rebalance:
        shift = rebalance.pop()

        # for each person assigned to shift
        # assignedlings = [ling for ling, sh in matched.items() if sh == shift]

        # Get all lings preferred by shift to current worst assignment        
        betterlings = shiftpref[shift][1:]

        # Unmatch them and put back in freeling. Put shift they were matched to in rebalance
        for ling in betterlings:
            if ling in matched:
                sh = matched.pop(ling)
                freeling.append(ling)

                # Deal with couples
                if ling in couples:
                    freeling.remove(ling)
                    partner = couples[ling]
                    if partner not in couple.keys():
                        couple[ling] = partner

                    # remove partner 
                    if partner in matched:
                        matched.pop(partner)
                        quota[sh] += 1
                    
                    if partner in freeling:
                        freeling.remove(partner)

                # Increment quota
                quota[sh] += 1

                if sh not in rebalance:
                    rebalance.append(sh)

        # Run the match again
        restorePref(lingpref, lbackup)
        restorePref(shiftpref, sbackup)
        couplesToEnd(couple, freeling)
        doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)




    print(rebalance)

    print("---------------")


    # Slot the rest wherever they'll fit
    assignLeftovers(leftovers, quota, shiftpref, matched)
    assignLWOP(leftovers, lwop, quota, matched)
    matched.update(overridden)

    printMatches(matched)
    printQuotas(quota)
    print(leftovers)
 
    
    

