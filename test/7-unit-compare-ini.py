with open("test1.ini", 'rb') as fr1:
    with open("test2.ini", 'rb') as fr2:
        if fr1.read() == fr2.read():
            print(True)
        else:
            print(False)
