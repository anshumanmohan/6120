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
      AU.addRequired<LoopInfoWrapperPass>();
      AU.setPreservesAll();
    }

    virtual bool runOnFunction(Function &F)
    {
      outs() << "I saw a function called " << F.getName() << "\n";
      LoopInfo &LI = getAnalysis<LoopInfoWrapperPass>().getLoopInfo();
      int loopCounter = 0;
      for (LoopInfo::iterator i = LI.begin(), li_end = LI.end(); i != li_end; i++)
      {
        Loop *L = *i;
        loopCounter++;
        for (Loop::block_iterator b = L->block_begin(), b_end = L->block_end(); b != b_end; b++)
        {
          outs() << "\treporting from loop #" << loopCounter << "\n";
        }
      }
      outs() << "\tthe function has " << loopCounter << " loop(s) total\n";

      return false;
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
