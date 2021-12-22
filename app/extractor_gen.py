# File for generation extractor.py from extractor_src.py

CHANNEL_LIST = "../data/channel_list.txt"
EXTRACTOR_SRC = "../app/extractor_src.py"
EXTRACTOR_DST = "../app/extractor.py"

channel_list = []
repeat_codeblock_list = []

def extractor_generator() -> None:
    '''
    Генерирует файл `extractor.py ` из файла `extractor_src.py` с необходимым количеством обработчиков новостных каналов,
    которые указаны в файле `channel_list.txt`. 
    
    Файл `extractor_src.py` менять так, чтобы была пустая строка (`\\n\\n`)
    между блоками кода, где блок - это последовательность команд, объединенных одной областью видимости (функция, цикл...)
    '''
    # считываем каналы из файла
    with open(CHANNEL_LIST) as f:
        for line in f:
            channel_list.append(line.replace("\n",""))
    # считываем основу будущего файла
    with open(EXTRACTOR_SRC) as f:
        code = f.read()
    # разбиваем файл кода список блоков и потом на два слайса, между которыми и будут вставлены обработчики каналов
    code_list = code.split("\n\n")
    for i, block in enumerate(code_list):
        if "@client" in block:
            repeat_codeblock = block
            code_list_1 = code_list[:i]
            code_list_2 = code_list[i + 1:]
    # считываем каналы новостей и генерируем для каждого свой обработчик, и все это в список
    for i in range(len(channel_list)):
        repeat_codeblock_list.append(
            repeat_codeblock.replace("channel_list[0]", f"channel_list[{i}]").replace("news_event_handler", f"news_event_handler{i+1}")
            )
    # создаем конечный файл и записываем в него по порядку все нужные блоки кода
    file = open(EXTRACTOR_DST, "w")
    for block in code_list_1:
        file.write(block + '\n\n')

    for block in repeat_codeblock_list:
        file.write(block + '\n\n')

    for block in code_list_2:
        file.write(block + '\n\n')
    file.close()

if __name__ == "__main__":
    extractor_generator()