I went for the unambitious route: I print a message every time I encounter a load instruction!

I modified Skeleton.cpp as needed, wrote a simple runtime library that is only compiled once, and generated a few example cases. You may notice an attempt to use Turnt; this was eventually scaled down. Turnt is now just used to generate .o files for all the example cases in one go. Sadly it is still necessary to link the .o files and run the exe files by hand.

You may also notice that my examples have a float/int division slant. Indeed, my initial goal was to print out one thing for integer divisions and another thing for float divisions. Doesn't seem all that hard, and I'm sure I will be shown how easy it is, but I did get a bit lost in the LLVM jungle. I found it tricky to eke out the kind of operand that a Binary Operator was working with. In any case, I ended up going with Load, an operand that I saw being used in examples.

To compile:
1. cd to the build/ directory; run the usual `cmake ..` and `make` instructions to generate an .so file
2. moving one directory up, run `gcc -c rtlib.c` to generate an .o file for the library
3. changing to the test/ directory, run `turnt *.c` to generate .o files for all my examples
4. now, for each example, run `gcc filename.o ../llvm-pass-skeleton/rtlib.o -o exe` and then `./exe`