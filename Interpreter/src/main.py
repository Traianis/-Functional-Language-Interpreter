from sys import argv
from src.Lexer import Lexer


def create_new_input(i, inp):
    k = 1
    new_input = [inp[i]]
    i = i + 1
    while i < len(inp) - 1:
        new_input.append(inp[i])
        if inp[i][0] == ')':
            k = k - 1
            if k == 0:
                break
        if inp[i][0] == '(':
            k = k + 1
        i = i + 1
    return i, new_input


def rec(inp):
    final_list = []
    if inp[0][0] == '(' and inp[1][0] == ')':
        return None
    # ( something )
    if inp[0][0] == '(':

        # ( + list )
        if inp[1][0] == "add":
            # + num
            if inp[2][0] == "num":
                final_list.append(inp[2][1])
                return final_list
            # + ( something )
            elif inp[2][0] == '(':
                new_input = inp[2:len(inp) - 1]
                summat = 0
                result = rec(new_input)

                while result is not None and type(result[0]) is tuple:
                    result = rec(result)

                if result == "ERROR":
                    return "ERROR"

                for c in result:
                    if c != '(' and c != ')':
                        summat = summat + int(c)

                return [str(summat)]

            # Syntax ERROR
            return "ERROR"


        # ( ++ something )
        elif inp[1][0] == "concat":
            if inp[2][0] == '(':
                final_list.append("(")
                i = 3
                while i < len(inp) - 1 and inp[i][0] != ')':
                    # Num
                    if inp[i][0] == "num":
                        final_list.append(inp[i][1])
                    # '(' something ')'
                    if inp[i][0] == '(':
                        i, new_input = create_new_input(i, inp)

                        # Repel the function
                        result = rec(new_input)

                        while result is not None and type(result[0]) is tuple:
                            result = rec(result)

                        if result == "ERROR":
                            return "ERROR"

                        if result is not None:
                            # delete '(' and ')'
                            result = result[1:len(result) - 1]
                            final_list.extend(result)

                    i = i + 1
                final_list.append(")")
                return final_list

            # Syntax ERROR
            return "ERROR"

        # lambda
        elif inp[1][0] == "lambda":
            i = len(inp) - 2

            # Find the input
            aux = inp[0]
            if inp[i][0] == "add" or inp[i][0] == "concat":
                aux = inp[i]
            elif inp[i][0] == "num":
                # form (l x: x l y: 1)
                if inp[i - 1][0] == "lambda":
                    while inp[i - 1][0] == "lambda":
                        i = i - 1

                aux = inp[i:len(inp) - 1]
            elif inp[i][0] == ")":
                k = 1
                while k:
                    i = i - 1
                    if inp[i][0] == "(":
                        k = k - 1
                    if inp[i][0] == ")":
                        k = k + 1

                # inp[i] == '('
                # form (l x: x l y: (y))
                if inp[i - 1][0] == "lambda":
                    while inp[i - 1][0] == "lambda":
                        i = i - 1

                aux = inp[i:len(inp) - 1]
            elif inp[i][0] == "id":
                while inp[i - 1][0] == "lambda":
                    i = i - 1
                aux = inp[i:len(inp) - 1]

            # Input found
            ok = 1
            j = 2
            l_id = inp[1][1][7:len(inp[1][1]) - 1]
            while inp[j][0] == "lambda":
                l_aux_id = inp[j][1][7:len(inp[j][1]) - 1]
                if l_id == l_aux_id:
                    ok = 0
                final_list.append(inp[j])
                j = j + 1
            while j < i:
                if inp[j][0] == "id" and inp[j][1] == l_id and ok:
                    final_list.extend(aux)
                else:
                    final_list.append(inp[j])
                j = j + 1

            return final_list

        # Just a list '(' num something ')'
        elif inp[1][0] == "num":
            final_list.append("(")

            i = 1
            while i < len(inp) - 1:
                if inp[i][0] == "num":
                    final_list.append(inp[i][1])

                if inp[i][0] == "(":
                    i, new_input = create_new_input(i, inp)

                    # Repel the function
                    result = rec(new_input)

                    while result is not None and type(result[0]) is tuple:
                        result = rec(result)

                    if result == "ERROR":
                        return "ERROR"

                    if result is None:
                        result = "()"

                    final_list.extend(result)

                i = i + 1

            final_list.append(")")
            return final_list



        # '(' ( something ) something )
        elif inp[1][0] == "(":
            i, new_input = create_new_input(1, inp)

            i = i + 1

            # Repel the function
            result = rec(new_input)

            if result == "ERROR":
                return "ERROR"

            # Check if it was a lambda function
            if result is None:
                result = "()"
            elif type(result[0]) is tuple:
                new_input = [inp[0]]
                new_input.extend(result)
                new_input.extend(inp[i:len(inp)])
                new_result = rec(new_input)
                return new_result

            final_list.append('(')
            final_list.extend(result)

            while i < len(inp) - 1:
                if inp[i][0] == "num":
                    final_list.append(inp[i][1])

                if inp[i][0] == "(":
                    i, new_input = create_new_input(i, inp)

                    # Repel the function
                    result = rec(new_input)

                    if result == "ERROR":
                        return "ERROR"

                    if result is None:
                        result = "()"

                    final_list.extend(result)

                i = i + 1

            final_list.append(")")
            return final_list
    elif inp[0][0] == "num":
        return [inp[0][1]]

    #Syntax ERROR
    return "ERROR"


def main():
    if len(argv) != 2:
        return

    filename = argv[1]

    f = open(filename, "r")
    text = f.read()

    i = 0
    while i < len(text):
        if text[i] == '\n' or text[i] == '\t':
            text = text[0:i] + " " + text[i + 1:len(text)]
        if text[i] == ' ':
            i = i + 1
            while (i < len(text) - 1) and (text[i] == ' ' or text[i] == '\n' or text[i] == '\t'):
                text = text[0:i] + text[i + 1:len(text)]
        else:
            i = i + 1

    # text = text.replace("\n", " ")
    text = text[0:len(text) - 1]

    spec = [("(", "("), (")", ")"), ("add", "+"), ("concat", "++"),
            ("lambda", "lambda\\ ([a-z]+ | [A-Z]+):"), ("id", "[a-z]+ | [A-Z]+"), ("num", "[0-9]+"),
            ("space", "\\ ")]


    lexer = Lexer(spec)

    final = lexer.lex(text)

    # Delete all space
    i = 0
    while i < len(final):
        if final[i][0] == "space":
            final = final[0:i] + final[i + 1:len(final)]
        else:
            i = i + 1

    result = rec(final)

    # If the result is still a function
    while result is not None and type(result[0]) is tuple:
        result = rec(result)

    if result == "ERROR":
        print("ERROR")
        return

    output = ""
    for i in range(len(result)):
        if result[i] == '(':
            if result[i + 1] == ')':
                output = output + result[i]
            else:
                output = output + result[i] + " "
        elif result[i] == ')':
            if i == len(result) - 1:
                output = output + result[i]
            else:
                output = output + result[i] + " "
        else:
            if i == len(result) - 1:
                output = output + result[i]
            else:
                output = output + result[i] + " "
    print(output, end="\n")


if __name__ == '__main__':
    main()
