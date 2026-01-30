#include <fstream>
#include <iostream>
#include <sstream>
using namespace std;

int main() {
    ifstream f("input.txt");
    stringstream ss;
    if (f.good()) { ss << f.rdbuf(); }
    string input = ss.str();
    if (input.find_first_not_of(" \n\r\t") == string::npos) {
        cerr << "No input provided. Edit input.txt.\n";
        return 1;
    }
    cout << "# Safety Checklist\n\n";
    cout << "## Checklist\n";
    cout << "- [ ] PPE verified\n- [ ] Job hazard analysis completed\n- [ ] Lockout/tagout if needed\n- [ ] Housekeeping maintained\n\n";
    cout << "## Raw Notes\n```text\n" << input << "\n```\n";
    return 0;
}
