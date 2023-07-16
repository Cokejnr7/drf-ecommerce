def validate_item_price(price):
    if price < 0:
        raise ValueError("price cannot be less than 0")
