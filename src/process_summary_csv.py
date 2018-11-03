import sys

if __name__ == "__main__":
    file_name = sys.argv[1]
    content = ''
    with open(file_name) as f:
        is_table = False
        for line in f:
            if is_table and len(line.strip()) == 0:
                break

            if line.split(',')[0].strip() == "Player Name":
                is_table = True

            if is_table:
                content += line.lstrip()
    with open(".".join(file_name.split(".")[:-1]) + "_clean.csv", 'w+') as f:
        f.write(content)