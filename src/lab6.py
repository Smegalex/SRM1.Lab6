from task1a import simplify_disjunctive_multiplicity
from task1b import ResolutionAlgorithm, Unify


def main():

    formula = "¬p∨(q∧s), ¬p∨s,¬s ⊢ ¬p∧q, r"
    print("Формула:", formula)
    simplify_disjunctive_multiplicity(formula)


    clauses = [
        ['P', 'a', 'x', 'f(g(y))'],
        ['P', 'z', 'f(z)', 'f(n)']
    ]

    print("\nInput clauses:")
    for clause in clauses:
        print(clause)

    unification_substitution = Unify(clauses[0][1], clauses[1][0], {})
    print("\nУніфікація:", "Уніфікація успішна." if unification_substitution else "Уніфікація не вдалася.")
    if unification_substitution:
        print("\n".join([f"{var} = {value}" for var, value in unification_substitution.items()]))


    result = ResolutionAlgorithm([tuple(clause) for clause in clauses])
    print("\nРезолюційний алгоритм:", "Теорема доведена." if result else "Теорема не доведена.")

    if __name__ == "__main__":
        main()
