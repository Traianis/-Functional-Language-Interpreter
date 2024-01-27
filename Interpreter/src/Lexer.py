from dataclasses import dataclass
import string
import re

from .Regex import Regex
from .NFA import NFA
from .DFA import DFA
from .Regex import NFA_Init
from .Regex import parse_regex

state_token = {}  # dict[state] = token
token_pos = {}  # dict[token] = priority
index = []  # token - last_final_state
list_token = []  # pos - token
dfa = DFA(set(), set(), 0, {}, set())


class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialisation should convert the specification to a dfa which will be used in the lex method
        global state_token
        global token_pos
        global dfa
        global index
        global list_token

        state_token = {}
        token_pos = {}
        index = []
        list_token = []
        dfa = DFA(set(), set(), 0, {}, set())

        # Creating a big NFA with all tokens
        new_nfa = NFA_Init()
        new_nfa.q0 = 0
        new_nfa.K = set()
        new_nfa.K.add(0)
        new_nfa.d[0, ''] = set()
        i = 0
        for inp in spec:
            token = inp[0]
            regex = parse_regex(inp[1])
            regex_nfa = regex.thompson()

            new_nfa.d.update(regex_nfa.d)
            new_nfa.S.update(regex_nfa.S)
            new_nfa.K.update(regex_nfa.K)
            new_nfa.F.update(regex_nfa.F)

            new_nfa.d[0, ''].add(regex_nfa.q0)

            for final in regex_nfa.F:
                state_token[final] = token

            token_pos[token] = i

            index.append(0)  # initialisation

            list_token.append(token)

            i = i + 1

        final_nfa = NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)
        #Convert it to DFA
        dfa = final_nfa.subset_construction()

        # the specification is a list of pairs (TOKEN_NAME:REGEX)
        pass

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        # this method splits the lexer into tokens based on the specification and the rules described in the lecture
        # the result is a list of tokens in the form (TOKEN_NAME:MATCHED_STRING)
        global state_token
        global token_pos
        global dfa
        global index
        global list_token

        state = dfa.q0
        i = 0
        j = 0
        line = 0
        last_new_line = -1
        final_list = []
        for k in range(len(index)):
            index[k] = -1
        val_max = -1
        ind_max = -1

        while i < len(word):
            j = i
            # Check if encountering a newline character
            while j < len(word):
                if word[j] == '\n' and last_new_line != j:
                    line = line + 1
                    last_new_line = j
                # Check if the current state is final and update the vector with final_pos of tokens
                if state in dfa.F:
                    states = map(int, filter(None, (i.strip() for i in state.split('q'))))
                    for q in states:
                        if q in state_token:
                            index[token_pos[state_token[q]]] = j
                            if j > val_max:
                                val_max = j
                                ind_max = token_pos[state_token[q]]
                            elif j == val_max and token_pos[state_token[q]] < ind_max:
                                ind_max = token_pos[state_token[q]]

                if (state, word[j]) in dfa.d:
                    state = dfa.d[(state, word[j])]
                else:
                    aux = "No viable alternative at character " + str(
                        j - last_new_line - 1) + ", line " + str(line)
                    error = [
                        ('', aux)]
                    return error

                if state == "sink":
                    # Check if encountering an acceptable token so far
                    if val_max == -1:
                        if j == len(word) - 1:
                            aux = "No viable alternative at character EOF, line " + str(line)
                        else:
                            aux = "No viable alternative at character " + str(
                                j - last_new_line - 1) + ", line " + str(line)
                        error = [
                            ('', aux)]
                        return error

                    # Add the current token to the final list
                    final_list.append((list_token[ind_max], word[i:index[ind_max]]))
                    i = index[ind_max]
                    state = dfa.q0
                    # Reset the index vector
                    for k in range(len(index)):
                        index[k] = -1
                    val_max = -1
                    ind_max = -1
                    break
                else:
                    j = j + 1
                    # Check if reaching the end of the word
                    if j == len(word):
                        if state in dfa.F:
                            states = map(int, filter(None, (i.strip() for i in state.split('q'))))
                            for q in states:
                                if q in state_token:
                                    index[token_pos[state_token[q]]] = j
                                    if j > val_max:
                                        val_max = j
                                        ind_max = token_pos[state_token[q]]
                                    elif j == val_max and token_pos[state_token[q]] < ind_max:
                                        ind_max = token_pos[state_token[q]]

                        # Check if encountering an acceptable token so far
                        if val_max == -1:
                            aux = "No viable alternative at character EOF, line " + str(line)
                            error = [
                                ('', aux)]
                            return error

                        final_list.append((list_token[ind_max], word[i:index[ind_max]]))
                        i = index[ind_max]

                        if i == len(word):
                            break

                        state = dfa.q0

                        for k in range(len(index)):
                            index[k] = -1
                        val_max = -1
                        ind_max = -1
        return final_list
        pass
