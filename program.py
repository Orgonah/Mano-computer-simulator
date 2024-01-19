import  controlprogram as micro



table = dict()

def split_line(line):
    line = line.split(' ')
    line = [word.strip() for word in line]
    ans = []
    for i in line:
        for j in i.split(','):
            if j != '':
                ans.append(j)
    return ans

def give_line_number(code):
    ans = []
    line_count = 0
    for i in range(len(code)):
        temp = code[i]
        if temp == []:
            line_count += 1
            continue
        if 'ORG' not in temp:
            code[i].append(line_count)
            ans.append(code[i])
            line_count += 1
        else:
            line_count = int(temp[1])
    
    return ans

def add_item_to_table(line):
    if ':' in line[0]:
        name = line[0][:-1]
        table[name] = line[-1]
        return line[1:]
    else:
        return line

def fill_table(code):
    code = code.split('\n')
    code = [line.strip() for line in code]
    code = [split_line(line) for line in code]
    code = give_line_number(code)
    code = list(map(add_item_to_table, code))
    return code


def dec_to_bin(num):
    ans = bin(num)[2:]
    ans = '0'*(16-len(ans)) + ans
    return ans

def bin_to_bin(num):
    ans = '0'*(16-len(num)) + num
    return ans

def hex_to_bin(num):
    ans = bin(int(num, 16))[2:]
    ans = '0'*(16-len(ans)) + ans
    return ans

def transfer_number(cell):
    inp = str(cell)
    if inp[:4] == "BIN.":
        return bin_to_bin(inp[4:])
    elif inp[:4] == "DEC.":
        return dec_to_bin(int(inp[4:]))
    elif inp[:4] == "HEX.":
        return hex_to_bin(inp[4:])
    else:
        return cell

def assembler(microcode, maincode):
    microbin, microtable = micro.assembler(microcode)
    maincode = fill_table(maincode)
    mainbin = []
    for i in maincode:
        ans = []
        for j in i:
                temp = transfer_number(j)
                if j in microtable:
                    temp = microtable[j][1:-2]
                elif j == 'I':
                    temp = '1'
                elif j in table:
                    temp = dec_to_bin(table[j])
                ans.append(temp)
        if len(ans) == 3:
            ans = '0' + ans[0] + ans[1][-11:] + '-'+str(ans[-1])
        elif len(ans) == 4:
            ans = '1' + ans[0] + ans[1][-11:] + '-'+str(ans[-1])
        else:
            ans = ans[0] + '-' + str(ans[-1])
        mainbin.append(ans)
    return microbin, mainbin