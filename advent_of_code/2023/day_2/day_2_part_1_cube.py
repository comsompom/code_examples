elf_file = 'elf_file_part1.txt'
total_ids = 0
games_dict = {
    'red': 12,
    'green': 13,
    'blue': 14
}
check_val = True

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        game_id = line.split(':')[0].split()[1]
        games = line.split(':')[1].split(';')
        check_val = True
        for game in games:
            sub_game = game.split(',')
            check = {x.split()[1]: int(x.split()[0]) for x in sub_game}
            for color, val in check.items():
                if check[color] > games_dict[color]:
                    check_val = False
                    break
        if check_val:
            total_ids += int(game_id)

print(total_ids)
