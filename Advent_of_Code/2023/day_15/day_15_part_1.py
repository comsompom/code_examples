elf_file = 'elf_text_15_1.txt'
lines_list = []
total_hash_sum = 0


with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        raw_line_list = line.replace('\n', '').split(',')
        lines_list.extend(raw_line_list)

for raw_line in lines_list:
    check = list(map((lambda x: ord(x)), [x for x in raw_line]))
    hash_val = 0
    for x in check:
        hash_val += x
        hash_val *= 17
        hash_val %= 256
    total_hash_sum += hash_val

print(f'Total: {total_hash_sum}')
