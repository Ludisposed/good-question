def file_to_set(file_name):
    result = set()
    with open(file_name,'rt') as f:
        for line in f:
            result.add(line.replace('\n',''))
    return result

def set_to_file(links,file_name):
    with open(file_name,'a+') as f:
        for l in sorted(links):
            f.write(l+'\n')

def append_to_file(data, path):
    with open(path,'a+') as file:
        file.write(data)