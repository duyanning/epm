#include <iostream>
#include "foo.h"

int main()
{
    using namespace std;
    // call C function
    int x = foo(5);
    cout << x << endl;
}
