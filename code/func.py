import time


def make_code_or_id(prefix):
    base_str = str(time.time()).replace('.', '')[:15]
    return prefix + '{:0<15}'.format(base_str)