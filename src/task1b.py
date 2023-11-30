def Unify(var, x, substitution):
    if var in substitution:
        return Unify(substitution[var], x, substitution)
    elif x in substitution:
        return Unify(var, substitution[x], substitution)
    elif isinstance(x, str) and x.islower() and x != var:
        substitution[var] = x
        return substitution
    elif isinstance(var, str) and var.islower() and var != x:
        substitution[x] = var
        return substitution
    elif isinstance(var, list) and isinstance(x, list) and len(var) == len(x):
        for v, y in zip(var, x):
            substitution = Unify(v, y, substitution)
        return substitution
    else:
        return None


def ApplySubstitution(substitution, clause):
    if substitution is None:
        return None
    return [substitution.get(term, term) for term in clause]


def Resolve(clause1, clause2):
    for literal1 in clause1:
        for literal2 in clause2:
            if literal1[0] == '~' and literal2[0] != '~':
                negated_literal1 = literal1[1:]
                unification = Unify(negated_literal1, literal2, {})
                if unification is not None:
                    resolved_clause = ApplySubstitution(
                        unification, clause1 + clause2)
                    resolved_clause.remove(literal1)
                    resolved_clause.remove(literal2)
                    return resolved_clause
            elif literal1[0] != '~' and literal2[0] == '~':
                negated_literal2 = literal2[1:]
                unification = Unify(negated_literal2, literal1, {})
                if unification is not None:
                    resolved_clause = ApplySubstitution(
                        unification, clause1 + clause2)
                    resolved_clause.remove(literal1)
                    resolved_clause.remove(literal2)
                    return resolved_clause
    return None


def ResolutionAlgorithm(clauses):
    while True:
        new_clauses = set()
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = Resolve(clauses[i], clauses[j])
                if resolvent is not None and len(resolvent) > 0:
                    if all(new_clause != tuple(resolvent) for new_clause in new_clauses):
                        new_clauses.add(tuple(resolvent))

        if not new_clauses:
            print("Теорема доведена.")
            return True

        if new_clauses.issubset(clauses):
            print("Теорема не доведена.")
            return False

        clauses.update(new_clauses)


if __name__ == "__main__":
    clauses = [
        ['P', 'a', 'x', 'f(g(y))'],
        ['P', 'z', 'f(z)', 'f(n)']
    ]
    for i in range(1, len(clauses[0])):
        unification_substitution = Unify(clauses[0][i], clauses[1][i], {})
        if unification_substitution:
            print("Уніфікація вдалася. Підстановка:", unification_substitution)
        else:
            print("Уніфікація не вдалася.")

    ResolutionAlgorithm([tuple(clause) for clause in clauses])
