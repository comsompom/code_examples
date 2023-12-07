'''
TBD Not Solved yet
'''
elf_file = 'elf_txt_3_1.txt'
matrix_symbols = []
matrix_raw = []

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        matrix_symbols.append(line.replace('\n', '').replace('.', ' ').split())
        matrix_raw.append(line.replace('\n', '').replace('.', '_').split())
    for idx, element in enumerate(matrix_raw):
        for x in matrix_symbols[idx]:
            check = element[0].find(x)
            print(f'el_beg: {check}  el_end: {check + len(x) - 1}  curr_idx: {idx}')


print(matrix_symbols)
print(matrix_raw)
