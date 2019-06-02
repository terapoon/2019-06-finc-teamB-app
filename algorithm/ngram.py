def _dice_coefficient(list_a,list_b):
    set_intersection = set.intersection(set(list_a), set(list_b))
    num_intersection = len(set_intersection)
    num_listA = len(list_a)
    num_listB = len(list_b)
    return_value = float(2.0 * num_intersection) / (num_listA + num_listB)
    return return_value

def _sympson_coefficient(list_a,list_b):
    set_intersection = set.intersection(set(list_a), set(list_b))
    num_intersection = len(set_intersection)
    num_listA = len(list_a)
    num_listB = len(list_b)
    return_value = float(num_intersection) / min([num_listA,num_listB])
    return return_value

def _jaccard_coefficient(list_a, list_b):    
    set_intersection = set.intersection(set(list_a), set(list_b))
    num_intersection = len(set_intersection)
    set_union = set.union(set(list_a), set(list_b))
    num_union = len(set_union)
    return_value = float(num_intersection) / num_union
    return return_value

def calc_relevance_vector(word1, word2, option):
    word1_len = len(word1)
    word2_len = len(word2)
    word1_features = []
    word2_features = []
    if word1_len==1:
        word1_features.append("$$"+word1)
        word1_features.append("$"+word1+"$")
        word1_features.append(word1+"$$")
    elif word1_len==2:
        word1_features.append("$$"+word1[0])
        word1_features.append("$"+word1)
        word1_features.append(word1+"$")
        word1_features.append(word1[1]+"$$")
    else:
        word1_features.append("$$"+word1[0])
        word1_features.append("$"+word1[:2])
        for i in range(word1_len-2):
            word1_features.append(word1[i:i+3])
            word1_features.append(word1[-2:]+"$")
            word1_features.append(word1[-1:]+"$$")

    if word2_len==1:
        word2_features.append("$$"+word2)
        word2_features.append("$"+word2+"$")
        word2_features.append(word2+"$$")
    elif word2_len==2:
        word2_features.append("$$"+word2[0])
        word2_features.append("$"+word2)
        word2_features.append(word2+"$")
        word2_features.append(word2[1]+"$$")
    else:
        word2_features.append("$$"+word2[0])
        word2_features.append("$"+word2[:2])
        for i in range(word2_len-2):
            word2_features.append(word2[i:i+3])
            word2_features.append(word2[-2:]+"$")
            word2_features.append(word2[-1:]+"$$")
            
    sympson = _sympson_coefficient(word1_features, word2_features)
    dice = _dice_coefficient(word1_features, word2_features)
    jaccard = _jaccard_coefficient(word1_features, word2_features)

    return option['SYMPSON_COST']*sympson + \
            option['DICE_COST']*dice + \
            option['JACCARD_COST']*jaccard
