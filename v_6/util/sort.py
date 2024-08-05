from util import parser, excel

# Global dictionary to keep track of prioritized elements per entry prototype
prioritized_elements_binary = {}
prioritized_elements_ternary = {}

def sort_formula_by_label(formula, entry_prototype):
    num_elements = parser.get_num_element(formula)
    element_label_lists = excel.get_element_label_lists(num_elements)
    sorted_formula = None

    if num_elements == 2:
        sorted_formula = sort_binary_formula_by_label(
            formula,
            entry_prototype,
            element_label_lists,
            num_elements,
        )
        listToStr = ' '.join(map(str, sorted_formula))
        print('Binary:', sorted_formula)
    elif num_elements == 3:
        sorted_formula = sort_ternary_formula_by_label(
            formula,
            element_label_lists,
            num_elements,
        )
        listToStr = ' '.join(map(str, sorted_formula))
        print('Ternary:', sorted_formula)
    return sorted_formula

def sort_binary_formula_by_label(formula, entry_prototype, element_label_lists, num_elements):
    parsed_formulas_set = [list(item) for item in parser.get_parsed_formula(formula)]
    A_list, B_list = element_label_lists

    # Initialize prioritized elements set for the entry prototype if not already done
    if entry_prototype not in prioritized_elements_binary:
        prioritized_elements_binary[entry_prototype] = set()

    for formula in parsed_formulas_set:
        parsed_element = formula[0]
        if parsed_element in A_list:
            formula.append("A")
        elif parsed_element in B_list:
            formula.append("B")
        else:
            formula.append("None")

    none_element_label_count = parser.get_none_element_label_count(parsed_formulas_set)
    is_same_element_label = parser.get_is_same_element_label(parsed_formulas_set, num_elements)

    def prioritize_element(formulas, entry_prototype):
        prioritized_set = prioritized_elements_binary[entry_prototype]
        if prioritized_set:
            prioritized_element = next(iter(prioritized_set))
            # Sort to keep prioritized element first
            return sorted(formulas, key=lambda x: (x[0] != prioritized_element, x))
        return formulas

    if none_element_label_count == 0 and not is_same_element_label:
        sorted_formulas = sorted(parsed_formulas_set, key=lambda x: x[-1])
        prioritized_elements_binary[entry_prototype].add(sorted_formulas[0][0])
        return prioritize_element(sorted_formulas, entry_prototype)

    if none_element_label_count == 1 and not is_same_element_label:
        first_formula = parsed_formulas_set[0]
        first_formula_label = first_formula[-1]
        second_formula = parsed_formulas_set[1]
        second_formula_label = second_formula[-1]

        if first_formula_label == "A" and second_formula_label == "None":
            prioritized_elements_binary[entry_prototype].add(first_formula[0])
            return prioritize_element([first_formula, second_formula], entry_prototype)
        if first_formula_label == "B" and second_formula_label == "None":
            prioritized_elements_binary[entry_prototype].add(second_formula[0])
            return prioritize_element([second_formula, first_formula], entry_prototype)
        if first_formula_label == "None" and second_formula_label == "A":
            prioritized_elements_binary[entry_prototype].add(second_formula[0])
            return prioritize_element([second_formula, first_formula], entry_prototype)
        if first_formula_label == "None" and second_formula_label == "B":
            prioritized_elements_binary[entry_prototype].add(first_formula[0])
            return prioritize_element([first_formula, second_formula], entry_prototype)

    if none_element_label_count == 2 or is_same_element_label:
        mendeleev_numbers = excel.get_mendeleev_numbers("data/element_Mendeleev_numbers.xlsx")
        sorted_formulas = sorted(parsed_formulas_set, key=lambda x: mendeleev_numbers.get(x[0], float("inf")))
        prioritized_elements_binary[entry_prototype].add(sorted_formulas[0][0])
        return prioritize_element(sorted_formulas, entry_prototype)

    return prioritize_element(parsed_formulas_set, entry_prototype)

def sort_ternary_formula_by_label(formula_tuple, element_label_lists, num_elements):
    parsed_formulas_set = [list(item) for item in parser.get_parsed_formula(formula_tuple)]
    R_list, M_list, X_list = element_label_lists

    # Initialize prioritized elements set for the entry prototype if not already done
    if formula_tuple not in prioritized_elements_ternary:
        prioritized_elements_ternary[formula_tuple] = set()

    for formula in parsed_formulas_set:
        parsed_element = formula[0]
        if parsed_element in R_list:
            formula.append("R")
        elif parsed_element in M_list:
            formula.append("M")
        elif parsed_element in X_list:
            formula.append("X")
        else:
            formula.append("None")

    none_element_label_count = parser.get_none_element_label_count(parsed_formulas_set)
    order_map = {"R": 0, "M": 1, "X": 2, "None": 3}
    is_element_same = parser.get_is_same_element_label(parsed_formulas_set, num_elements)

    def prioritize_element(formulas, formula_tuple):
        prioritized_set = prioritized_elements_ternary[formula_tuple]
        if prioritized_set:
            prioritized_element = next(iter(prioritized_set))
            # Sort to keep prioritized element second
            return sorted(formulas, key=lambda x: (x[1] != prioritized_element, x))
        return formulas

    if (none_element_label_count == 0 and not is_element_same) or none_element_label_count == 1:
        sorted_formulas_set = sorted(parsed_formulas_set, key=lambda x: order_map[x[2]])
        prioritized_elements_ternary[formula_tuple].add(sorted_formulas_set[0][1])
        return prioritize_element(sorted_formulas_set, formula_tuple)

    if none_element_label_count == 2 or is_element_same:
        mendeleev_numbers = excel.get_mendeleev_numbers("data/element_Mendeleev_numbers.xlsx")
        sorted_formulas_set = sorted(parsed_formulas_set, key=lambda x: (order_map.get(x[2], float("inf")), mendeleev_numbers.get(x[0], float("inf"))))
        prioritized_elements_ternary[formula_tuple].add(sorted_formulas_set[0][1])
        return prioritize_element(sorted_formulas_set, formula_tuple)

    if num_elements == 3 and is_element_same:
        sorted_formulas_set = sorted(parsed_formulas_set, key=lambda x: (order_map[x[2]], mendeleev_numbers.get(x[0], float("inf"))))
        return sorted_formulas_set

    if none_element_label_count == 3:
        sorted_formulas_set = sorted(parsed_formulas_set, key=lambda x: mendeleev_numbers.get(x[0], float("inf")))
        return sorted_formulas_set

    return prioritize_element(parsed_formulas_set, formula_tuple)

def sort_formulas(formulas):
    return [(formula[0], formula[1], sort_formula_by_label(formula[0], formula[1])) for formula in formulas]