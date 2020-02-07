#include <iostream>
#include <probe.h>
#include <memory>


class DummyPayload{
public:
    static int instantiation_counter;
    DummyPayload(int vara, double varb){
        DummyPayload::instantiation_counter+=1;
        var_a=vara;
        var_b=varb;
    }
    int var_a{};
    double var_b{};
};
int DummyPayload::instantiation_counter=0;

template<class T> 
class BaseClass
{
public:
    BaseClass() =default ;
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
    DerivedClass(): BaseClass(){
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
    myobjec.on_Deactivate();
    if(myobjec.m_object)
    {
        std::cout<<"Objec exist !!!"<<std::endl;
        std::cout<<myobjec.m_object->var_a<<std::endl;
    }
    else
    {
        std::cout<<"Object Does not exist"<<std::endl;
    }
    
    myobjec.on_Activate();
    myobjec.on_Deactivate();
    myobjec.on_Activate();
     if(myobjec.m_object)
    {
        std::cout<<"Objec exist !!!"<<std::endl;
        std::cout<<DummyPayload::instantiation_counter<<std::endl;
    }
    else
    {
        std::cout<<"Object Does not exist"<<std::endl;
    }    

    
    
    return 0;
}
