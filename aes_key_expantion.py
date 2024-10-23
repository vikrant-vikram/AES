def row_mazor_col_mazor(l:list)->list:
    w = []
    for i in range(4):
        temp = []
        for j in range(4):
            temp.append(k[j][i])
        w.append(temp)
    return w

def key_expantion(key = "0f 15 71 c9 47 d9 e8 59 0c b7 ad d6 af 7f 67 98", nr = 11 )-> list:
    key = key.split(" ")
    k = []
    for i in range(0,16,4):
        temp = []
        for j in range(i, i+4):
            temp.append(key[j])
        k.append(temp)



    print(k)
    return []


key_expantion()
