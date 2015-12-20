# PyRC-73Bot
Does dice and the such

###Dice Usage
!roll:
    XdY
    XdY+Z
    XdY-Z
    Z*XdY
   sXdY     - Sort (Low to High) (implies verbose)
   vXdY     - Verbose (Describe each roll)
   aXdY     - Array (skip printing grand total)
    XdYeZ   - Explode (Reroll Z or higher)
    XdYbZ   - Brutal  (Reroll Z or lower)
    XdYtZ   - Target Z or higher
    XdYfZ   - Fail on Z or lower
    XdYkZ   - Keep Z highest
    XdY+AdB - Multiple Dice
!nwod:
    X         - X d10s, rerolling 10s
    XeY     - X d10s, rerolling Y dice. 0 to reroll none.
    vX(eY)  - Verbose mode
    sX(eY)  - Sort mode (implies verbose)
!owod:
    XtY     - X d10s, with a target threshold of Y, subtracting ones and highlighting botches.
!xia:
    X       - X d10s, grouped together and sorted by width.
!tp:
    XpYmZ   - X+Y+Z d6s, separated into X panic dice, Y min-2 dice, & Z normal dice, sorted internally