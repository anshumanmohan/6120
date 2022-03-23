#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/IR/Instruction.h"
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
      for (LoopInfo::iterator l = LI.begin();
           l != LI.end();
           l++)
      {
        Loop *L = *l;
        loopCounter++;
        for (Loop::block_iterator b = L->block_begin();
             b != L->block_end();
             b++)
        {
          errs() << "\tI'm a block inside loop #" << loopCounter << "\n";
          BasicBlock *B = *b;
          for (BasicBlock::iterator i = B->begin();
               i != B->end();)
          { // Note the weird increment of i.
            // This tolerates the deletion of an op
            // while still leaving the iteration unaffected.
            if (auto *op = dyn_cast<Instruction>(i++)) // i++?
            {
              if (L->Loop::isLoopInvariant(op))
                continue;
              // if (!isSafeToSpeculativelyExecute(op))
              // continue;
              if (op->mayReadFromMemory())
                continue;
              // OK so now we want to lift if we can...
              BasicBlock *Preheader = L->Loop::getLoopPreheader();
              // Without a preheader, hoisting is not feasible.
              if (!Preheader)
                continue;
              Instruction *InsertPt = Preheader->getTerminator();
              if (L->Loop::hasLoopInvariantOperands(op))
              {
                op->moveBefore(InsertPt);
                errs() << "moved the instruction \n"
                       << *op << "\n";
                changed = true;
                i = B->begin(); // overkill...
                continue;
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
