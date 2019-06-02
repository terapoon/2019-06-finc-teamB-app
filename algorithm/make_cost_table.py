import pandas as pd
from utils import calc_cost
from settings import INFO_DICT
from settings import COST_DICT


def _main(info_option, cost_option):
    # TODO: load data from database here!!
    # now import dummy.csv from current directory.
    df = pd.read_csv(info_option['INPUT_FILE_PATH'], header=0).fillna(info_option['NULL'])
    male_df = df[df['gender'] == 0].reset_index(drop=True)
    female_df = df[df['gender'] == 1].reset_index(drop=True)
    cost_table_df = calc_cost(male_df, female_df, info_option, cost_option)
    cost_table_df.columns = ['male_id', 'female_id', 'edge_cost']
    cost_table_df.to_csv(info_option['COST_TABLE_FILE_PATH'], index=False)
    
if __name__ == '__main__':
    _main(INFO_DICT, COST_DICT)
