import subprocess
import os, sys, logging
from znakapp.celery import app

lama = []
@app.task(max_concurrency=1)
def get_active_tasks():
    count_lama = 5 #count of lamas, can be changed
    for i in range(1, count_lama+1):
        if i not in lama:
            lama.append(i)
            print(lama, " add ", i)
            return i
        
def delete_task(number):
    lama.remove(number)
    print(lama, ' delete ', number)
        
@app.task
def execute_lama(lama_number, input_link):
    base_dir = '/home/djangoapp/znakapp/service'
    python_path = sys.executable
    static_out_dir = os.path.join(base_dir, 'static', 'out', f's{lama_number}')
    mask_path = os.path.join(base_dir,'lama',f'{lama_number}','prepare_masks.py')
    lama_path = os.path.join(base_dir,'lama',f'{lama_number}','lama','bin','predict.py')
    static_parser_dir = os.path.join(base_dir, 'parsers_znakapp',f'p{lama_number}', 'images')
    static_parser_txt_dir = os.path.join(base_dir, 'parsers_znakapp',f'p{lama_number}')
    try:
        # Clear parser lib
        for f in os.listdir(static_parser_dir):
            os.remove(os.path.join(static_parser_dir, f))       
    except Exception as ex:
        print(f"Clear {lama_number}: error {ex}")
        return 0
        
    direcory_name = os.path.join(base_dir, 'parsers_znakapp', f'p{lama_number}', 'main.py')         
    try:
        subprocess.call([python_path, direcory_name, input_link])       
    except Exception as ex:
        print(f"Parser {lama_number}: error {ex}")
        return 0
    try:
        for f in os.listdir(static_out_dir):
            os.remove(os.path.join(static_out_dir, f))
        if 'krisha.kz' in input_link:
            subprocess.call([python_path, lama_path])
            print(f'Lama {lama_number}: OK')
        else:
            for img in os.listdir(static_out_dir):
                    os.rename(f'{static_parser_dir}/{img}', f'{static_out_dir}/{img}') 
        os.path.join(static_out_dir,'info_list.txt')
        os.rename(f'{static_parser_txt_dir}/info_list.txt', f'{static_out_dir}/info_list.txt')       
    except Exception as ex:
        print(f"Clear or lama {lama_number}: error {ex}")
        return 0
        
        
bot_lama = []
@app.task(max_concurrency=1)
def bot_get_active_tasks():
    bot_count_lama = 5 #count of lamas, can be changed
    for i in range(1, bot_count_lama+1):
        if i not in bot_lama:
            bot_lama.append(i)
            print(bot_lama, " add ", i)
            return i
        
def bot_delete_task(number):
    bot_lama.remove(number)
    print(bot_lama, ' delete ', number)
        
@app.task
def bot_execute_lama(lama_number, input_link):
    base_dir = 'D:\WORK\znakapp\znakapp\service'
    python_path = sys.executable
    static_out_dir = os.path.join(base_dir, 'static', 'out', f'bots{lama_number}')
    mask_path = os.path.join(base_dir,'lama',f'bot{lama_number}','prepare_masks.py')
    lama_path = os.path.join(base_dir,'lama',f'bot{lama_number}','lama','bin','predict.py')
    static_parser_dir = os.path.join(base_dir, 'parsers_znakapp',f'botp{lama_number}', 'images')
    try:
        # Clear parser lib
        for f in os.listdir(static_parser_dir):
            os.remove(os.path.join(static_parser_dir, f))  
        print("Clear ok")     
    except Exception as ex:
        print(f"Clear bot {lama_number}: error {ex}")
        return 0
        
    
    direcory_name = os.path.join(base_dir, 'parsers_znakapp', f'botp{lama_number}', 'main.py')         
    try:
        subprocess.call([python_path, direcory_name, input_link])       
    except Exception as ex:
        print(f"Parser bot {lama_number}: error {ex}")
        return 0
    try:
        for f in os.listdir(static_out_dir):
            os.remove(os.path.join(static_out_dir, f))
        if 'krisha.kz' in input_link:
            subprocess.call([python_path, mask_path])
            print(f'Mask bot {lama_number}: OK')
            subprocess.call([python_path, lama_path])
            print(f'Lama bot {lama_number}: OK')
        else:
            for img in os.listdir(static_out_dir):
                    os.rename(f'{static_parser_dir}/{img}', f'{static_out_dir}/{img}')        
    except Exception as ex:
        print(f"Clear or lama bot {lama_number}: error {ex}")
        return 0