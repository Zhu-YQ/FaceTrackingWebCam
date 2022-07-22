def parsePointInfo(info):
    symbol_index_list = []
    for i in range(len(info)):
        if info[i] == '(':
            symbol_index_list.append(i)
        elif info[i] == ',':
            symbol_index_list.append(i)
        elif info[i] == ')':
            symbol_index_list.append(i)
        else:
            continue
    result_list = [int(info[symbol_index_list[0] + 1 : symbol_index_list[1]]),
                   int(info[symbol_index_list[1] + 1 : symbol_index_list[2]])]
    return result_list
