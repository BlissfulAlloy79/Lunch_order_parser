# Lunch_order_parser

---

## Scenario

~~You are Chris Wong~~

~~Since the spirit of your school is "We Are Man For and With Others", you are now in charged with helping the lunch order for your schoolmates~~

The restaurant you are ordering contains different lunch sets (A, B, C, D, E, F, G, J, K) and drinks are provided for free

For set A and set B, you should specify 飯 or 意粉 or 薯菜, if not specified it will default as 飯

With the student discounts, every lunch set only costs $38 and drinks are free

#### For the order sent to the restaurant, it must be in the following format:

```markdown
[yyyy-mm-dd]
[school name]

Total: $38x[total set count] = $[total amount]

[lunch set] x[count]
...

[drinks] x[count]
...
```

#### For the schoolmates, they will compose up their order into the following format:

```markdown
[yyyy-mm--dd] [weekday]

[schoolmate info] [lunch set] + [drinks]
[schoolmate info] [lunch set] + [drinks]
...
```

---

## How it works

The script basically reads the '+' sign in each line of orders

If the '+' sign can't be found, it will raise an exception

## Setting up

Clone the repo into a file

Make sure the `main.py` and `order_parser.py` are in the same directory

Fist time set up it will generate a `config.yml`, fill up the config and re-execute the `main.py`

Since the I/O was based on a telegram bot, a tg bot token will also be required

### telegram bot commands:

~~check the `main.py` yourself la~~

```
/order [yyyy-mm--dd] [weekday]

[schoolmate info] [lunch set] + [drinks]
[schoolmate info] [lunch set] + [drinks]
...
```

~~.exe when?~~

~~docker when?~~
