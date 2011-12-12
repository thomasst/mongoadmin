def ellipsize(s, length):
    if not s:
        return ''
    if len(s) <= length:
        return s
    else:
        return s[:length-3] + '...'
