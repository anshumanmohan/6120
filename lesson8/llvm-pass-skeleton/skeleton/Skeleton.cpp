#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
using namespace llvm;

namespace
{
  struct LICM : public FunctionPass
  {
    static char ID;
    LICM() : FunctionPass(ID) {}

    void getAnalysisUsage(AnalysisUsage &AU) const
    {
      AU.setPreservesCFG();
      AU.addRequired<LoopInfoWrapperPass>();
    }

    virtual bool runOnFunction(Function &F)
    {
      bool changed = false;
      errs() << "I saw a function called " << F.getName() << "\n";
      LoopInfo &LI = getAnalysis<LoopInfoWrapperPass>().getLoopInfo();
      int loopCounter = 0;
      for (LoopInfo::iterator l = LI.begin(), li_end = LI.end();
           l != li_end;
           l++)
      {
        Loop *L = *l;
        loopCounter++;
        for (Loop::block_iterator b = L->block_begin(), l_end = L->block_end();
             b != l_end;
             b++)
        {
          errs() << "\tI'm a block inside loop #" << loopCounter << "\n";
          BasicBlock *B = *b;
          for (BasicBlock::iterator i = B->begin(), b_end = B->end();
               i != b_end;)
          { // Note the weird increment of i.
            // This tolerates the deletion of an op
            // while still leaving the iteration unaffected.
            if (auto *op = dyn_cast<Instruction>(i++))
            {
              if (L->Loop::hasLoopInvariantOperands(op))
              {
                errs() << "\t\tI'm an instr inside the blk with LI operands\n";
                // We can hoist this to _just before_ the _end_ of the preheader
                if (BasicBlock *pre = L->getLoopPreheader())
                {
                  Instruction *end_of_pre = pre->getTerminator();
                  // op->insertBefore(end_of_pre);
                  // works by itself, but then the compiler loops/blocks forever
                  // op->removeFromParent();
                  // segfaults clang
                  // op->eraseFromParent();
                  // segfaults clang
                  // op->moveBefore(end_of_pre);
                  // comment out the "insertBefore" and run this. segfaults.
                  // changed = true;
                  // errs() << "\t\tI've been moved\n";
                }
              }
            }
          }
        }
      }
      errs() << "\tthe function has " << loopCounter << " loop(s) total\n";
      // I'm not sure why it would block or loop forever...
      // the above line IS printed,
      // so I can only assume that the return below also goes through.
      // Something loops/blocks forever AFTER that.
      return changed;
    }
  };
}

char LICM::ID = 0;

// Automatically enable the pass.
// http://adriansampson.net/blog/clangpass.html
static void registerLICM(const PassManagerBuilder &,
                         legacy::PassManagerBase &PM)
{
  PM.add(new LICM());
}
static RegisterStandardPasses
    RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
                   registerLICM);
