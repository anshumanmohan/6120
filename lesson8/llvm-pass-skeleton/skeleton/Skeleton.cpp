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
      errs() << "I saw a function called " << F.getName() << "!!\n";

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
