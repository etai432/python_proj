import copy

def det3(list1):
    save_list=copy.deepcopy(list1)
    print(save_list)
    for i in range(1,4):
        print("original list: ", list1)
        list1.pop(0) #changing list1
        list1[i].pop(i)
        list1[i-1].pop(i-1)
        list1 = save_list[:] #resetting list1
        print("copying back to list1: ", list1)

n = [[2,4,2],[3,1,1],[1,2,0]]
det3(n)