#include <probe.h>
#include <iostream>
#include <memory>
#include <vector>
#include "version.hpp"

int returnvecsize() {
  std::vector<int> vec;
  vec.emplace_back(1);
  return (vec.size() == 1);
}

int main(int argc, char** argv) {
  if (returnvecsize()) std::cout << "done" << std::endl;
  std::cout << "Version" << getVersion();
  return 0;
}
