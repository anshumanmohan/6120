My implementation of TDCE is straightforward. As suggested, I define "one pass" variants of the two strategies, compose those, and then iterate the composition to convergence. I do not support jumps and branches, but instead of throwing an error I check for jumps and branches and, on finding any, correctly do nothing. 

I tested my implementation by running it on the suite of reference examples. There were a few programs that I did a "better" or comparable job on (modulo alpha renaming) so I used turnt's --save utility to clobber the expected values.

My implementation of LVN is organized in a similar way; I compose LVN with TDCE and iterate the composed method until convergence. I used a DataFrame for my table, which may have been a mistake. Anyway I got through it with a few getters and setters. As an extension to the basic algorithm, I expose the semantics of arithmetic, identity, and const and realize some profit. Other extensions? TODO

Again, I tested my implementation against the suite of reference examples for TDCE and LVN. Where appropriate, I clobbered the expected values with my own. Opening up constant folding and exposing the semantics of arithmetic collapses many of the previous examples into one-liners; this makes it a bit trickier to test them. The solution is probably to rely more function arguments, thereby blocking constant propagation. I haven't done this yet; see below.

Remaining issues:
- On a three files I have a weird turnt error that I'm hoping to clear up. 
- I don't support arguments to functions, and am hoping to ask about handling that. 
- The example divide-by-zero is interesting because it raises the question of _when_ an error should be raised. Just do nothing for the whole pass? 