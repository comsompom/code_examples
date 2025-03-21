# pylint: disable=E0401
# pylint: disable=C0103
# pylint: disable=W1514
"""script to solve day 1 problem 1"""
import re


elf_file = 'elf_text_part1.txt'
calibration_val = 0

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        first_num = int(re.search(r'\d+', line).group(0)[0]) * 10
        last_num = int(re.search(r'\d+', line[::-1]).group(0)[0])
        full_num = first_num + last_num
        calibration_val += full_num

print(calibration_val)
