# pylint: disable=C0103
# pylint: disable=W1514
# pylint: disable=C0114
elf_file = 'elf_text_9_1.txt'
numbers_lists = []


with open(elf_file) as elf_txt:
    for line in elf_txt.readlines():
        temp_list = line.replace('\n', '').split()
        numbers_lists.append([int(x) for x in temp_list])

predict_list = []
for line_list in numbers_lists:
    sub_predict_list = []
    work_list = list(line_list)
    sub_predict_list.append(work_list)
    check_zeros = False
    while not check_zeros:
        temp_list = []
        for x in range(0, len(work_list)-1):
            if x + 1 <= len(work_list):
                temp_list.append( work_list[x + 1] - work_list[x])
        work_list = [x for x in temp_list]
        sub_predict_list.append(work_list)
        check_val = 0
        for x in work_list:
            if x == 0:
                check_val += 1
        if len(work_list) == check_val:
            check_zeros = True
    predict_list.append(sub_predict_list[::-1])

total_sum = 0
for prediction in predict_list:
    idx = 0
    predict_val = prediction[idx][-1]
    while idx < len(prediction):
        predict_val += prediction[idx][-1]
        idx += 1
    total_sum += predict_val

print(total_sum)
