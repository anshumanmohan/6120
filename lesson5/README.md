
Note the the example skipped is actually making an error; I've left it in as an interesting example of what happens when the CFG is malformed (for some definition of malformed). 

The CFG marks "l0" and "l1" as the preds of "end", but in fact "l1" is unreachable (it has no preds) and will always be skipped. This causes an incorrect calculation of the dominators.

Had we run a cleanup pass using CFG data before running the dominator algorithm, we would have killed off the unreachable block "l1" and avoided this issue. 