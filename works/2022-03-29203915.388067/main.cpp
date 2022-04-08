#include <iostream>
#include <fstream>
using namespace std;
int main(int argc, char* argv[]){
  int x,y;
  ifstream file(argv[1]);
  file >> x >> y;
  cout << x+y;
  return 0;
}