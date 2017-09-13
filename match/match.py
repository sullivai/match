#from tkinter import *
import matchfunctions as mf
import utilityfunctions as uf
from conf import *



    

#def getWorse(p1, p2, shiftpreflist):
#    worse = p1 if shiftpreflist.index(p1) > shiftpreflist.index(p2) else p2
#    return worse


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
            worstling = mf.getWorst(mf.getMatched(shift, matched), shiftpref[shift])
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

        #if quota[shift] < 0:
        #    worstling = mf.getWorst(mf.getMatched(shift, matched), shiftpref[shift])
        #    matched.pop(worstling)
        #    quota[shift] += 1
        #    freeling.append(worstling)
        #    print(worstling + " bumped from " + shift)

        #    if worstling in couples:
        #        matched.pop(couples[worstling])
        #        quota[shift] += 1
        #        rebalance.append(shift)
        #        print(couples[worstling] + " bumped from " + shift)
        #        #if hold != '':
        #        #    freeling.remove(hold)
        #        #    matched[hold] = shift
        #        #    quota[shift] -= 1

           
        # If no more of this slot available, pare down the pref list
        if quota[shift] == 0:
            worstling = mf.getWorst(mf.getMatched(shift, matched), shiftpref[shift])
            #if worstling not in couples:
            i = shiftpref[shift].index(worstling)
            #del shiftpref[shift][(i+1):]
            del shiftpref[shift][:i]
            #print(shiftpref[shift])


    


    
#######################################################
##                        MAIN                       ##
#######################################################    
if __name__ == "__main__":
    #root = Tk()
    #w = Label(root, text="Hello, world!")
    #w.pack()
    #root.mainloop()

    #get lingpref
    #get shiftpref
    #get freeling
    #get manual overrides
    #get merit list
    #get LWOP
    #get couples
    #get medicals
    #get quota


    for item in lingpref:
        lingpref[item].reverse()
    for item in shiftpref:
        shiftpref[item].reverse()

    for item in shiftpref['DMON-THU']:
        print(item,end=" | ")
    print("\n")    

    shiftpref2 = {}
    for item in shiftpref:
        x = []
        for thing in shiftpref[item]:
            x.append(thing)
        shiftpref2[item] = x

        


    # Process special cases
    overridden = mf.processOverrides(manual, quota, freeling, shiftpref)
    mf.processMeritlist(merit, overridden, lingpref, quota, freeling, shiftpref)
    mf.processLWOP(lwop, freeling)
    couples = mf.processCouples(couple, freeling)
    mf.processWaivers(shiftpref, medical)

    
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
    uf.printMatches(matched)


    '''
    # Re-stabilize
    while rebalance:
        shift = rebalance.pop()
        i = getRank(mf.getWorst(matched, shiftpref[shift]), shiftpref[shift])
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
    uf.printQuotas(quota)

    #for poo in rebalance:
    #    print(poo)
    #    # for each person assigned to poo
    #    assignedlings = [ling for ling, shift in matched.items() if shift == poo]
        
    #    betterlings = shiftpref[poo][1:]

    #    for ling in betterlings:
    #        if ling in matched:
    #            s = matched.pop(ling)
    #            freeling.append(ling)
    #            if ling in couples and couples[ling] in freeling:
    #                freeling.remove(couples[ling])
    #                couple[ling] = couples[ling]
    #                freeling.remove(ling)
    #            quota[s] += 1
    #            if s not in rebalance:
    #                rebalance.append(s)
    #    doTheMatch(freeling, lingpref, shiftpref2, leftovers, matched, quota, couples, rebalance)
    #    #while couple:
    #    #    p1, p2 = couple.popitem()
    #    #    freeling.append(p1)
    #    #    #freeling.append(p2)
    #    #doTheMatch(freeling, lingpref, shiftpref2, leftovers, matched, quota, couples, rebalance)
    #    print("\n\nNext\n\n")


    print(rebalance)
    uf.printQuotas(quota)
    print("AFTER ROUND 2")
    uf.printMatches(matched)
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




    '''
    while rebalance:
        shift = rebalance.pop()
        print("========> "+shift)
        #for item in shiftpref[shift]:
        #    print(item)
        worst = mf.getWorst(mf.getMatched(shift, matched), shiftpref[shift])
        
        i = getRank(mf.getWorst(mf.getMatched(shift, matched), shiftpref[shift]), shiftpref[shift])
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

            #mf.processCouples(couple, freeling)
            #mf.processLWOP(lwop, freeling)
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


            

    #for item in rebalance:
    #    print(shiftpref[item])

    print("---------------")
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

    # Slot the rest wherever they'll fit
    mf.assignLeftovers(leftovers, quota, shiftpref, matched)
    mf.assignLWOP(leftovers, lwop, quota, matched)
    matched.update(overridden)

    uf.printMatches(matched)
    uf.printQuotas(quota)

    print(leftovers)
 
    
    

