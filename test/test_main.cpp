#include <iostream>


int main ( int argc, char **argv )
{
    if ( argc<2 ) {
        std::cout<<"Test failed (no argument)"<<std::endl;
        return 1;
    }
    if ( argv[1][0]=='o' ) {
        std::cout<<"Test OK"<<std::endl;
        return 0;
    } else {
        std::cout<<"Test FAILED"<<std::endl;
        return 1;
    }
    return 1;
}
