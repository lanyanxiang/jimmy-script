import jimmy_script

if __name__ == "__main__":
    while True:
        expr = input("jimmy-script > ")
        result, error = jimmy_script.evaluate(expr)
        if error:
            print(error)
        else:
            print(result)