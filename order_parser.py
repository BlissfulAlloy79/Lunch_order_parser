"""
Inputs of this parsing module:
[placer info] [order set info] + [drinks]
if order set info is A or B without specifying 飯 or 意粉 or 薯菜
it will setdefault as 飯
"""

import re


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
