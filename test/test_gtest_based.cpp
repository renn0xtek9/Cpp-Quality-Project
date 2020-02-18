#include <gtest/gtest.h>

void function_that_throw() {
  throw std::exception();
}
void this_function_has_no_except() noexcept {
  function_that_throw();
}

TEST(WhatHappenIfThrownFromANoExcept, DummyTest) {
  this_function_has_no_except();
  EXPECT_EQ(true, true);
}

TEST(WhatHappenIfFail, DummyTest) {
  FAIL();
  EXPECT_EQ(true, true);
};
TEST(WhatHappenIfThrown, DummyTest) {
  function_that_throw();
  EXPECT_EQ(true, true);
}
TEST(WhatHappenIfExit1, DummyTest) {
  exit(1);
  EXPECT_EQ(true, true);
}
TEST(ThisTestSucceed, DummyTest) {
  EXPECT_EQ(true, true);
}
