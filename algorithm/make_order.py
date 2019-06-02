import pandas as pd
from settings import INFO_DICT

def _main(option, id, gender):
    # return order
    df = pd.read_csv(option['COST_TABLE_FILE_PATH'], header=0)
    person_df = df[df['male_id'] == gender].reset_index(drop=True)
    order_df = person_df.sort_values(by='edge_cost', ascending=False).reset_index(drop=True)
    if gender == 0:
        # male
        order_df['female_id'].to_csv(option['ORDER_FILE_PATH'], index=False)
    else:
        # female
        order_df['male_id'].to_csv(option['ORDER_FILE_PATH'], index=False)



if __main__ == '__name__':
    _main(INFO_DICT, id, gender)
