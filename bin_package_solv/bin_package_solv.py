def bin_packing (size: float, zero: int, answer: list, vinfo, got_bins, alg_ans: int):
    global min

    for ind1 in range(zero, len(vinfo)):
        for ind2 in range(0,len(got_bins)):
            if got_bins[ind2] + vinfo[ind1].num <= size:
                if alg_ans <= min:
                    vinfo[ind1].num_bin = ind2
                    got_bins[ind2] += vinfo[ind1].num
                    if (got_bins[ind2] == vinfo[ind1].num):
                        alg_ans += 1
                    bin_packing(size, ind1+1, answer, vinfo, got_bins, alg_ans)
                    vinfo[ind1].num_bin = -1
                    got_bins[ind2] -= vinfo[ind1].num
                if alg_ans >= min:
                    return

    if vinfo[len(vinfo) - 1].num_bin == -1:
        return

    if alg_ans < min:
        min = alg_ans
        for i in range(0, len(vinfo)):
            answer[vinfo[i].idx] = vinfo[i].num_bin
    return


class Info:
    def __init__(self, num, idx, num_bin):
        self.num = num
        self.idx = idx
        self.num_bin = num_bin


n = int(input())
size = float(input())

s = []

for i in range(0,n):
    s.append(Info(num=float(input()), num_bin=-1, idx=i))


s_new = sorted(s, key=lambda Info: Info.num, reverse=True)
# for i in range(n):
#     print(s_new[i].idx)

my_answer = [0] * n
bins_ = [0.0] * n
min = n

bin_packing(size, 0, my_answer, s_new, bins_,0)

for el in my_answer:
    print(el+1, end=' ')

