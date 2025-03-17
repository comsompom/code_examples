# pylint: disable=C0103
# pylint: disable=E0401
"""Solve day 2 problem 2"""
import copy


elf_file = 'elf_file_part2.txt'
total_power = 0
games_dict = {
    'red': 0,
    'green': 0,
    'blue': 0
}

with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        games = line.split(':')[1].split(';')
        game_power = copy.deepcopy(games_dict)
        few_power = 1
        for game in games:
            sub_game = game.split(',')
            check = {x.split()[1]: int(x.split()[0]) for x in sub_game}
            for color, val in check.items():
                if check[color] > game_power[color]:
                    game_power[color] = check[color]
        for val in game_power.values():
            few_power *= int(val)
        total_power += few_power

print(total_power)
