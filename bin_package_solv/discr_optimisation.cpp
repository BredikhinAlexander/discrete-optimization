//
// Created by Александр on 18.05.2020.
//

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct My_struct
{
    int bin_index;
    double weight;
    int num;
};

int minn = 0;
int bin_packing(double max_weight, int nul, vector<int> &otvet, vector<My_struct> &buff, vector<double>& biins, int answer)
{
    for(int index_1 = nul; index_1 < buff.size(); ++index_1) {
        for(int index_2 = 0; index_2 < biins.size(); ++index_2) {
            if(biins[index_2] + buff[index_1].weight <= max_weight) {
                if(answer <= minn) {
                    buff[index_1].bin_index = index_2;
                    biins[index_2] += buff[index_1].weight;
                    if(biins[index_2] == buff[index_1].weight) {
                        answer++;
                    }
                    bin_packing(max_weight, index_1 + 1, otvet, buff, biins, answer);
                    buff[index_1].bin_index = -1;
                    biins[index_2] -= buff[index_1].weight;
                }
                if(answer >= minn) {
                    return answer;
                }
            }
        }
    }
    if(buff[buff.size() - 1].bin_index == -1)
        return answer;
    if(answer < minn) {
        minn = answer;
        for(int i = 0; i < buff.size(); ++i) {
            otvet[buff[i].num] = buff[i].bin_index;
        }
    }
    return answer;
}

int main()
{
    int number = 0;
    double max_weight = 0.0;
    cin >> number >> max_weight;
    minn = number;



    vector<My_struct> buff;
    for(int i = 0; i < number; ++i)
    {
        My_struct my_first;
        cin >> my_first.weight;
        my_first.bin_index = -1;
        my_first.num = i;
        buff.push_back(my_first);
    }
    // sort(begin(buff), end(buff), [](const My_struct &l, const My_struct &r){return l.weight > r.weight;});
    sort(buff.begin(), buff.end(), [](const My_struct &left, const My_struct &right)
                                                                                    {return left.weight > right.weight;});


    vector<double> biins(number, 0);
    vector<int>otvet(number, 0);

    bin_packing(max_weight, 0,  otvet, buff, biins, 0);


    for(int el : otvet)
    {
        cout << el + 1;
        cout << " ";
    }
    return 0;
}

