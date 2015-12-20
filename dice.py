import random
import re

class DiceRoller:
    '''
    An independent class for rolling the d's
    Currently stolen from https://github.com/CrystalDave/PyRC-Diceroller for testing
    '''
    def __init__(self):
        return
    
    def base_roll(s):
        """General dice rolling"""
        sort = False
        verbose = False
        array = False
        sFlags = re.match(r'[a-z]+',s,re.I)
        if sFlags:
            sFlags = sFlags.group()
            if 's' in sFlags:
                sort = True
                verbose = True
                s = s.replace('s','',1)
            if 'v' in sFlags:
                verbose = True
                s = s.replace('v','',1)
            if 'a' in sFlags:
                array = True
                s = s.replace('a','',1)

        sComment = ''
        sComStart = re.search(r'\d ',s)
        if sComStart:
            sComment = s[sComStart.end():]
            s = s[:sComStart.end()-1]

        modifier = re.search(r'[\+|-]\d+$',s) # Dice modifier. +-Z
        if modifier:
            modifier = modifier.group()
            if modifier[0] == '-':
                modifier = int(modifier[1:])*-1
            else:
                modifier = int(modifier[1:])
        else: modifier = 0

        explode = re.search(r'e\d+',s) # e prefacing
        if explode:
            explode = explode.group()
            explode = int(explode[1:])
            if explode == 1:
                return "Error: Don't make every die explode."

        brutal = re.search(r'b\d+',s) # b prefacing
        if brutal:
            brutal = brutal.group()
            brutal = int(brutal[1:])

        target = re.search(r't\d+',s) # t prefacing
        if target:
            target = target.group()
            target = int(target[1:])

        failure = re.search(r'f\d+',s) # f prefacing
        if failure:
            failure = failure.group()
            failure = int(failure[1:])

        keep = re.search(r'k\d+',s) # k prefacing
        if keep:
            keep = keep.group()
            keep = int(keep[1:])

        multiRe = re.search(r'(\d+)\*(\d*d\d+)',s) # W*XdY
        if multiRe:
            multimod = multiRe.group(1)
            multimod = int(multimod)
            tempS = s
            tempS = tempS[:multiRe.start()] + tempS[multiRe.end():]
            insS = ''
            for n in range(0,multimod):
                insS = insS + multiRe.group(2) + '+'
            insS = insS[:-1]
            tempS = insS + tempS
            s = tempS

        dicepairs = re.findall(r'(\d*)d(\d+)',s) # Basic dice pairs: XdY
        if not dicepairs: return "an error."

        printqueue = []
        dicetotal = modifier
        successes = fails = expcount = brucount = 0
        if len(dicepairs) == 1:
            array = True
        for n in range(0,len(dicepairs)):
            if n < 0:
                return "Error: Roll at least one die."
            sortqueue = []
            subtotal = 0
            if dicepairs[n][0] == "": dicepairs[n] = ('1',dicepairs[n][1])
            i = int(dicepairs[n][0])
            while (i > 0): #primary dicerolling
                i += -1
                if n < 0:
                    return "Error: Roll at least a one-sided die."
                die = random.randint(1,int(dicepairs[n][1]))
                if explode:
                    if die >= explode:
                        i += 1
                        expcount += 1
                if brutal:
                    if brutal == dicepairs[n][1]:
                        pass
                    elif die <= brutal:
                        die = random.randint(1,int(dicepairs[n][1]))
                        brucount += 1
                if target:
                    if die >= target:
                        successes += 1
                if failure:
                    if die <= failure:
                        fails += 1
                dicetotal += die
                subtotal  += die
                sortqueue.append(die)
            if sort:
                sortqueue.sort()
            if keep:
                keeptemp = len(sortqueue) - keep
                for i in range(0,keeptemp):
                    temp = sortqueue.pop(min(sortqueue))
                    subtotal = subtotal - temp
                    dicetotal = dicetotal - temp
            printqueue.append(str(dicepairs[n][0])+"d"+str(dicepairs[n][1])+":")
            if verbose:
                for n in range(0,len(sortqueue)):
                    printqueue.append(str(sortqueue[n]))
            printqueue.append("= "+str(subtotal))
        if not array:
            printqueue.append("Grand total: " + str(dicetotal) + ".")
        if explode:
            printqueue.append(str(expcount) + " exploded, hitting a "+ str(explode) + " or higher. ")
        if brutal:
            printqueue.append(str(brucount) + " hit a " + str(brutal) + " or under, and were rerolled. ")
        if target:
            printqueue.append(str(successes) + " succeeded on a " + str(target) + " or higher.")
        if failure:
            printqueue.append(str(fails) + " failed on a " + str(failure) + " or lower.")
        printqueue.append(sComment)
        return ' '.join(printqueue)
