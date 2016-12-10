
def int_to_bin(value):
    binary_vector = []
    i = value
    while(i):
        if i & 1 == 1:
            binary_vector.append(1)
        else:
            binary_vector.append(0)
        i /= 2

    while len(binary_vector) <= 8:
        binary_vector.append(0)

    return binary_vector


def bin_to_int(binary_vector):
    sum = 0
    for i in range(len(binary_vector)):
        sum += binary_vector[i] * pow(2, i)
    return sum
