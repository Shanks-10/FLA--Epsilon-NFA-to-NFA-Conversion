def epsilon_closure(states, epsilon_transitions):
    closure = set(states)
    queue = list(states)

    while queue:
        current_state = queue.pop()
        epsilon_neighbors = epsilon_transitions.get(current_state, set())
        new_states = epsilon_neighbors - closure
        closure.update(new_states)
        queue.extend(new_states)

    return closure

def epsilon_nfa_to_nfa(epsilon_nfa):
    nfa = {"states": set(), "alphabet": set(), "transitions": {}}
    epsilon_transitions = epsilon_nfa.get("epsilon_transitions", {})

    for state in epsilon_nfa["states"]:
        closure = epsilon_closure({state}, epsilon_transitions)
        nfa["states"].add(tuple(closure))

    nfa["alphabet"] = epsilon_nfa["alphabet"]

    for state_set in nfa["states"]:
        for symbol in nfa["alphabet"]:
            next_states = set()
            for state in state_set:
                epsilon_neighbors = epsilon_transitions.get(state, set())
                next_states.update(epsilon_closure(epsilon_neighbors, epsilon_transitions))
            if next_states:
                nfa["transitions"][(state_set, symbol)] = tuple(next_states)

    return nfa

def main():
    epsilon_nfa = {
        "states": set(input("Enter epsilon NFA states (comma-separated): ").split(',')),
        "alphabet": set(input("Enter alphabet symbols (comma-separated): ").split(',')),
        "epsilon_transitions": {}
    }

    epsilon_transitions_input = input("Enter epsilon transitions (e.g., q0,q1;q1,q2): ")
    for transition in epsilon_transitions_input.split(';'):
        source, destinations = transition.split(',')
        epsilon_nfa["epsilon_transitions"][source] = set(destinations.split(','))

    nfa_result = epsilon_nfa_to_nfa(epsilon_nfa)
    
    print("\nNFA:")
    print(nfa_result)

main()
