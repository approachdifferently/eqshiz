import pandas as pd
import os
from dotenv import load_dotenv

def imp1(path):
    chars=[]
    df=pd.DataFrame()
    print('###STARTIN IMPORT###')
    inv_files = [f for f in os.listdir(path) if f.endswith('Inventory.txt')]
    for file in inv_files:
        file_path1 = os.path.join(path, file)
        file_path = file_path1.replace("\\", "/")
        tempdf = pd.read_table(file_path)
        charn = file[:-14]
        tempdf['charn'] = charn
        df = pd.concat([df, tempdf], ignore_index=True)    
        chars.append(charn)
        print('###')
    print('###IMPORT COMPLETE###')
    print('##########################')
    print('##########################')
    return df,chars