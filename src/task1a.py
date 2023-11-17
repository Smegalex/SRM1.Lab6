def divide_expression(expression: str) -> list:
    expression = simplify_implication(expression)
    expression = simplify_negation(expression)
    expression_result = []
    buffer = ""
    for i in range(len(expression)):
        if expression[i] == "∨" or expression[i] == "→" or expression[i] == "∧" or expression[i] == "(" or expression[i] == ")" or (expression[i] == "¬" and expression[i+1] == "("):
            if buffer != "":
                expression_result.append(buffer)
            expression_result.append(expression[i])
            buffer = ""
            continue
        buffer += expression[i]
    if buffer != "":
        expression_result.append(buffer)

    expression_result = open_brackets(expression_result)
    return expression_result


def divide_by_expressions(conditions: str) -> list:
    conditions_result = []
    for i in range(len(conditions)):
        conditions[i] = conditions[i].strip()

        if not conditions[i].count("∨") and not conditions[i].count("→") and not conditions[i].count("∧"):
            conditions_result.append([conditions[i]])
            continue

        condition_buffer = ""
        expression_start = False
        bracket_start = False
        expression = ""
        bracket_expression = ""
        buffer = ""
        for j in range(len(conditions[i])):
            if (conditions[i][j] == "∨" or conditions[i][j] == "→") and not bracket_start:
                expression_start = not expression_start
                if expression_start:
                    expression += buffer
                    buffer = ""
                else:
                    expression += buffer
                    condition_buffer += expression
                    expression_start = True
                    expression = ""
                    buffer = ""
            if conditions[i][j] == "(" or conditions[i][j] == ")":
                bracket_start = not bracket_start
                if bracket_start:
                    bracket_expression += buffer
                    buffer = ""
                else:
                    bracket_expression += buffer + ")"
                    if expression != "":
                        condition_buffer += expression
                        expression = ""
                    condition_buffer += bracket_expression
                    bracket_expression = ""
                    buffer = ""
                    continue

            buffer += conditions[i][j]
        expression += buffer
        condition_buffer += expression
        condition_buffer = divide_expression(condition_buffer)
        conditions_result.append(condition_buffer)

    return conditions_result


def simplify_implication(expression: str) -> str:
    expression_result = expression
    # remove '→' (implication)
    brackets = False
    if len(expression) < 3:
        return expression_result
    if expression.count("→"):
        if expression[0] == "(" and expression[-1] == ")":
            expression = expression.translate({ord(i): None for i in "()"})
            brackets = True

        expression = expression.replace(" ", "")
        ind = expression.index("→")
        expression = [expression[:ind]] + [expression[ind+1:]]

        expression[0] = "¬" + expression[0]
        expression[1] = simplify_implication(expression[1])
        expression_result = expression[0] + "∨" + expression[1]

        if brackets:
            expression_result = "(" + expression_result + ")"
    return expression_result


def simplify_negation(expression: str) -> str:
    # remove extra '¬' (negation)
    logic_negation_count = 0
    expression_result = ""
    for i in range(len(expression)):
        if expression[i] == "¬":
            logic_negation_count += 1
            continue
        if not (logic_negation_count % 2 == 0) and logic_negation_count != 0:
            expression_result += "¬"
        logic_negation_count = 0

        expression_result += expression[i]

    return expression_result


def open_brackets(expression: list) -> list:
    expression_result = expression

    if expression.count("("):
        expression_result = []
        for i in range(len(expression)):
            if expression[i] == "(" and i > 0 and i+2 < len(expression):
                if expression[i-1] == "¬":
                    expression_result = negation_brackets(expression, i-1)
                    expression_result = open_brackets(expression_result)
                if expression[i-1] == expression[i+2] and (expression[i-1] == "∨" or expression[i-1] == "∧"):
                    expression_result = ' '.join(expression).translate(
                        {ord(i): None for i in "()"}).split()
                    expression_result = open_brackets(expression_result)
                if expression[i-1] == "∧" and expression[i+2] == "∨":
                    expression_result = concat_brackets(expression, i-1)
                    expression_result = open_brackets(expression_result)
                if expression[i-1] == "∨" and expression[i+2] == "∧":
                    if expression_result == []:
                        expression_result = expression
                    break
            elif expression[0] == "(" and expression[-1] == ")":
                expression_result = ' '.join(expression).translate(
                    {ord(i): None for i in "()"}).split()
                expression_result = open_brackets(expression_result)
            elif expression[i] == ")" and i < len(expression)-1:
                if expression_result.count(")") or expression_result == []:
                    end = expression[i+1:]
                    end.reverse()
                    expression_result = end + expression[:i+1]
                    expression_result = open_brackets(expression_result)
    return expression_result


def concat_brackets(expression: list, start_index: int) -> list:
    expression_result = []
    for i in range(start_index-1):
        expression_result.append(expression[i])

    buffer = ""
    end_index = 0
    for i in range(start_index+2, len(expression)):
        if expression[i] == ")":
            end_index = i+1
            break
        elif expression[i] == "∨":
            buffer += "∨"
        else:
            buffer += "(" + expression(start_index-1) + \
                "∧" + expression[i] + ")"
    for i in range(end_index, len(expression)):
        expression_result.append(expression[i])

    return expression_result


def negation_brackets(expression: list, start_index: int) -> list:
    expression_result = []
    for i in range(start_index):
        expression_result.append(expression[i])

    buffer = ""
    end_index = 0
    for i in range(start_index+2, len(expression)):
        if expression[i] == ")":
            end_index = i+1
            break
        elif expression[i] == "∧":
            buffer += "∨"
        elif expression[i] == "∨":
            buffer += "∧"
        else:
            buffer += "¬" + expression[i]
    buffer = divide_expression(buffer)
    if len(buffer) > 1:
        expression_result += ["("] + buffer + [")"]
        expression_result = open_brackets(expression_result)
    else:
        expression_result += buffer

    for i in range(end_index, len(expression)):
        expression_result.append(expression[i])

    return expression_result


def close_bracketed(expression: list) -> list:
    expression_result = []
    bracketed_start = False
    bracketed_expr = ""
    for i in range(len(expression)):
        if expression[i] == "(":
            bracketed_start = True

        if expression[i] == ")":
            bracketed_start = False
            expression_result.append(bracketed_expr+")")
            bracketed_expr = ""
            continue

        if bracketed_start:
            bracketed_expr += expression[i]
            continue

        expression_result.append(expression[i])
    return expression_result


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
    results = divide_by_expressions(results)

    for i in range(len(conditions)):
        conditions[i] = close_bracketed(conditions[i])
    for j in range(len(results)):
        results[j] = divide_expression(results[j])
        results[j] = open_brackets(["¬"]+["("]+results[j]+[")"])
        results[j] = close_bracketed(results[j])

    disjunctive_multiplicity = conditions + results
    return disjunctive_multiplicity


def ResolutionMethod(disjunctive_multiplicity: list):

    resulting_multiplicity = disjunctive_multiplicity
    buffer = ""
    match = False
    literal = ""
    for i in disjunctive_multiplicity:
        for j in range(len(i)):
            if i[j] != "∨":
                literal = simplify_negation("¬"+i[j])
                buffer = resulting_multiplicity.copy()
                for k in range(len(resulting_multiplicity)):
                    if resulting_multiplicity[k].count(literal):
                        buffer.pop(k)
                        match = True
                if match and buffer.count(i[j]):
                    buffer.remove(i[j])
                resulting_multiplicity = buffer
    return resulting_multiplicity


def is_true_logical_statement(statement: str) -> bool:
    try:
        disjunctive_multiplicity = simplify_disjunctive_multiplicity(statement)
    except ValueError:
        print("ValueError - '⊢' (logical assumption, turnstile) symbol is not present in the formula")

    resulting_multiplicity = ResolutionMethod(disjunctive_multiplicity)

    if resulting_multiplicity == []:
        return True
    else:
        return False


# simplify_disjunctive_multiplicity("p→(r →q),(q∧s)→t, ¬h  → (s∧¬t) ⊢ p→(r →h)")
# ∨    →    ∧    ⊢      ¬
# "ValueError - '⊢' (logical assumption, turnstile) symbol is not present in the formula"
