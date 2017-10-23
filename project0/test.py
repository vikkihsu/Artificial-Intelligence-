def median(lst):
    new_lst = lst.sort()
    print(lst.sort())
    if len(new_lst) % 2 != 0:
        return new_lst[(len(new_lst)+1)/2]
    else:
        return (new_lst[len(new_lst)/2]+new_lst[len(new_lst)/2+1])/2

median([1,2,4,6,7,5])