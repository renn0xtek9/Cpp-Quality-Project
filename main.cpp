#include <iostream>
#include <probe.h>
#include <memory>



struct DummyPayload{
    int var_a{};
    double var_b{};
};

template<class T> 
class BaseClass
{
public:
    BaseClass(){
        
    }
    void on_Deactivate() {
        m_object.reset();
    }
    std::unique_ptr<T> m_object{};
    virtual void Instantiate() =0 ;
    
    virtual void on_Activate(){
        Instantiate();
    }
    
private:
    
    
};

class DerivedClass: public BaseClass<DummyPayload>
{
public:
    DerivedClass(): BaseClass<DummyPayload>(){
        Instantiate();
    }
    void Instantiate() override{
        std::cout<<"Insantiate";
        m_object=std::make_unique<DummyPayload>(DummyPayload{2,3.0});
    }
};





int main ( int argc, char **argv )
{
    Probe();
    
    DerivedClass myobjec;

    
    
    return 0;
}
