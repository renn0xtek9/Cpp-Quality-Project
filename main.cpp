#include <iostream>
#include <probe.h>

void ShortTime()
{
    std::cout<<"Short"<<std::endl;
    for(int j=0;j<100;j++)
    {
        ;
    }
}
void AllocateLikeMad()
{
    for(int index=0;index<100;index++)
    {
        int *ptr= new int;
    }    
}
void AllocateALittle()
{
    for(int index=0;index<100;index++)
    {
        int *ptr= new int;
    }    
    
}


void SuperLongTime()
{    
    std::cout<<"Long"<<std::endl;
    for(int i=0;i<100;i++)
    {
        ;
    }
}
int main ( int argc, char **argv )
{
    Probe();
    ShortTime();
    SuperLongTime();
    AllocateLikeMad();
    return 0;
}
