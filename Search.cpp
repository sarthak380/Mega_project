#include <iostream>
using namespace std;

int main() {
    int nums[] = {5, 2, 9, 1, 5, 6};
    int target = 6;
    int size=6;

    for(int i=0;i<size;i++){
        if(nums[i]==target){
            return i;
        }
    }
    

    return -1;// after this no exxecution ..
}

