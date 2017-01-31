
def get_z_a(za):
    i = int(za)
    a = i % 1000
    z = i // 1000
    result = {"z": z, "a": a}
    return result


