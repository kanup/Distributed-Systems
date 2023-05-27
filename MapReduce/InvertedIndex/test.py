import os

files = []
input_dir = 'input'
for filename in os.listdir(input_dir):
    if filename.startswith("input"):
        files.append(filename)

l = len(files)

div = l // 2
rem = l % 2

mapper_splits = []
i = 0
while i < l:
    path = ''
    size = div
    if rem > 0:
        size += 1
        rem -= 1
    for j in range(0, size):
        path += files[i+j] + ','
    path = path[:-1]
    mapper_splits.append(path)
    i += size

print(mapper_splits)