import numpy as np
import t1_membership_functions
import itertools
import t2_fuzzifier
import t2_fuzzy_operators
import t2_type_reducer
import t1_defuzzifier
import t2_similarity_measure


def preprocessing(input_lvs, output_lv):
    '''
    Creates the Universe (U) and MFs (input and output)
    '''

    # Creation of the Universe [0;10]
    for item in input_lvs:
        item['U'] = np.arange(0, 10, 0.01)
    output_lv['U'] = np.arange(0, 10, 0.01)

    # Creation of the input MFs
    for lv in input_lvs:
        for term in lv['terms'].values():
            umf_type, *umf_params = term['umf']
            lmf_type, *lmf_params = term['lmf']
            term['range'] = (min(umf_params), max(umf_params))
            term['umf'] = getattr(t1_membership_functions, umf_type)(lv['U'], *umf_params)
            term['lmf'] = getattr(t1_membership_functions, lmf_type)(lv['U'], *lmf_params)

    # Creation of the output MFs
    for term in output_lv['terms'].values():
        umf_type, *umf_params = term['umf']
        lmf_type, *lmf_params = term['lmf']
        term['range'] = (min(umf_params), max(umf_params))
        term['umf'] = getattr(t1_membership_functions, umf_type)(output_lv['U'], *umf_params)
        term['lmf'] = getattr(t1_membership_functions, lmf_type)(output_lv['U'], *lmf_params)


def activated_rules(fuzzy_values, rule_base):
    '''
    Returns ativated rules
    '''
    terms = (item.keys() for item in fuzzy_values.values())
    antecedents = tuple(itertools.product(*terms))
    return [rule for rule in rule_base if rule[0] in antecedents]


def implication(fuzzy_values, activated_rules, output_lv):
    '''
    Returns final MFs
    '''
    result = []
    for rule in activated_rules:
        antecedent, consequent = rule
        mfs = [fuzzy_values[index][term] for index, term in enumerate(antecedent)]
        lmf = [lmf for lmf, umf in mfs]
        umf = [umf for lmf, umf in mfs]
        tmp = t2_fuzzy_operators.t2_fuzzy_min(output_lv['terms'][consequent], min(lmf), min(umf))
        result.append(tmp)
    return result


def aggregation(*fuzzy_sets):
    '''
    Aggregate final MFs
    '''
    return t2_fuzzy_operators.t2_fuzzy_union(*fuzzy_sets)


def process(input_lvs, output_lv, rule_base, crisp_values):
    '''
    Returns overall output: ((defuzzified value, term), final MF)
    '''

    # Get probabilities of terms
    fuzzy_values = t2_fuzzifier.fuzzification(crisp_values, input_lvs)
    # Get corresponding rules
    rules = activated_rules(fuzzy_values, rule_base)
    # Apply fuzzy implization
    implication_fuzzy_sets = implication(fuzzy_values, rules, output_lv)
    # Apply fuzzy aggregation
    result_fuzzy_set = aggregation(*implication_fuzzy_sets)
    # From type-2 to type-1 MF
    t1_fs = t2_type_reducer.EKM(output_lv['U'], *result_fuzzy_set)
    # Get resulting defuzzified value
    crisp_result = t1_defuzzifier.defuzzification(output_lv['U'], t1_fs, 'mom')

    # Jaccard measure to find the most similar word
    word_result = []
    for term, fou in output_lv['terms'].items():
        sm = t2_similarity_measure.jaccard_measure({'lmf': result_fuzzy_set[0],
                                                    'umf': result_fuzzy_set[1]},
                                                   fou)
        word_result.append((term, sm))
    word_result = max(word_result, key=lambda item: item[1])
    
    return (crisp_result, word_result[0]), result_fuzzy_set

