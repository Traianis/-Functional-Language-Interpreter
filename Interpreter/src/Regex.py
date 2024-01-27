from dataclasses import dataclass
import string
import re

from .NFA import NFA

q_nr = 1


class NFA_Init:
    def __init__(self):
        self.S = set()
        self.K = set()
        self.d = dict()
        self.q0 = None
        self.F = set()


def pipe_nfa(nfa1, nfa2):
    new_nfa = NFA_Init()
    global q_nr

    new_nfa.q0 = nfa1.q0
    new_nfa.K.update(nfa1.K)
    new_nfa.d.update(nfa1.d)
    new_nfa.S.update(nfa1.S)
    new_nfa.F.update(nfa1.F)

    # Deleting q0 from nfa2
    new_nfa.d[new_nfa.q0, ''].update({x - 1 for x in nfa2.d[nfa2.q0, '']})

    # Add all states of nfa2 updated
    for i in nfa2.K:
        new_nfa.K.add(i - 1)

    for key, value in nfa2.d.items():
        if key[0] != nfa2.q0:
            new_nfa.d[key[0] - 1, key[1]] = {x - 1 for x in value}

    for i in nfa2.F:
        new_nfa.F.add(i - 1)

    new_nfa.S.update(nfa2.S)

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def random_character(c):
    new_nfa = NFA_Init()
    global q_nr
    # Create states and transitions for the character
    q1 = q_nr
    q_nr = q_nr + 1
    q2 = q_nr
    q_nr = q_nr + 1

    new_nfa.K.add(q1)
    new_nfa.K.add(q2)
    new_nfa.S.update(c)
    new_nfa.d[q1, c] = {q2}
    new_nfa.F = {q2}
    new_nfa.q0 = q1

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def upper_letters():
    new_nfa = NFA_Init()
    global q_nr
    q1 = q_nr
    q_nr = q_nr + 1
    q2 = q_nr
    q_nr = q_nr + 1

    new_nfa.K.add(q1)
    new_nfa.K.add(q2)
    upper_letter = ''.join(chr(i) for i in range(ord('A'), ord('Z') + 1))
    for c in list(upper_letter):
        new_nfa.S.update(c)
        new_nfa.d[q1, c] = {q2}
    new_nfa.F = {q2}
    new_nfa.q0 = q1

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def lower_letters():
    new_nfa = NFA_Init()
    global q_nr
    q1 = q_nr
    q_nr = q_nr + 1
    q2 = q_nr
    q_nr = q_nr + 1

    new_nfa.K.add(q1)
    new_nfa.K.add(q2)
    lower_letter = ''.join(chr(i) for i in range(ord('a'), ord('z') + 1))
    for c in list(lower_letter):
        new_nfa.S.update(c)
        new_nfa.d[q1, c] = {q2}
    new_nfa.F = {q2}
    new_nfa.q0 = q1

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def digits():
    new_nfa = NFA_Init()
    global q_nr
    # Create states and transitions for the character class
    q1 = q_nr
    q_nr = q_nr + 1
    q2 = q_nr
    q_nr = q_nr + 1

    new_nfa.K.add(q1)
    new_nfa.K.add(q2)
    digit = "0123456789"
    for c in list(digit):
        new_nfa.S.update(c)
        new_nfa.d[q1, c] = {q2}
    new_nfa.F = {q2}
    new_nfa.q0 = q1

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def question_mark(nfa):
    global q_nr
    # Create a new NFA for the question mark
    new_nfa = NFA_Init()

    # Create a new start state and connect it to the start state of nfa
    q0 = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q0)
    new_nfa.q0 = q0

    # Create a new final state
    q_final = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q_final)
    new_nfa.F = {q_final}
    new_nfa.d[q0, ''] = {nfa.q0, q_final}

    # Combine states, alphabet, and transitions
    new_nfa.K.update(nfa.K)
    new_nfa.S.update(nfa.S)
    new_nfa.d.update(nfa.d)

    # Add epsilon transitions from accept states of nfa to the new final state
    for final_state in nfa.F:
        new_nfa.d[final_state, ''] = {q_final}

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def plus(nfa):
    global q_nr
    # Create a new NFA for the plus
    new_nfa = NFA_Init()

    # Create a new start state and connect it to the start state of nfa
    q0 = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q0)
    new_nfa.d[q0, ''] = {nfa.q0}
    new_nfa.q0 = q0

    # Create a new final state
    q_final = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q_final)
    new_nfa.F = {q_final}

    # Combine states, alphabet, and transitions
    new_nfa.K.update(nfa.K)
    new_nfa.S.update(nfa.S)
    new_nfa.d.update(nfa.d)

    # Add epsilon transitions from accept states of nfa to nfa q0 and to the new final state
    for final_state in nfa.F:
        new_nfa.d[final_state, ''] = {nfa.q0, q_final}

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


def kleene_star(nfa):
    global q_nr
    # Create a new NFA for the kleene star
    new_nfa = NFA_Init()

    # Create a new start state and connect it to the start state of nfa
    q0 = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q0)
    new_nfa.q0 = q0

    # Create a new final state
    q_final = q_nr
    q_nr = q_nr + 1
    new_nfa.K.add(q_final)
    new_nfa.d[q0, ''] = {nfa.q0, q_final}
    new_nfa.F = {q_final}

    # Combine states, alphabet, and transitions
    new_nfa.K.update(nfa.K)
    new_nfa.S.update(nfa.S)
    new_nfa.d.update(nfa.d)

    # Add epsilon transitions from accept states of nfa to nfa q0 and to the new final state
    for final_state in nfa.F:
        new_nfa.d[final_state, ''] = {nfa.q0, q_final}

    return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)


class Regex:
    def thompson(self) -> NFA:
        global q_nr
        nfa = NFA_Init()
        q = q_nr
        q_nr = q_nr + 1
        nfa.q0 = q
        nfa.F = {q}
        while len(self.regex) != 0:
            # '(' regex ')'
            if self.regex[0] == '(' or self.regex[0] == ')':
                par = self.regex.pop(0)
                new_regex_string = ''
                nr = 1

                if len(self.regex) == 0:
                    new_nfa = random_character(par)
                else:
                    while True:
                        c = self.regex.pop(0)
                        if c == '(':
                            nr = nr + 1
                        elif c == ')' and nr > 1:
                            nr = nr - 1
                        elif c == ')' and nr == 1:
                            break
                        new_regex_string = new_regex_string + c

                    new_regex = Regex(list(new_regex_string))
                    new_nfa = new_regex.thompson()

                    if len(self.regex) != 0:
                        if self.regex[0] == '*':
                            self.regex.pop(0)
                            new_nfa = kleene_star(new_nfa)

                        elif self.regex[0] == '+':
                            self.regex.pop(0)
                            new_nfa = plus(new_nfa)

                        elif self.regex[0] == '?':
                            self.regex.pop(0)
                            new_nfa = question_mark(new_nfa)

                nfa = Regex.concat_nfa(nfa, new_nfa)

            # regex '|' regex
            elif self.regex[0] == '|':
                self.regex.pop(0)
                new_regex = Regex(self.regex)
                new_nfa = new_regex.thompson()

                nfa = pipe_nfa(nfa, new_nfa)

            # [---] pattern
            elif self.regex[0] == '[':
                self.regex.pop(0)
                new_nfa = "Error"

                if self.regex[0] == '0':
                    new_nfa = digits()

                if self.regex[0] == 'A':
                    new_nfa = upper_letters()

                if self.regex[0] == 'a':
                    new_nfa = lower_letters()

                self.regex.pop(0)
                self.regex.pop(0)
                self.regex.pop(0)
                self.regex.pop(0)

                if len(self.regex) != 0:
                    if self.regex[0] == '*':
                        self.regex.pop(0)
                        new_nfa = kleene_star(new_nfa)

                    elif self.regex[0] == '+':
                        self.regex.pop(0)
                        new_nfa = plus(new_nfa)

                    elif self.regex[0] == '?':
                        self.regex.pop(0)
                        new_nfa = question_mark(new_nfa)

                nfa = Regex.concat_nfa(nfa, new_nfa)

            # Special character which needs \ before
            elif self.regex[0] == '\\':
                self.regex.pop(0)

                if len(self.regex) != 0:
                    if self.regex[0] in "*+?()/| ":
                        c = self.regex.pop(0)
                        new_nfa = random_character(c)

                        if len(self.regex) != 0:
                            if self.regex[0] == '*':
                                self.regex.pop(0)
                                new_nfa = kleene_star(new_nfa)

                            elif self.regex[0] == '+':
                                self.regex.pop(0)
                                new_nfa = plus(new_nfa)

                            elif self.regex[0] == '?':
                                self.regex.pop(0)
                                new_nfa = question_mark(new_nfa)

                        nfa = Regex.concat_nfa(nfa, new_nfa)
            else:
                # Normal character
                c = self.regex.pop(0)
                new_nfa = random_character(c)

                if len(self.regex) != 0:
                    if self.regex[0] == '*':
                        self.regex.pop(0)
                        new_nfa = kleene_star(new_nfa)

                    elif c == '+' and self.regex[0] == '+':
                        self.regex.pop(0)
                        aux = random_character('+')
                        new_nfa = Regex.concat_nfa(new_nfa, aux)

                    elif self.regex[0] == '+':
                        self.regex.pop(0)
                        new_nfa = plus(new_nfa)

                    elif self.regex[0] == '?':
                        self.regex.pop(0)
                        new_nfa = question_mark(new_nfa)

                nfa = Regex.concat_nfa(nfa, new_nfa)
        return NFA(nfa.S, nfa.K, nfa.q0, nfa.d, nfa.F)

    @staticmethod
    def concat_nfa(nfa1, nfa2):
        # Concat 2 NFAs
        new_nfa = NFA_Init()

        new_nfa.q0 = nfa1.q0

        new_nfa.K.update(nfa1.K)
        new_nfa.K.update(nfa2.K)

        new_nfa.S.update(nfa1.S)
        new_nfa.S.update(nfa2.S)

        new_nfa.d.update(nfa1.d)
        new_nfa.d.update(nfa2.d)

        new_nfa.F.update(nfa2.F)

        for q in nfa1.F:
            new_nfa.d[q, ''] = {nfa2.q0}

        return NFA(new_nfa.S, new_nfa.K, new_nfa.q0, new_nfa.d, new_nfa.F)

    def __init__(self, string):
        self.regex = string


def parse_regex(regex: str) -> Regex:
    # create a Regex object by parsing the string
    i = 0
    # Delete " "
    while i < len(regex):
        if regex[i] == ' ' and regex[i - 1] != '\\':
            regex = regex[0:i] + regex[i + 1:len(regex)]
        else:
            i = i + 1

    final_regex = Regex(list(regex))

    return final_regex
    # you can define additional classes and functions to help with the parsing process

    # the checker will call this function, then the thompson method of the generated object. the resulting NFA's
    # behaviour will be checked using your implementation form stage 1
    pass
