#include "probe.h"
#include <vector>
void Probe() {
  std::vector<int> vec;
  for (int i = 0; i < 100000; i++) {
    vec.emplace_back(0);
  }
}
