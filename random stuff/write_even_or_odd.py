for i in range(1, 2001):
    if i % 2 == 0:
        print("elif i == " + str(i) + ":")
        print('\tprint("even")')
    else:
        print("elif i == " + str(i) + ":")
        print('\tprint("odd")')
