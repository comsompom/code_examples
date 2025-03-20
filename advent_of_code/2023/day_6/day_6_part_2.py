# pylint: disable=C0114
# pylint: disable=C0103
# pylint: disable=W1514
# pylint: disable=R0801
elf_file = 'elf_text_6_2.txt'
time_list = []
dist_list = []
total_win_numbers = 1

with open(elf_file) as elf_txt:
    raw_list = []
    for line in elf_txt.readlines():
        raw_list.append(line.replace('\n', '').split(':')[1].replace(' ', '').split())
    time_list = raw_list[0]
    dist_list = raw_list[1]


for idx, time in enumerate(time_list):
    race_dict = {}
    for x in range(int(time)):
        cur_race = x * (int(time) - x)
        if cur_race > int(dist_list[idx]):
            race_dict[x] = cur_race
    total_win_numbers *= len(race_dict)

print(total_win_numbers)
