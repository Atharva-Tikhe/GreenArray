from webapp.match_in_db import MatchWithDb
import logging
from datetime import datetime
now = datetime.now()

# logging.basicConfig(format='%(asctime)s %(message)s')
logging.basicConfig(filename=f'{now.strftime("%d_%m_%Y_%H")}_logs.log' , filemode='a', format='%(asctime)s %(message)s', level=logging.INFO)

sample_matrix = './assets/sample-matrix.tsv'

logging.info(f'Processing sample matrix: {sample_matrix}')

with open('./assets/sample-matrix.tsv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        filename, gender = line.strip().split('\t')
        if gender == "Male" or gender == 'M':
            obj = MatchWithDb('webapp/processed_56878_v1-full_wc.tsv', f'assets/inputs/{filename}', 'M')
            if obj.get_confirmation() == True:
                logging.info(f'{filename} processed')
            else:
                logging.error(f'{filename} was not processed, check server callback')
        elif gender == "Female" or gender == 'F':
            obj = MatchWithDb('webapp/processed_56878_v1-full_wc.tsv', f'assets/inputs/{filename}', 'F')
            if obj.get_confirmation():
                logging.info(f'{filename} processed')
            else:
                logging.error(f'{filename} was not processed, check server callback')
        else:
            raise ValueError(f"Gender '{gender}' is not recognized")
