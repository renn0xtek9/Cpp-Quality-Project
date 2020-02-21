#include <probe.h>
#include <iostream>
#include <memory>
#include <vector>

int returnvecsize() {
  std::vector<int> vec;
  vec.emplace_back(1);
  return (vec.size() == 1);
}

int main(int argc, char** argv) {
  if (returnvecsize()) std::cout << "done";
  return 0;
}
