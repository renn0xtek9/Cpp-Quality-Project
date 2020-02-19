#include <probe.h>
#include <iostream>
#include <memory>
// https://codeyarns.com/2016/11/21/override-and-final-in-c/

class VirtualClass {
 public:
  int j{};
  virtual void foo() = 0;
  virtual void bar() {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
  }
  virtual void override_me() const {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
    std::cout << "\t\tyou did not override me ?" << std::endl;
  }
};

class A : public VirtualClass {
 public:
  void foo() {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
  }
  /*
  void override_me() override{
      std::cout<<"This wouldn't compile thanks to override anyway";
  }
  */
};

class B : public VirtualClass {
 public:
  void foo() {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
  }
  void bar() override {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
  }
  void override_me() const final {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
    std::cout << "This is a final override" << std::endl;
  }
  /*
  void override_me() final{
      std::cout<<"This would't compile because final but not virtual (not virtual because it does not find the
  paren)"<<std::endl;
  }
  */
  virtual void override_me_too() const final {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << std::endl;
    std::cout << "This is valid (thanks to virutal) and final BUT you are not overriding anyhthing (because missing of "
                 "override) !!!"
              << std::endl;
    //         PureVirtualCalss::override_me_too();  //this would not work of course
  }
};
class C : public B {
 public:
  /*
  void override_me() const override
  {
      std::cout<<"This should not compile (overriding a final)"<<std::endl;
  }
  */

  /*
  void override_me_too() const override
  {
      std::cout<<"This should compile because of the final"<<std::endl;
  }
  */

  void bar() override {
    std::cout << __PRETTY_FUNCTION__ << " " << __LINE__ << " " << __FILE__ << " overriding bar" << std::endl;
  }
};

int main(int argc, char** argv) {
  Probe();
  A objA;
  objA.override_me();

  B objB;
  objB.override_me();
  objB.override_me_too();

  C objC;
  objC.bar();

  return 0;
}
