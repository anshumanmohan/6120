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
            // This tolerates the deletion of op.
            if (auto *op = dyn_cast<Instruction>(i++))
            {
              if (L->Loop::hasLoopInvariantOperands(op))
              {
                errs() << "\t\tI'm an instruction inside that block with LI operands\n";
                // let's lift this above the loop
                if (BasicBlock *pre = L->getLoopPreheader())
                {
                  Instruction *end_of_pre = pre->getTerminator();
                  // op->insertBefore(end_of_pre);
                  // changed = true;
                  // errs() << "\t\tI've been moved\n";
                  // op->removeFromParent();
                  // op->eraseFromParent();
                  // op->moveBefore(end_of_pre);
                }
              }
            }
          }
        }
      }
      errs() << "\tthe function has " << loopCounter << " loop(s) total\n";
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
