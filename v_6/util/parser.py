import re

def get_parsed_formula(formula):
    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    matches = re.findall(pattern, formula)
    parsed_formula = []
    for element, index in matches:
        index = float(index) if index else 1
        parsed_formula.append((element, index))
    return parsed_formula

def get_num_element(formula):
    elements = get_parsed_formula(formula)
    return len(elements)

def separate_formulas(compounds):
    binary_formulas = []
    ternary_formulas = []
    skipped_formulas = []

    for compound in compounds:
        formula = compound['Formula']
        entry_prototype = compound['Entry prototype']
        parsed_formula = get_parsed_formula(formula)
        elements = [element for element, _ in parsed_formula]

        if len(elements) == 2:
            binary_formulas.append((formula, entry_prototype, parsed_formula))
        elif len(elements) == 3:
            ternary_formulas.append((formula, entry_prototype, parsed_formula))
        else:
            skipped_formulas.append(formula)

    return binary_formulas, ternary_formulas, skipped_formulas

def get_none_element_label_count(
    parsed_formula_set,
):
    none_element_label_count = 0
    for formula in parsed_formula_set:
        element_label = formula[-1]

        if element_label == "None":
            none_element_label_count += 1
    return none_element_label_count


def get_is_same_element_label(parsed_formula_set, num_elements):
    labels = [item[2] for item in parsed_formula_set if item[2]]

    if num_elements == 2:
        if labels[0] == labels[1]:
            return True

    if num_elements == 3:
        labels = [item[2] for item in parsed_formula_set if item[2]]
        if labels[0] == labels[1] and labels[0] == labels[2]:
            return True

    return False