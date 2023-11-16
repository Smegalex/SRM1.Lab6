def divide_expression(expression: str) -> list:
    expression_result = []
    buffer = ""
    for i in range(len(expression)):
        if expression[i] == "∨" or expression[i] == "→" or expression[i] == "∧" or expression[i] == "(" or expression[i] == ")":
            if buffer != "":
                expression_result.append(buffer)
            expression_result.append(expression[i])
            buffer = ""
            continue
        buffer += expression[i]
    if buffer != "":
        expression_result.append(buffer)
    print(expression_result)
    return expression_result


def divide_by_expressions(conditions: str) -> list:
    conditions_result = []
    for i in range(len(conditions)):
        conditions[i] = conditions[i].strip()

        if not conditions[i].count("∨") and not conditions[i].count("→") and not conditions[i].count("∧"):
            conditions_result.append([conditions[i]])
            continue

        expression_start = False
        expression = ""
        buffer = ""
        for j in range(len(conditions[i])):
            if conditions[i][j] == "∨" or conditions[i][j] == "→":
                expression_start = not expression_start
                if expression_start:
                    expression += buffer
                    buffer = ""
                else:
                    expression += buffer
                    expression = divide_expression(expression)
                    if i < len(conditions_result):
                        conditions_result[i] = expression
                    else:
                        conditions_result.append(expression)
                    expression_start = True
                    expression = ""
                    buffer = ""
            buffer += conditions[i][j]
        expression += buffer
        expression = divide_expression(expression)
        if i < len(conditions_result):
            conditions_result[i] = expression
        else:
            conditions_result.append(expression)

    print(conditions)
    print(conditions_result)
    return conditions_result


def simplify_disjunctive_multiplicity(formula: str):
    if formula.count("⊢"):
        formula = formula.split("⊢")
        conditions = formula[0]
        results = formula[1]
    else:
        raise ValueError

    conditions = conditions.split(",")
    results = results.split(",")
    conditions = divide_by_expressions(conditions)
    print("\n")
    results = divide_by_expressions(results)


simplify_disjunctive_multiplicity("¬p∨(q∧s), ¬p∨s,¬s ⊢ ¬p∧q, r")

# ∨    →    ∧    ⊢
# "ValueError - '⊢' (logical assumption, turnstile) symbol is not present in the formula"
