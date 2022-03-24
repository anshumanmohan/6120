
Phew, I found this assignment rather challenging. I didn't actually have to write very much code, largely because I was able to use built-in LLVM methods to do the heavy lifting. However, this also meant that I was playing with lots of code that I didn't understand. There was lots of monkey-see-monkey-do using all manner of internet sources, followed by silly experimentation of my own.

I tinkered with `LoopPass` a fair bit but couldn't figure it out, especially since I needed no just the loops but also their containing blocks and preheaders.

The following resource was a real lifesaver, although it steered me towards `LoopInfo`:
https://www.inf.ed.ac.uk/teaching/courses/ct/17-18/slides/llvm-2-writing_pass.pdf
patched with 
https://stackoverflow.com/questions/30351725/llvm-loopinfo-in-functionpass-doesnt-compile
and
https://stackoverflow.com/a/9701867

I then got into trouble with `clang` segfaulting; this eventually turned out to be because I was tagging branches as loop-invariant and moving them around. I got this to work on four little C programs that I wrote.

I grabbed the Embench test suite and ran my pass on all of it. Some functions were still segfaulting mysteriously (I suspect I am moving other delicate things, no just branches...) but I just nixed those programs. Some very handy cherrypicking! 

Finally, I don't think I deserve any points for evaluation. I struggled to figure out an evaluation tool fully linked up and deployed. Not one of the existing guides for `gperftools` seems to work as written; our `clang` compilation via an LLVM pass complicates things too much. As of writing I believe I have `gperftools` figured out, but the tool fails to work with the embench programs because they don't have `main` methods, gah. In any case, I will stop whining. I could probably figure this out but am deciding not to. Sorry!