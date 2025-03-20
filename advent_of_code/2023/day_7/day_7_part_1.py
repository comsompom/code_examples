# pylint: disable=C0103
# pylint: disable=C0114
# pylint: disable=C0116
# pylint: disable=R0911
# pylint: disable=R0912
# pylint: disable=W1514
# pylint: disable=W0621
elf_file = 'elf_text_7_1.txt'
cards_strength = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
cards_list = []
current_order_rank = 1
strength_rank = 1
total_winnings = 0


def check_rank(hand_card, hand_dict):
    check_list = list(hand_dict.values())
    if len(check_list) == 5:
        cur_rank = 0
        total_rank = 0
        for x in hand_card:
            prev_rank = cur_rank
            cur_rank = cards_strength.index(x)
            if cur_rank - prev_rank == 1:
                total_rank += 1
        if total_rank == 4:
            return 1
        return 1
    if len(check_list) == 4:
        if 2 in check_list:
            return 2
    if len(check_list) == 3:
        if 2 in check_list:
            return 3
        if 3 in check_list:
            return 4
    if len(check_list) == 2:
        if 3 in check_list:
            return 5
        if 4 in check_list:
            return 6
    if len(check_list) == 1:
        return 7
    return 0


with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        one_card = []
        hand_dict = {}
        hand_card = list(line.replace('\n', '').split()[0])
        for x in hand_card:
            hand_dict[x] = hand_dict.get(x, 0) + 1
        one_card.append(hand_card)
        one_card.append(int(line.replace('\n', '').split()[1]))
        one_card.append(check_rank(hand_card, hand_dict))
        one_card.append(0)
        cards_list.append(one_card)


def get_rank_for_sort(card_rank):
    return card_rank[2] == strength_rank


def set_ordered_rank(check_list, current_order_rank):
    if len(check_list) < 1:
        return check_list, current_order_rank
    for card in check_list:
        card[0] = [cards_strength.index(x) for x in card[0]]
    check_list = sorted(check_list)
    for sub_list in check_list:
        sub_list[3] = current_order_rank
        current_order_rank += 1
    return check_list, current_order_rank


for x in range(1, 7):
    temp_list, current_order_rank = set_ordered_rank(
        list(filter(get_rank_for_sort, cards_list)), current_order_rank)
    strength_rank += 1

temp_list, current_order_rank = set_ordered_rank(
    list(filter(get_rank_for_sort, cards_list)), current_order_rank)

for x in cards_list:
    total_winnings += x[1] * x[3]

print(total_winnings)
