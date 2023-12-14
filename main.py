from curses.ascii import isdigit
from typing import Dict, List
from functools import reduce


def add(a, b):
    return a + b


digit_dict = {
    "e": ("eight", 8),
    "f": {
        "fi": ("five", 5),
        "fo": ("four", 4),
    },
    "n": ("nine", 9),
    "o": ("one", 1),
    "s": {
        "se": (
            "seven",
            7,
        ),
        "si": (
            "six",
            6,
        ),
    },
    "t": {
        "th": (
            "three",
            3,
        ),
        "tw": (
            "two",
            2,
        ),
    },
    "z": ("zero", 0),
}


def get_line_components(line: str):
    components = []

    indices = []

    line_length = len(line)

    for i in range(line_length):
        char = line[i]
        if isdigit(char):
            indices.append(i)

    prefix_checked = False
    iterator = 0
    while iterator < len(indices):
        index_value = indices[iterator]
        substring = []

        total_indices = len(indices)

        if iterator == 0 and index_value > 0 and not prefix_checked:
            substring_before_first_digit = []
            for i in range(0, index_value):
                substring_before_first_digit.append(line[i])

            components.append(substring_before_first_digit)
            prefix_checked = True
            continue

        if iterator == total_indices - 1:
            if index_value < line_length:
                for i in range(index_value + 1, line_length):
                    substring.append(line[i])
        else:
            next_index = int(indices[iterator + 1])

            distance = next_index - index_value

            if distance > 0:
                j = index_value + 1
                for j in range(j, next_index):
                    substring.append(line[j])

        components.append(int(line[index_value]))
        if len(substring) > 0:
            components.append(substring)
        iterator = iterator + 1

    return components


def get_digit_strings(component: List[str]) -> List[int]:
    digits = []
    length = len(component)

    for i in range(length):
        char = component[i]

        # print(f"i={i}: {char}")

        outcome = digit_dict.get(char, None)
        if outcome:
            concat = char

            j = i + 1
            while True:
                if outcome is None:
                    # print(f"No outcomes for {concat}")
                    break
                if j == len(component):
                    # print("NO MORE LETTERS")
                    break

                # print(f"j={j}: {component[j]}")

                # print(f"Possible outcomes: {outcome}")

                if isinstance(outcome, dict):
                    concat = concat + component[j]
                    outcome = outcome.get(concat, None)
                elif isinstance(outcome, tuple):
                    # print(f"one possible result for {concat}")
                    # print(f"Checking {concat} against {outcome[0]}")

                    pattern = outcome[0]

                    if concat == pattern:
                        # print(f"found a match! {concat} == {pattern}")
                        digits.append(outcome[1])
                        break

                    start_index = len(concat)

                    next_concat_letter = component[j]
                    next_pattern_letter = pattern[start_index]

                    # print(f"Next concat: {next_concat_letter}")
                    # print(
                    #     f"Next in pattern {pattern} at index {start_index}: {next_pattern_letter}"
                    # )

                    if next_concat_letter != next_pattern_letter:
                        # print(
                        #     f"Subsequent letters do not match! {next_concat_letter} != {next_pattern_letter}"
                        # )
                        break
                    else:
                        concat = concat + next_concat_letter

                if j < len(component) - 1:
                    j = j + 1

    return digits


data = open("data.txt", "r")

line = data.readline()
line_number = 1

calibration_values: List[int] = []

while line:
    print(f"Line #{line_number}: {line}")

    temp: List[int] = []
    components = get_line_components(line)

    for component in components:
        # print(f"\t component: {component}")
        if isinstance(component, int):
            temp.append(component)
        else:
            extracted_numbers = get_digit_strings(component)

            [temp.append(number) for number in extracted_numbers]

    print(f"TEMP: {temp}")

    if len(temp) > 1:
        calibration_values.append(int(f"{temp[0]}{temp[len(temp) -1]}"))
    elif len(temp) <= 1:
        calibration_values.append(int(f"{temp[0]}{temp[0]}"))

    line = data.readline()
    line_number = line_number + 1

print(calibration_values)

result = reduce(add, calibration_values)
print(f"Final sum: {result}")

data.close()
