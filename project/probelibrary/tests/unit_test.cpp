/*! \file unit_test.cpp
\brief unit tests of probe library
*/

#include <gtest/gtest.h>
#include <probe.h>

/*! \test ProbeSanity
 * \brief Check that the Probe function does not throw
 */
TEST(ProbeSanity, NoThrow) {
  EXPECT_NO_THROW(Probe());
}
