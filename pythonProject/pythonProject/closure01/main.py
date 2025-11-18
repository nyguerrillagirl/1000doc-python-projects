a = 100
def foo():
    global a
    print("==> in foo, global a value", a)
    b = a

    def bar():
        nonlocal b
        print(b)

    return bar


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("first time calling bar()")
    func = foo()
    func()
    a = a + 100
    foo()
    print("second time calling bar()")
    func()

