#include <gtest/gtest.h>
#include <probe.h>

TEST(ProbeSanity, NoThrow) {
  EXPECT_NO_THROW(Probe());
}
