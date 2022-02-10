My implementation of TDCE is straightforward. As suggested, I define "one pass" variants of the two strategies, compose those, and then iterate the composition to convergence. I do not support jumps and branches, but instead of throwing an error I check for jumps and branches and, on finding any, correctly do nothing. 

I tested my implementation by running it on the suite of reference examples. There were a few programs that I did a "better" or comparable job on (modulo alpha renaming) so I used turnt's --save utility to clobber the expected values.

My implementation of LVN is organized in a similar way; I compose LVN with TDCE and iterate the composed method until convergence. I used a DataFrame for my table, which may have been a mistake. Anyway I got through it with a few getters and setters. As an extension to the basic algorithm, I expose the semantics of arithmetic, identity, copying, and const, and realize some profit. 

Again, I tested my implementation against the suite of reference examples for TDCE and LVN. Where appropriate, I clobbered the expected values with my own. Introducing constant-folding and exposing the semantics of arithmetic collapses many of the previous examples into two-liners. However, this exposes two problems:
- One, it raises the interesting question of what one should do when tasked with illegal math, e.g. division by zero. I deal with instructions that divide by zero by leaving them alone.
- Two, it makes it a bit tricky to test other features of my LVN implementation because constant-folding magics away lines of code that would have otherwise been evidence of correctly-implemented optimizations. I believe my implementation to be correct because I worked on constant-folding last, and so I had already tested other features against my .out files. However, this is clearly not a good solution long-term. The solution is probably to rely on more function arguments, thereby preventing constant propagation. I haven't done this yet; see below. 

Remaining issues:
- On a three files I have a weird turnt error that I'm hoping to clear up.  
(-vp flags?)
- Arguments to functions!