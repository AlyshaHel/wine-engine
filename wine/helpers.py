def common_words(a: list, b: list):
    a_set = set(a)
    b_set = set(b)

    if a_set & b_set:
        return a_set & b_set
    else:
        return None

