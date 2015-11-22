#include "Seq.h"
class CompoundSeq : public Seq {
 public:
 private:
  vector<Seq*> m_seqList;
};
