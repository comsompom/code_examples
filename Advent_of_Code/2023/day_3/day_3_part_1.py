elf_file = 'elf_txt_3_1.txt'
matrix = []

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        matrix.append(line.replace('\n', '').split())

print(matrix)
