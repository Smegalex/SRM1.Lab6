from task1a import is_true_logical_statement, simplify_disjunctive_multiplicity
from task1b import ResolutionAlgorithm, Unify


if __name__ == "__main__":

    task1a_variant1 = "¬p∨q, ¬p∨s,¬s ⊢ ¬p"
    task1a_variant19 = "p→r, q→s, r → t, s→h, t → ¬h, p → q ⊢ ¬p"
    task1a_variant25 = "p→q, q→r, p→s, s→t, t→h, ¬(r∧h) ⊢¬p"
    task1a_variants = {1: task1a_variant1,
                       19: task1a_variant19, 25: task1a_variant25}

    task1a_imaginative = "¬¬p∨¬(q∨s), ¬p∨s,¬s ⊢ ¬p∧q, r"
    task1a_variant20 = "p→(r →q),(q∧s)→t, ¬h  → (s∧¬t) ⊢ p→(r →h)"
    task1a_variant24 = "¬p, r, q → p, s → (r∨q), (t∨h) → s ⊢ t"
    task1a_bonuses = {"придуманий": task1a_imaginative,
                      20: task1a_variant20, 24: task1a_variant24}

    for key, item in task1a_bonuses.items():
        print(f"Варіант {key}:\n{item}")
        if is_true_logical_statement(item):
            print("Логічне припущення є істинне.")
        else:
            print("Логічне припущення не є істинним.")
        print(
            f"Множина диз'юнктивів для формули, поданої вище:\n{simplify_disjunctive_multiplicity(item)}")
        print("\n\n")

    """clauses = [
        ['P', 'a', 'x', 'f(g(y))'],
        ['P', 'z', 'f(z)', 'f(n)']
    ]

    print("\nInput clauses:")
    for clause in clauses:
        print(clause)

    unification_substitution = Unify(clauses[0][1], clauses[1][0], {})
    print("\nУніфікація:",
          "Уніфікація успішна." if unification_substitution else "Уніфікація не вдалася.")
    if unification_substitution:
        print("\n".join([f"{var} = {value}" for var,
              value in unification_substitution.items()]))

    result = ResolutionAlgorithm([tuple(clause) for clause in clauses])
    print("\nРезолюційний алгоритм:",
          "Теорема доведена." if result else "Теорема не доведена.")
"""
