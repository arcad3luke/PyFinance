import main

annual_gross = main.hourly()


def caliCalc():
    if annual_gross <= 8932:
        state_tax = annual_gross * .01
        return state_tax
    if 8933 >= annual_gross <= 21175:
        state_tax = 89.32 + annual_gross * .02
        return state_tax
    if 21176 >= annual_gross <= 33421:
        state_tax = 334.18 + annual_gross * .04
        return state_tax
    if 33422 >= annual_gross <= 46394:
        state_tax = 824.02 + annual_gross * .06
        return state_tax
    if 46395 >= annual_gross <= 58634:
        state_tax = 1602.4 + annual_gross * .08
        return state_tax
    if 58635 >= annual_gross <= 299508:
        state_tax = 2581.60 + annual_gross * .093
        return state_tax
    if 299509 >= annual_gross <= 359407:
        state_tax = 24982.88 + annual_gross * .103
        return state_tax
    if 359408 >= annual_gross <= 599012:
        state_tax = 31152.48 + annual_gross * .113
        return state_tax
    if annual_gross > 599013:
        state_tax = 58227.85 + annual_gross * .123
        return state_tax
