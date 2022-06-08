from functools import reduce


def get_config_value(key, cfg):
    return reduce(lambda c, k: c[k], key.split('.'), cfg)
