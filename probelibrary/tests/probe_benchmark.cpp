#include<iostream>
#include<chrono>
#include<probe.h>
int main (int argc, char **argv)
{
    auto start = std::chrono::high_resolution_clock::now(); 
    Probe();
    auto stop = std::chrono::high_resolution_clock::now(); 

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start); 
  
    std::cout << "Time taken by function: "<< duration.count() << " microseconds" << std::endl; 
    
    return 0;
}
