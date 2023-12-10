import numpy as np

def __normalization(x, _range):
    '''
    Returns value normalized to [0;10]
    '''
    x_min, x_max, dx = _range
    return (x - x_min) / (x_max - x_min) * 10


def fuzzification(crisp_values, input_lvs):
    """
    Returns dict of terms, which were activated (P > 0)
    """
    result = {}
    for index, crisp_value in enumerate(crisp_values):
        # Normalization to [0;10]
        x = __normalization(crisp_value, input_lvs[index]['X'])
        # Get most close value to the given in Universe
        x_curr = np.argmax(input_lvs[index]['U'] >= x)
        result[index] = {}
        for term_name, term in input_lvs[index]['terms'].items():
            # Checking if P > 0
            if term['umf'][x_curr] > 0:
                # Return lower and upper bounds
                result[index][term_name] = term['lmf'][x_curr], term['umf'][x_curr]

    return result

