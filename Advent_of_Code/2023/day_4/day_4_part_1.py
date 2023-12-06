elf_file = 'elf_text_4_1.txt'
total_wins = 0


with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        two_cards = line.replace('\n', '').split(':')[1]
        win_numbers = set(two_cards.split('|')[0].split())
        have_numbers = set(two_cards.split('|')[1].split())
        have_win_numbers = len(win_numbers.intersection(have_numbers))
        if have_win_numbers > 0:
            have_win_numbers -= 1
            total_wins += 2 ** have_win_numbers

print(total_wins)
