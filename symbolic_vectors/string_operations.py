def get_table_basic(heads, content, sep='|'):
    S = []
    head_lenghts = [max(map(len, (c[i] for c in content))) + len(h) for i, h in enumerate(heads)]
    W = sep.join(["_"*(sum(head_lenghts) + len(sep)*(len(heads)) - 1)])
    S.append(' ' + W)
    S.append(sep + sep.join([*(h + " "*(head_lenghts[i] - len(h)) for i, h in enumerate(heads))]) + sep)
    S.append(sep + sep.join([*(l*"_" for l in head_lenghts)]) + sep)
    for c in content:
        S.append(sep + sep.join([*((q := str(f)) + abs(len(q) -
              head_lenghts[i])*' ' for i, f in enumerate(c))]) + sep)
    S.append('|' + W + '|')
    return '\n'.join(S)

def get_table(heads, content, sep='│'):
    S = []
    head_lengths = [max(map(len, (c[i] for c in content))) + len(h) for i, h in enumerate(heads)]
    W = '─' * (sum(head_lengths) + len(sep) * (len(heads)) - 1)
    S.append('┌' + W + '┐')
    S.append(sep + sep.join([*(h + " " * (head_lengths[i] - len(h)) for i, h in enumerate(heads))]) + sep)
    S.append('├' + '┼'.join([l * '─' for l in head_lengths]) + '┤')
    for c in content:
        S.append(sep + sep.join([*((q := str(f)) + abs(len(q) - head_lengths[i]) * ' ' for i, f in enumerate(c))]) + sep)
    S.append('└' + W + '┘')
    return '\n'.join(S)
