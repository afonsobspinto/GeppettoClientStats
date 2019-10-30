def match_strings(s1, s2):
    return s1 in s2 or s2 in s1


def is_javascript(s):
    return s.endswith('.js') or s.endswith('.ts') or s.endswith('.tsx') or s.endswith('.jsx')
