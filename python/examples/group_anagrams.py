# LeetCode 49 — Group Anagrams
# Given an array of strings, group the anagrams together.
# Approach: two strings are anagrams iff sorting their characters
# produces the same canonical key. Use a dict to collect groups.
# O(n * k log k) time, where k is the average string length.

def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = sorted(s)  # list of sorted chars
        # Convert list back to string for use as a dict key
        key_str = ""
        for ch in key:
            key_str = key_str + ch
        if key_str not in groups:
            groups[key_str] = []
        groups[key_str].append(s)
    result = []
    for key in groups:
        group_list = []
        for s in groups[key]:
            group_list.append(s)
        result.append(group_list)
    return result


def show_groups(groups):
    """Pretty-print a list of lists of strings."""
    out = "["
    first = True
    for g in groups:
        if not first:
            out = out + ", "
        first = False
        out = out + "["
        inner_first = True
        for s in g:
            if not inner_first:
                out = out + ", "
            inner_first = False
            out = out + "'" + s + "'"
        out = out + "]"
    out = out + "]"
    print(out)


# ---- Tests ----
show_groups(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Expected: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

show_groups(group_anagrams([""]))
# Expected: [[""]]

show_groups(group_anagrams(["a"]))
# Expected: [["a"]]

show_groups(group_anagrams(["abc", "bca", "cab", "xyz", "zyx", "zz"]))
# Expected: [["abc", "bca", "cab"], ["xyz", "zyx"], ["zz"]]

