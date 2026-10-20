import math
import re

def lexer(text):
    pattern = r'\d+(?:\.\d*)?|\.\d+|tan|==|[+\-*/()]'
    tokens = []

    while text:
        text = text.lstrip()

        if text == "":
            break

        match = re.match(pattern, text)

        if match:
            tokens.append(match.group())
            text = text[len(match.group()):]
        else:
            raise ValueError("Недопустимый символ: " + text[0])

    return tokens


def calculate(tokens):
    position = 0

    def number():
        nonlocal position

        if position >= len(tokens):
            raise ValueError(
                "Выражение неожиданно закончилось: ожидалось число."
            )

        token = tokens[position]

        if token == "-":
            position += 1

            if position >= len(tokens) or tokens[position] in ("+", "-"):
                raise ValueError(
                    "Два знака подряд. Уберите лишний знак."
                )

            return -number()

        if token == "+":
            position += 1

            if position >= len(tokens) or tokens[position] in ("+", "-"):
                raise ValueError(
                    "Два знака подряд. Уберите лишний знак."
                )

            return number()

        if token == "tan":
            position += 1

            if position >= len(tokens) or tokens[position] != "(":
                raise ValueError(
                    "После tan ожидается открывающая скобка '('."
                )

            position += 1
            result = expression()

            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError(
                    "После аргумента tan отсутствует закрывающая скобка ')'."
                )

            position += 1
            return math.tan(result)

        if token == "(":
            position += 1
            result = expression()

            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError(
                    "Отсутствует закрывающая скобка ')'."
                )

            position += 1
            return result

        if token == ")":
            raise ValueError(
                "Неожиданная закрывающая скобка ')'. Проверьте скобки."
            )

        if re.fullmatch(r'\d+(?:\.\d*)?|\.\d+', token):
            position += 1
            return float(token)

        raise ValueError(
            f"Ожидалось число или выражение в скобках, но найдено '{token}'. "
        )

    def multiply():
        nonlocal position
        result = number()

        while position < len(tokens):
            if tokens[position] == "*":
                position += 1
                result *= number()

            elif tokens[position] == "/":
                position += 1
                right = number()

                if right == 0:
                    raise ValueError(
                        "Деление на ноль невозможно. Измените делитель."
                    )

                result /= right

            else:
                break

        return result

    def expression():
        nonlocal position
        result = multiply()

        while position < len(tokens):
            if tokens[position] == "+":
                position += 1
                result += multiply()

            elif tokens[position] == "-":
                position += 1
                result -= multiply()

            else:
                break

        return result

    for i in range(len(tokens) - 1):
        if tokens[i] in ("+", "-") and tokens[i] == tokens[i + 1]:
            raise ValueError(
                f"Два знака '{tokens[i]}' подряд. Уберите лишний знак."
            )

    result = expression()

    if position < len(tokens) and tokens[position] == "==":
        position += 1
        right = expression()
        result = result == right

    if position != len(tokens):
        token = tokens[position]

        if token == ")":
            raise ValueError(
                "Лишняя закрывающая скобка ')'. Проверьте скобки."
            )

        if re.fullmatch(r'\d+(?:\.\d*)?|\.\d+', token) or token == "(":
            raise ValueError(
                f"Перед '{token}' пропущен математический оператор."
            )

        raise ValueError(
            f"Неожиданный элемент '{token}'. Проверьте выражение."
        )

    return result


while True:
    text = input("Введите выражение (exit - выход): ")

    if text.strip().lower() == "exit":
        break

    try:
        tokens = lexer(text)
        result = calculate(tokens)
        print("Результат:", result)

    except ValueError as error:
        print("Ошибка:", error)

    except RecursionError:
        print("Ошибка: слишком много вложенных выражений или скобок.")
