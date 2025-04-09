def formatted_price(price):
    new_price = list(str(price))
    if len(new_price) > 6:
        x = len(new_price) % 3
        formatted_price = ''.join(new_price[:x])
        for i in (range(x, len(new_price), 3)):
            formatted_price += ' '+''.join(new_price[i:i+3])
        return formatted_price.replace(' .', ',')
    else:
        price = str(price)
        return price.replace('.', ',')