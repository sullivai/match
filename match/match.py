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
            leftovers.append(ling)
            if ling in couples:
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
            print(shiftpref[shift])


    


    
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

    for item in shiftpref['DMON-THU']:
        print(item,end=" | ")
    print("\n")    



    # Match couples
    rebalance = []
    while couple:
        p1, p2 = couple.popitem()
        freeling.append(p1)
        #freeling.append(p2)
    doTheMatch(freeling, lingpref, shiftpref, leftovers, matched, quota, couples, rebalance)
    print("\n\nNext\n\n")

    for item in shiftpref['DMON-THU']:
        print(item,end=" | ")
    print("\n")  



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


    # Slot the rest wherever they'll fit
    mf.assignLeftovers(leftovers, quota, shiftpref, matched)
    mf.assignLWOP(leftovers, lwop, quota, matched)
    matched.update(overridden)

    uf.printMatches(matched)
    uf.printQuotas(quota)

    print(leftovers)
 
    
    

