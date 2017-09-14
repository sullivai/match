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



    #for item in shiftpref:
    #    shiftpref[item].reverse()

   

    #lbackup = {}
    #for item in lingpref:
    #    lbackup[item] = preservePref(lingpref[item])

    #sbackup = {}
    #for item in shiftpref:
    #    sbackup[item] = preservePref(shiftpref[item])
        
    #process pref lists
    lbackup = processPreflist(lingpref)
    sbackup = processPreflist(shiftpref)


    # Process special cases
    overridden = processOverrides(manual, quota, freeling, shiftpref)
    processMeritlist(merit, overridden, lingpref, quota, freeling, shiftpref)
    processLWOP(lwop, freeling)
    couples = processCouples(couple, freeling)
    processWaivers(shiftpref, medical)

    
    # Match singles
    matched = {}
    leftovers = [] 
    doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota)

    #for item in shiftpref['DMON-THU']:
    #    print(item,end=" | ")
    print("\n")    



    # Match couples
    rebalance = []
    while couple:
        p1, p2 = couple.popitem()
        freeling.append(p1)
        #freeling.append(p2)
    doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)
    print("\n\nNext\n\n")

    #for item in shiftpref['DMON-THU']:
    #    print(item,end=" | ")
    print("\n")  
    print("AFTER ROUND 1")
    printMatches(matched)
    print(leftovers)

    '''
    # Re-stabilize
    while rebalance:
        shift = rebalance.pop()
        i = getRank(getWorst(matched, shiftpref[shift]), shiftpref[shift])
        for name in shiftpref[shift][:i]:
            freeling.append(name)
            if name in couples and couples[name] not in freeling:
                #freeling.append(couples[name])
            if name in matched:
                shift = matched.pop(name)
                quota[shift] += 1
                rebalance.append(shift)
        
        doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)        
    '''




    print("rebalance")
    
    print(rebalance)
    printQuotas(quota)

    for poo in rebalance:
        for item in lbackup:
            lingpref[item] = preservePref(lbackup[item])
 
        for item in sbackup:
            shiftpref[item] = preservePref(sbackup[item])


        print(poo)
        # for each person assigned to poo
        assignedlings = [ling for ling, shift in matched.items() if shift == poo]
        
        betterlings = shiftpref[poo][1:]

        for ling in betterlings:
            if ling in matched:
                s = matched.pop(ling)
                freeling.append(ling)
                if ling in couples:
                    # remove ling from freeling
                    freeling.remove(ling)

                    if couples[ling] not in couple.keys():
                        couple[ling] = couples[ling]

                    # remove partner from matched
                    if couples[ling] in matched:
                        matched.pop(couples[ling])
                        quota[s] += 1
                    # increment quota
                    
                    # add ling to couple if partner not in couple




                    if couples[ling] in freeling:
                        freeling.remove(couples[ling])
                    #couple[ling] = couples[ling]
                    #freeling.remove(ling)
                quota[s] += 1
                if s not in rebalance:
                    rebalance.append(s)
        doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)
        while couple:
            p1, p2 = couple.popitem()
            freeling.append(p1)
        #    #freeling.append(p2)
        doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)
        print("\n\nnext\n\n")






    print(rebalance)
    printQuotas(quota)
    print("AFTER ROUND 2")
    printMatches(matched)
    print('x')
    '''
        
        #for ling in assignedlings:
            print("\t"+ling)
            # get each shift they prefer to poo
            lpreflist = lingpref[ling]
            lpreflist.append(matched[ling])
            preferredshifts = list(set(quota.keys()) - set(lpreflist))
            #get each person assigned to that shift

            # if that shift prefers ling to anyone it's assigned to, problem
            for sh in preferredshifts:
                assignees = [name for name, shft in matched.items() if shft == sh]
                lingrank = getRank(ling,shiftpref[sh])
                for name in assignees:
                    assignedrank = getRank(name,shiftpref[sh])
                    if lingrank == -1 or lingrank > assignedrank:
                        print("\t\t"+sh + " ("+str(lingrank)+") "+" "+name+" ("+str(assignedrank)+")" +  " OK")
                    else:
                        print("\t\t"+ sh + " ("+str(lingrank)+") "+" "+name+" ("+str(assignedrank)+")" + " blocks" )
                        matched.pop(name)
                        freeling.append(name)
                        quota[sh] += 1
                        if name in couples:
                            matched[couples[name]].pop()
                            quota[sh] += 1
                        rebalance.append(sh)
    '''



                  
        #print('x')







            

    #for item in rebalance:
    #    print(shiftpref[item])

    print("---------------")


    # Slot the rest wherever they'll fit
    assignLeftovers(leftovers, quota, shiftpref, matched)
    assignLWOP(leftovers, lwop, quota, matched)
    matched.update(overridden)

    printMatches(matched)
    printQuotas(quota)

    print(leftovers)
 
    
    

