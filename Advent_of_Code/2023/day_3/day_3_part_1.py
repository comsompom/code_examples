'''
TBD Check matrix list for symbol, add num to list, sum list
'''
import numpy as np
import re


elf_file = 'elf_txt_3_1.txt'
matrix_symbols = []
matrix_symbols_pos = []
matrix_raw = []
matrix_base = []
numbers_list = []
total_sum = 0

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        cur_line = line.replace('\n', '').replace('.', ' ')
        sub_list = [re.sub(r'[^0-9]', '', x) for x in cur_line.split() if len(re.sub(r'[^0-9]', '', x)) > 0]
        matrix_symbols.append(sub_list)
        cur_list = [x for x in cur_line]
        matrix_raw.append(line.replace('\n', '').replace('.', '_').split())
        matrix_base.append(cur_list)
    for idx, element in enumerate(matrix_raw):
        sub_list = []
        for x in matrix_symbols[idx]:
            tmp_list = []
            check = element[0].find(x)
            tmp_list.append(check)
            tmp_list.append(check + len(x) - 1)
            sub_list.append(tmp_list)
        matrix_symbols_pos.append(sub_list)


print(matrix_symbols)    # nums for checking
print(matrix_symbols_pos)   # pos nums for checking

matrix_main = np.array(matrix_base)
raws_num = len(matrix_symbols)
print(matrix_main)

for idx, sub_list_string in enumerate(matrix_symbols_pos):
    if len(sub_list_string) > 0:
        for idy, idx_num in enumerate(sub_list_string):
            if raws_num > idx > 0:
                col_b = idx - 1
                col_e = 3
            else:
                col_b = idx
                col_e = 2
            if idx_num[0] > 0:
                raw_b = idx_num[0] - 1
            else:
                raw_b = idx_num[0]
            check_number = matrix_symbols[idx][idy]
            check_matrix = matrix_main[col_b:(col_b + col_e), raw_b:idx_num[1]+2]
            check_matrix_list = check_matrix.tolist()
            check_str = ''
            for sub_chm in check_matrix_list:
                check_str += ''.join([i for i in sub_chm if not i.isdigit()]).replace(' ', '')
            if len(check_str) > 0:
                total_sum += int(check_number)


print(total_sum)
