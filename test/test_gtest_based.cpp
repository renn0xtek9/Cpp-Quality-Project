#include <gtest/gtest.h>

void function_that_throw()
{
    throw std::exception();    
}
void this_function_has_no_except() noexcept
{
    function_that_throw();
}

TEST(DummyTest, WhatHappenIfThrownFromANoExcept)
{
    this_function_has_no_except();
    EXPECT_EQ(true,true);
}

TEST(DummyTest, WhatHappenIfFail)
{
    FAIL();
    EXPECT_EQ(true,true);
};
TEST(DummyTest ,WhatHappenIfThrown)
{
    function_that_throw();
    EXPECT_EQ(true,true);
}
TEST(DummyTest, WhatHappenIfExit1)
{
    exit(1);
    EXPECT_EQ(true,true);
}
TEST(DummyTest, ThisTestSucceed)
{
    EXPECT_EQ(true,true);
}
