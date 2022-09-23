import numpy as np


def is_magic_square(square):
    sum1 = len(square) * (len(square) ** 2 + 1) / 2
    sum2 = np.sum(square, axis=0)
    sum3 = np.sum(square, axis=1)
    for i in sum2:
        if not i == sum1:
            return False
    for i in sum3:
        if not i == sum1:
            return False
    if not np.sum(np.diag(square)) == sum1:
        return False
    if not np.sum(np.fliplr(square).diagonal()) == sum1:
        return False
    return True


def make_a_magic_square(length):
    arr = np.arange(1, length * length+1)
    np.random.shuffle(arr)
    arr1 = np.reshape(arr, (length, length))
    while not is_magic_square(arr1):
        arr = np.arange(1, length * length+1)
        np.random.shuffle(arr)
        arr1 = np.reshape(arr, (length, length))
        print(arr1)
    print(arr1)
    return arr1


def main():
    make_a_magic_square(3)


if __name__ == "__main__":
    main()
