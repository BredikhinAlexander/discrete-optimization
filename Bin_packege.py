from typing import List

# Leave the whole “solve_bp_decision” function intact
def solve_bp_decision(items: List[float], n_bins: int) -> bool:
    def able_to_pack(items: List[float], bin_capacities: List[float]) -> bool:
        return items == [] or any(
            able_to_pack(
                items[:-1],
                bin_capacities[:i] + [capacity - items[-1]] + bin_capacities[(i + 1):]
            )
            for i, capacity in enumerate(bin_capacities) if capacity >= items[-1]
        )

    return able_to_pack(sorted(items), [1.0] * n_bins)





# You should leave function header intact
def solve_bp_evaluation(items: List[float]) -> int:
    index = len(items)
    for i in range(1,index+1):
        if solve_bp_decision(items, i):
            return i



# You should leave function header intact
def solve_bp_search(items: List[float]) -> List[int]:
    opt = solve_bp_evaluation(items)
    #weights = items.copy()
    cont = dict((i, []) for i in range(1,opt+1))
    cont[1].append(0)
    buf = [0.]*opt
    buf[0] = items[0]

    #weights.pop(0)
    for i in range(1, len(items)):
        for j in cont.keys():

            if len(cont[j]) == 0:
                cont[j].append(i)
                buf[j-1] += items[i]
                #weights.pop(0)
                break

            if buf[j - 1] + items[i] <= 1:
                #weights.pop()
                new_list = items[i+1:]
                buf[j-1] += items[i]
                for k in buf:
                    if k != 0:
                        new_list.append(k)
                result = solve_bp_evaluation(new_list)
                if result == opt:
                    cont[j].append(i)
                    #weights.pop(0)
                    break
                else:
                    buf[j - 1] -= items[i]

    otvet = [0]*len(items)
    for l in cont.keys():
        for k in cont[l]:
            otvet[k] = l

    return otvet





