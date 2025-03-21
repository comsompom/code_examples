# pylint: disable=C0103
# pylint: disable=W1514
'''
Day 8. Part 1
'''
elf_file = 'elf_text_8_1.txt'
map_list = []
total_steps = 1
direction_step = 0

with open(elf_file) as elf_txt:
    directions = elf_txt.readline().replace(
        '\n', '').replace('L', '0').replace('R', '1')
    directions_list = list(directions)
    elf_txt.readline()
    for line in elf_txt.readlines():
        map_sublist = []
        main_point = line.replace('\n', '').replace(' ', '').split('=')[0]
        left_right = line.replace('\n', '').replace(
            ' ', '').split('=')[1].replace('(', '').replace(')', '').split(',')
        map_sublist.append(main_point)
        map_sublist.append(left_right)
        map_list.append(map_sublist)

get_finish = False
cur_map_pos = 0
cur_direction = map_list[0][0]
for idx, check_start in enumerate(map_list):
    if check_start[0] == 'AAA':
        cur_map_pos = idx
        cur_direction = map_list[idx][0]

while not get_finish:
    get_line = map_list[cur_map_pos]
    if get_line[0] == cur_direction:
        if direction_step < len(directions_list):
            cur_direction = get_line[1][int(directions_list[direction_step])]
            if cur_direction == 'ZZZ':
                print(f'STEPS: {total_steps}')
                get_finish = True
            direction_step += 1
            total_steps += 1
        else:
            direction_step = 0
        cur_map_pos += 1
    else:
        cur_map_pos += 1
    if cur_map_pos == len(map_list):
        cur_map_pos = 0
