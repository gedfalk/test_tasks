import json
import argparse

from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Merging two log files into one')

    parser.add_argument(
        'log_1',
        metavar = '<LOG FILE 1>',
        type = str,
        help = 'Path to the first log file',
    )
    parser.add_argument(
        'log_2',
        metavar = '<LOG FILE 2>',
        type = str,
        help = 'Path to the second log file',
    ) 
    parser.add_argument(
        '-o', '--output',
        ###
    )
    parser.add_argument(
        'output_dir',
        metavar = '<OUTPUT DIR>',
        type = str,
        help = 'Path to the merged log',
    )   

    return parser.parse_args()  
    

def paths_checked(args):
    """
    Проверяет входные аргументы.
    
    В случае отсутствия <LOG FILE 1> или <LOG FILE 2> кидает ошибку.
    Если директория <OUTPUT DIR> не существует, то создаёт её.
    
    """

    if not (Path(args.log_1).exists() and Path(args.log_2).exists()):
        print('Wasn`t able to locate input log files. Try again')
        return False
    if not Path(args.output_dir).exists():
        Path(args.output_dir).mkdir(parents=True)
    return True


def merging_logfiles(args):
    """
    Слияние логов.

    Построчно считывает два поданых файла. С помощью модуля json получает доступ к полю timestamp и сравнивает даты.
    Результат записывает в выходной файл.

    """
    print(f"Merging <{args.log_1}> and <{args.log_2}>...")

    with open(args.log_1, 'r') as log_a, open(args.log_2, 'r') as log_b, open(args.output_dir+'/merged_log.jsonl', 'w') as log_ab:
        a = log_a.readline()
        b = log_b.readline()
        while a and b:
            a_time = datetime.strptime(json.loads(a)['timestamp'], "%Y-%m-%d %H:%M:%S")
            b_time = datetime.strptime(json.loads(b)['timestamp'], "%Y-%m-%d %H:%M:%S")

            if a_time < b_time:
                log_ab.write(a)
                a = log_a.readline()
            else:
                log_ab.write(b)
                b = log_b.readline()
        
        # После того, как один из файлов закончился, записывает остаток от второго
        if a == '':
            log_ab.write('\n' + b + log_b.read())
        else:
            log_ab.write('\n' + a + log_a.read())

    print(f".\n.\n.\nProcess completed.\nCheck <{args.output_dir}/merged_log.jsonl>")


if __name__ == '__main__':
    args = parse_args()

    if paths_checked(args):
        merging_logfiles(args)


    
