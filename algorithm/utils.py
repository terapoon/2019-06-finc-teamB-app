import numpy as np
import pandas as pd
# import MeCab
# from gensim.models import KeyedVectors
from datetime import date
from ngram import calc_relevance_vector

'''
def _get_word_vector_from_text(text, option, model):
    mt = MeCab.Tagger('')
    sum_vec = np.zeros(option['WORD_VECTOR_LEN'])
    word_count = 0
    node = mt.parseToNode(text).next
    while node:
        fields = node.feature.split(',')
        if fields[0] == '名詞' or fields[0] == '動詞' or fields[0] == '形容詞':
            sum_vec += model.wv[node.surface]
            word_count += 1
    return sum_vec / word_count
'''

def _calc_cos_of_2_texts(text1, text2, option): # ,model):
    # vector1 = _get_word_vector_from_text(text1, option, model)
    # vector2 = _get_word_vector_from_text(text2, option, model)
    # return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return calc_relevance_vector(text1, text2, option)

def _calc_cos_of_2_vectors(vector1, vector2):
    return np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

def calc_cost(male_df, female_df, info_option, cost_option):
    cost_table = []
    # load trained word2vec model
    '''
    print('loading model now ...')
    model = KeyedVectors.load_word2vec_format(info_option['MODEL_PATH'], binary=True)
    print('model is loaded!')
    '''
    for _, male_row in male_df.iterrows():
        # manually inputted info
        # male id
        male_id = male_row['id'] 
        # male age
        today = date.today()
        male_birthday = date(male_row['year'], male_row['month'], male_row['day'])
        male_time_delta = today - male_birthday
        male_age = male_time_delta.days // 365
        # male hobby
        male_hobby = male_row['hobby']
        # male introduce sentences
        male_introduce = male_row['introduce']
        # male familiarity with gym
        male_gym = male_row['gym']
        # male command of exercises
        male_intensiveness = male_row['intensiveness']

        # info from Finc Application
        # male steps (today?)
        male_steps = male_row['steps']
        # male weight 
        male_weight = male_row['weight']
        # male bmi
        male_bmi = male_row['bmi']
        # male bodyfat
        male_bodyfat = male_row['bodyfat']
        # male visfat
        male_visfat = male_row['visfat']
        # male muscle
        male_muscle = male_row['muscle']
        # male bodyage
        male_bodyage = male_row['bodyage']
        # male goal_weight
        male_goal_weight = male_row['goal_weight']
        # male goal_steps
        male_goal_steps = male_row['goal_steps'] 
        # male goal_sleep_hour
        male_goal_sleep_hour = male_row['goal_sleep-hour']
        # male goal_sleep_minute 
        male_goal_sleep_minute = male_row['goal_sleep_minute']
        for _, female_row in female_df.iterrows():
            # manually inputted info
            # female id
            female_id = female_row['id'] 
            # female age
            today = date.today()
            female_birthday = date(female_row['year'], female_row['month'], female_row['day'])
            female_time_delta = today - female_birthday
            female_age = female_time_delta.days // 365
            # female hobby
            female_hobby = female_row['hobby']
            # female introduce sentences
            female_introduce = female_row['introduce']
            # female familiarity with gym
            female_gym = female_row['gym']
            # female command of exercises
            female_intensiveness = female_row['intensiveness']

            # info from Finc Application
            # female steps (today?)
            female_steps = female_row['steps']
            # female weight 
            female_weight = female_row['weight']
            # female bmi
            female_bmi = female_row['bmi']
            # female bodyfat
            female_bodyfat = female_row['bodyfat']
            # female visfat
            female_visfat = female_row['visfat']
            # female muscle
            female_muscle = female_row['muscle']
            # female bodyage
            female_bodyage = female_row['bodyage']
            # female goal_weight
            female_goal_weight = female_row['goal_weight']
            # female goal_steps
            female_goal_steps = female_row['goal_steps'] 
            # female goal_sleep_hour
            female_goal_sleep_hour = female_row['goal_sleep-hour']
            # female goal_sleep_minute
            female_goal_sleep_minute = female_row['goal_sleep_minute']

            # female_age
            if female_age < male_age - info_option['LOWER_AGE_MARGIN'] or \
                    female_age > male_age + info_option['UPPER_AGE_MARGIN']:
                edge_cost = info_option['ERROR']
            else:
                # similarity of hobby
                hobby_relevance = _calc_cos_of_2_texts(male_hobby, female_hobby, cost_option)
                # similarity of introduce sentence
                introduce_relevance = _calc_cos_of_2_texts(male_introduce, female_introduce, cost_option)
                # similarity of basic info (age, gym, intensiveness)
                male_vector = np.array([cost_option['AGE_COST']*male_age,
                            cost_option['GYM_COST']*male_gym,
                            cost_option['INTENSIVENESS_COST']*male_intensiveness])
                female_vector = np.array([cost_option['AGE_COST']*female_age,
                            cost_option['GYM_COST']*female_gym,
                            cost_option['INTENSIVENESS_COST']*female_intensiveness])
                basic_info_relevance = _calc_cos_of_2_vectors(male_vector, female_vector)
                # similarity of manually inputted info
                manually_inputted_info_relevance = cost_option['HOBBY_COST']*hobby_relevance + \
                            cost_option['INTRODUCE_COST']*introduce_relevance + \
                            cost_option['BASIC_INFO_COST']*basic_info_relevance
                # similarity of info from Finc Application
                if (male_steps != info_option['NULL'] and female_steps != info_option['NULL']) and \
                        (male_weight != info_option['NULL'] and female_weight != info_option['NULL']) and \
                        (male_bmi != info_option['NULL'] and female_bmi != info_option['NULL']) and \
                        (male_bodyfat != info_option['NULL'] and female_bodyfat != info_option['NULL']) and \
                        (male_visfat != info_option['NULL'] and female_visfat != info_option['NULL']) and \
                        (male_muscle != info_option['NULL'] and female_muscle != info_option['NULL']) and \
                        (male_bodyage != info_option['NULL'] and female_bodyage != info_option['NULL']) and \
                        (male_goal_weight != info_option['NULL'] and female_goal_weight != info_option['NULL']) and \
                        (male_goal_steps != info_option['NULL'] and female_goal_steps != info_option['NULL']) and \
                        (male_goal_sleep_hour != info_option['NULL'] and female_goal_sleep_hour != info_option['NULL']) and \
                        (male_goal_sleep_minute != info_option['NULL'] and female_goal_sleep_minute != info_option['NULL']):
                    male_goal_sleep = male_goal_sleep_hour + male_goal_sleep_minute / 60
                    female_goal_sleep = female_goal_sleep_hour + female_goal_sleep_minute / 60
                    male_weight_gap = male_weight - male_goal_weight
                    female_weight_gap = female_weight - female_goal_weight
                    male_step_gap = male_goal_steps - male_steps
                    female_step_gap = female_goal_steps - female_steps
                    # Finc data is usable
                    if (male_bodyfat == info_option['DEFAULT'] and female_bodyfat == info_option['DEFAULT']) and \
                            (male_visfat == info_option['DEFAULT'] and female_visfat == info_option['DEFAULT']) and \
                            (male_muscle == info_option['DEFAULT'] and female_muscle == info_option['DEFAULT']) and \
                            (male_bodyage == info_option['DEFAULT'] and female_bodyage == info_option['DEFAULT']):
                        # above 4 topic is not measured
                        male_vector2 = np.array([cost_option['BMI_COST']*male_bmi,
                                    cost_option['WEIGHT_GAP_COST']*male_weight_gap,
                                    cost_option['STEPS_GAP_COST']*male_weight_gap,
                                    cost_option['GOAL_SLEEP_COST']*male_goal_sleep])
                        female_vector2 = np.array([cost_option['BMI_COST']*female_bmi,
                                    cost_option['WEIGHT_GAP_COST']*female_weight_gap,
                                    cost_option['STEPS_GAP_COST']*female_weight_gap,
                                    cost_option['GOAL_SLEEP_COST']*female_goal_sleep])
                    else:
                        male_vector2 = np.array([cost_option['BMI_COST']*male_bmi,
                                    cost_option['BODYFAT_COST']*male_bodyfat,
                                    cost_option['VISFAT_COST']*male_visfat,
                                    cost_option['MUSCLE_COST']*male_muscle,
                                    cost_option['BODYAGE_COST']*male_bodyage,
                                    cost_option['WEIGHT_GAP_COST']*male_weight_gap,
                                    cost_option['STEPS_GAP_COST']*male_weight_gap,
                                    cost_option['GOAL_SLEEP_COST']*male_goal_sleep])
                        female_vector2 = np.array([cost_option['BMI_COST']*female_bmi,
                                    cost_option['BODYFAT_COST']*female_bodyfat,
                                    cost_option['VISFAT_COST']*female_visfat,
                                    cost_option['MUSCLE_COST']*female_muscle,
                                    cost_option['BODYAGE_COST']*female_bodyage,
                                    cost_option['WEIGHT_GAP_COST']*female_weight_gap,
                                    cost_option['STEPS_GAP_COST']*female_weight_gap,
                                    cost_option['GOAL_SLEEP_COST']*female_goal_sleep])
                    finc_info_relevance = _calc_cos_of_2_vectors(male_vector2, female_vector2)
                    edge_cost = cost_option['INPUTTED_INFO_COST']*manually_inputted_info_relevance + \
                            cost_option['FINC_INFO_COST']*finc_info_relevance
                else:
                    edge_cost = manually_inputted_info_relevance
            print('add cost edge ', [male_id, female_id, edge_cost])
            cost_table.append([male_id, female_id, edge_cost])
    print('saving cost table now ...')
    return pd.DataFrame(np.array(cost_table))
