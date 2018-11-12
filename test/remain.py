month = 16480
car = 100000 / 18
rent = 4200
must_pay_gu = 40000
must_pay_jj = 60000
must_pay_car = 100000
lend_cost = 0.15
lend_years = 5
lend_rate_monty = 0.0029


def month_pay(all_lend):
    lend_monty = all_lend / 60 + all_lend * lend_rate_monty
    return lend_monty + car + rent


def remain_10m(lend_money):
    lend_money = lend_money * 10000
    month_pay_all = month_pay(lend_money)
    print('lend {}, month pay: {}'.format(lend_money, month_pay_all))
    print('\tmonth remain: {}'.format(month - month_pay_all))
    print('\tafter 10 month remain: {}'.format(10 * (month - month_pay_all)))
    print('\tafter 10 month, total remain: {}'.format(
        lend_money * (1 - lend_cost) - must_pay_car - must_pay_gu - must_pay_jj + 10 * (month - month_pay_all)))


def all_interest(lend_money):
    all_interest_money = lend_money * lend_cost + lend_money * lend_rate_monty * lend_years * 12
    print("\tlend {}w, 5 years all interest is: {}w\n".format(lend_money, all_interest_money))


if __name__ == "__main__":
    remain_10m(30)
    all_interest(30)
    remain_10m(25)
    all_interest(25)
    remain_10m(20)
    all_interest(20)
