
My work is in two files: 
- dom.py, where I construct the basic domination relation
- dom_extensions.py, where I use the basic relation to construct relations for strict domination, immediate domination, and the domination frontier. 

It was a reasonably straightforward process, more or less proceeding as discussed in class. I found myself wrestling with Python a fair bit; I'm realizing that at heart I really am a functional programmer and so I tend to want/expect things like partial application and immutability. That said, who among us can argue against a Python gem like `if v1 in strict_doms[v2] and (v1 not in strict_doms[v3] for v3 in strict_doms[v2])`? It's poetry, dammit. 

I tested my work using Turnt the whole time, borrowing from the course repository's examples/test/dom/ and also adding skipped.bril from a previous lesson. I'm glad I did, since it proved to be an interesting example (see below). Compared to what others seem to have done re: testing, my work is quite meagre, essentially just "testing by eye". Plus, it wasn't even that easy: variations in Python's set-ordering meant that Turnt [repeatedly threw false alarms](https://github.com/anshumanmohan/6120/blob/master/lesson5/pain.png).

I ran into two interesting issues: 

Issue 1:
Entry labels that have predecessors. I was a bit stumped but then found a helpful thread about it on Zulip. I followed the advice given there and was out of the woods pretty quickly. Many thanks to Shubham for posting that.

Issue 2:
My example skipped.bril shows what happens when one tries to compute the domination relation using a CFG that is malformed (for some definition of malformed). The CFG marks "l0" and "l1" as the preds of "end", but in fact "l1" is unreachable (it has no preds) and will always be skipped. This causes an incorrect calculation of the dominators. Had we run a cleanup pass using CFG data before running the domination algorithm, we would have killed off the unreachable block "l1" and avoided this issue. 
