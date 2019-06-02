INFO_DICT = {
    'INPUT_FILE_PATH' : './dummy.csv',
    'COST_TABLE_FILE_PATH' : './cost_table.csv',
    'ORDER_FILE_PATH' : './order.csv',
    'UPPER_AGE_MARGIN' : 5,
    'LOWER_AGE_MARGIN' : 5,
    'ERROR' : -999,
    'NULL' : -999,
    'DEFAULT' : 0
}

COST_DICT = {
    # n-gram cost
    'SYMPSON_COST' : 0.7,
    'DICE_COST' : 0.2,
    'JACCARD_COST' : 0.1,
    # inputted info cost
    'INPUTTED_INFO_COST' : 0.3,
    'AGE_COST' : 0.1,
    'GYM_COST' : 4.5,
    'INTENSIVENESS_COST' : 4.5,
    'HOBBY_COST' : 1.5,
    'INTRODUCE_COST' : 1.5,
    'BASIC_INFO_COST': 1.0,
    # finc info cost
    'FINC_INFO_COST' : 0.3,
    'BMI_COST' : 1.5,
    'BODYFAT_COST' : 0.5,
    'VISFAT_COST' : 0.5,
    'MUSCLE_COST' : 0.8,
    'BODYAGE_COST' : 1.0,
    'WEIGHT_GAP_COST' : 1.5,
    'STEPS_GAP_COST' : 0.6,
    'GOAL_SLEEP_COST': 1
}
