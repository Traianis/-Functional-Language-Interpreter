from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file
        final_set_states = set()
        queue_state = [state]
        while len(queue_state) != 0:
            # print (queue_state)
            q = queue_state.pop(0)
            final_set_states.add(q)

            q_epsilon_states = set()
            if (q, '') in self.d:
                q_epsilon_states = self.d[q, '']
            # add the new states in queue
            for new_q in q_epsilon_states:
                if new_q not in final_set_states and new_q not in queue_state:
                    queue_state.append(new_q)
        return final_set_states
        pass

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        S_DFA = self.S
        final_set = {}
        q_set = NFA.epsilon_closure(self, self.q0)
        q_set = sorted(q_set)

        Q0_DFA = ''.join([('q' + str(x)) for x in q_set])
        K_DFA = {Q0_DFA, "sink"}
        K_DFA.add(Q0_DFA)
        K_DFA.add("sink")
        D_DFA = {}
        for c in S_DFA:
            D_DFA["sink", c] = "sink"
        F_DFA = set()
        visited_state = {}
        queue_set_state = [q_set]
        visited_state["sink"] = 1
        empty_set = []
        while queue_set_state != empty_set:
            current_set = queue_set_state.pop(0)
            current_set = sorted(current_set)
            # transform into a string
            current_string_set = ''.join([('q' + str(x)) for x in current_set])

            # Add to set of final state
            for q in current_set:
                if q in self.F:
                    F_DFA.add(current_string_set)
                    break

            # visite the state
            visited_state[current_string_set] = 1

            # Create a dictionary for this set of states
            dict_current_set = {}
            for c in S_DFA:
                dict_current_set[c] = set()

            # Complete the dictionary with states
            for q in current_set:
                for c in S_DFA:
                    if (q, c) in self.d:
                        for q_to_be_epclosed in self.d[q, c]:
                            dict_current_set[c] = dict_current_set[c] | set(
                               self.epsilon_closure(q_to_be_epclosed))

            # Add to DFA dictionary
            for c in S_DFA:
                dict_current_set[c] = sorted(dict_current_set[c])
                q_string_state = ''.join([('q' + str(x)) for x in dict_current_set[c]])
                if q_string_state == '':
                    q_string_state = "sink"
                D_DFA[current_string_set, c] = q_string_state

                # Add to queue the new state
                if q_string_state not in visited_state and dict_current_set[c] not in queue_set_state:
                    queue_set_state.append(dict_current_set[c])
                    K_DFA.add(q_string_state)

        return DFA(S_DFA, K_DFA, Q0_DFA, D_DFA, F_DFA)
        pass

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        pass

