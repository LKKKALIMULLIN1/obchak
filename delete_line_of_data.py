def delete_line(index):
    lines = open('data.txt').readlines()
    f = open("data.txt", 'w')
    for number, line in enumerate(lines):
        if number != index - 1:
            f.write(line)