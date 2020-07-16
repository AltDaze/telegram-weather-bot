from hashlib import md5

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

class Pay:
    def paykey(self, sum, id, qiwi=None, yandex=None, card=None, kassa=None, any=None, text=None, sal=None):
        from telebot import types
        pkb =           types.InlineKeyboardMarkup()
        global qb, yb, cb
        
        if sal:
            sale =      '{:.2f}'.format(sum / 100 * sal)
            newsum =    float(float(sum) - float(sale))
            sum =       newsum
        
        if kassa:
            script =    make_md5('{}:{}:secret:{}'.format(kassa, sum, id))
            kassaurl =  "http://www.free-kassa.ru/merchant/cash.php?m={3}&oa={0}&o={1}&s={2}".format(sum, id, script, kassa)

            ksb =       types.InlineKeyboardButton(text=text, url=kassaurl)
            pkb.add(ksb)

        if qiwi:
            qiwiurl =   "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={0}&amountInteger={1}&amountFraction=0&extra%5B%27comment%27%5D={2}&currency=643".format(qiwi, sum, id)

            qb =        types.InlineKeyboardButton(text=text, url=qiwiurl)
            pkb.add(qb)

        if yandex:
            yandexurl = "https://money.yandex.ru/transfer?receiver={0}&sum={1}&successURL=&quickpay-back-url=&shop-host=&label=&comment={2}&origin=form&selectedPaymentType=PC&destination={2}%3B%0A{2}&form-comment={2}&short-dest=&quickpay-form=shop".format(yandex, sum, id)

            yb =        types.InlineKeyboardButton(text=text, url=yandexurl)
            pkb.add(yb)

        if card:
            cardurl =   "https://money.yandex.ru/transfer?receiver={0}&sum={1}&successURL=&quickpay-back-url=&shop-host=&label=&targets={2}&comment={2}&origin=form&selectedPaymentType=AC&destination={2}%3B%0A{2}&form-comment={2}&short-dest=&quickpay-form=shop".format(card, sum, id)

            cb =        types.InlineKeyboardButton(text=text, url=cardurl)
            pkb.add(cb)

        if any:
            script =    make_md5('{}:{}:{}:{}:{}'.format('RUB', sum, 'secret', any, id))
            anyurl =    "https://anypay.io/merchant?merchant_id={}&pay_id={}&amount={}&currency=RUB&sign={}".format(any, id, sum, script)

            ab =        types.InlineKeyboardButton(text=text, url=anyurl)
            pkb.add(ab)

        return pkb