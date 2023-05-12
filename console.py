from order_parser import OrderParse

contents: list = []


def read_order():
    global contents
    print("Enter your order: (format please refer to readme.md)")

    for i in range(2):
        line = input()
        contents.append(line)
    while True:
        line = input()
        if line:
            contents.append(line)
        else:
            break

    print(f"Received list {contents}")
    print()
    return


def main():
    read_order()
    try:
        interp = OrderParse(contents)

        t_order = interp.get_total()
        f_order = interp.get_food()
        d_order = interp.get_drinks()

        order_date = interp.get_date()
        # send order msg
        formatted_text = f"{order_date}\n"
        formatted_text += "華仁\n\n"
        formatted_text += f"Total: $38x{t_order} = ${38 * t_order}\n\n"
        for i in f_order.keys():
            formatted_text += f"{i} x{f_order[i]}\n"
        formatted_text += "\n"
        for i in d_order.keys():
            formatted_text += f"{i} x{d_order[i]}\n"
        print(formatted_text)

        # generate checklist in Markdown format
        check_text = f"{order_date}\n\n"
        check_text += f"Total: $38x{t_order} = ${38 * t_order}\n\n"
        for i in interp.order:
            check_text += f"[ ] {i}\n\n"
        print(check_text)

    except SyntaxError as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
