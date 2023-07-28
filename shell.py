import interpreter.lang as lang


def run():
    while True:
        output, error = lang.run(file_name="stdin", text=input("> "))
        if error:
            print(error)
        else:
            print(output)


if __name__ == "__main__":
    run()
