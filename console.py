import re

contents: list = []


class OrderParse:
    def __init__(self, order):
        if type(order) is str:
            self.raw = order.split('\n')
        else:
            self.raw = order
        self.order = self.raw[2:]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2} [A-Z][a-z]{2}", self.raw[0]):
            raise SyntaxError("Header format incorrect, cannot identify date")
        if self.raw[1] != "":
            raise SyntaxError("Header spacing missing!")
        for i, j in enumerate(self.order):
            if '+' not in j:
                raise SyntaxError(f"Missing identifying notation '+' in the order list, item no. {i + 1}")

    def get_date(self):
        return self.raw[0]

    def get_total(self):
        return len(self.order)

    def get_food(self):
        food: dict = {}
        order = [i.split('+') for i in self.order]

        f_tmp = [i[-2].split() for i in order]
        for i in f_tmp:
            if len(i[-2]) == 1:
                i[-1] = i[-2] + i[-1]
            if i[-1] == "A" or i[-1] == "B":
                i[-1] += "飯"
            if i[-1] in food:
                food[i[-1]] += 1
            elif i[-1] not in food:
                food[i[-1]] = 1

        f_keys = list(food.keys())
        f_keys.sort()
        food = {i: food[i] for i in f_keys}

        return food

    def get_drinks(self):
        drinks: dict = {}
        order = [i.split('+') for i in self.order]

        d_tmp = [i[-1].strip() for i in order]
        for i in d_tmp:
            if i in drinks:
                drinks[i] += 1
            elif i not in drinks:
                drinks[i] = 1

        return drinks


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

    ex_wait = input("press enter to exit")
    exit()


if __name__ == '__main__':
    main()
