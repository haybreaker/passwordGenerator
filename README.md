# passwordGenerator
PasswordGenerator Published for Use within an Organisation, using large scale randomization so even open source, very difficult to crack

This project was undertaken for a corporate service desk environment to ensure any new user accounts or password resets were done with randomness
to ensure security and no standards or duplicate passwords.

The requirements were that passwords used are completley random so that no password has feasible chance of being generated twice, however was still
fairly human readable so that if explained to users over the phone, the level of complexity isn't so hard as to cause misinterpretation. 

This had been generated to use a dictionary to get a word or word combination that reach desired length of password but then substitute at random letters
for particular numbers, symbols etc. From there we can have sure even if a word combination was reached twice, that the number substituion is unlikely to be
similar. 

This states with a basic 2000 word dictionary we approach a number of millions of combinations, and with a more specialized, larger dictionary list, those potentials
grow exponentially. 
