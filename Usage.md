#Usage
This is the full help file of 73Bot.

###Dice Usage
!roll:
-    XdY
-    XdY+Z
-    XdY-Z
-    Z*XdY
-   sXdY     - Sort (Low to High) (implies verbose)
-   vXdY     - Verbose (Describe each roll)
-   aXdY     - Array (skip printing grand total)
-    XdYeZ   - Explode (Reroll Z or higher)
-    XdYbZ   - Brutal  (Reroll Z or lower)
-    XdYtZ   - Target Z or higher
-    XdYfZ   - Fail on Z or lower
-    XdYkZ   - Keep Z highest
-    XdY+AdB - Multiple Dice
-!nwod:
-    X         - X d10s, rerolling 10s
-    XeY     - X d10s, rerolling Y dice. 0 to reroll none.
-    vX(eY)  - Verbose mode
-    sX(eY)  - Sort mode (implies verbose)
-!owod:
-    XtY     - X d10s, with a target threshold of Y, subtracting ones and highlighting botches.
-!xia:
-    X       - X d10s, grouped together and sorted by width.
!tp:
    XpYmZ   - X+Y+Z d6s, separated into X panic dice, Y min-2 dice, & Z normal dice, sorted internally
    
###Game Usage
- !pause - will print pause line for game play session
- !begin - will print begin line for game play session
- !end - will print end line for game play session

###General Usage
- !wiki - coming soon
- !help - shows a basic use chart
- !fullhelp - prints a link to this readme
- !say x - says x

###Admin Usage
- !joinchan x - 73 will join another channel, writes to .ini file
- !quitchan x - coming soon
- !stop password - will stop bot
- !reload - reloads config file
- !addadmin nick - add admin to list
- !nick nick - to change the name of the bot
