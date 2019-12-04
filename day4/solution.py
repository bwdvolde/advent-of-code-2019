from collections import Counter


def count_passwords(start, end, valid_password_calculator):
    return len([0 for password in range(start, end) if valid_password_calculator(password)])


def is_valid_password_part_1(password):
    """
    >>> is_valid_password_part_1(111123)
    True
    >>> is_valid_password_part_1(111111)
    True
    >>> is_valid_password_part_1(223450)
    False
    >>> is_valid_password_part_1(123789)
    False
    """
    password_digits = [int(digit) for digit in str(password)]
    for i in range(1, len(password_digits)):
        previous = password_digits[i - 1]
        current = password_digits[i]
        if current < previous:
            return False
        elif current == previous:
            contains_double = True

    return contains_double


def is_valid_password_part_2(password):
    """
    >>> is_valid_password_part_2(112233)
    True
    >>> is_valid_password_part_2(123444)
    False
    >>> is_valid_password_part_2(111122)
    True
    """
    password_digits = [int(digit) for digit in str(password)]
    counts = set(Counter(password_digits).values())
    return 2 in counts and is_valid_password_part_1(password)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(count_passwords(136818, 685979, is_valid_password_part_1))
    print(count_passwords(136818, 685979, is_valid_password_part_2))
