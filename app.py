from models.Customer import Customer
from models.Order import Order
from models.Product import Product
from models.Cart import Cart


def main():
    # Create customer
    szymon = Customer("John Doe", "johndoe@example.com")

    # Create products
    laptop = Product("Laptop", 2999)
    smartphone = Product("Smartphone", 1299)
    tablet = Product("Tablet", 499)

    # Create a cart and add products
    cart = Cart()
    cart.add_item(laptop)
    cart.add_item(smartphone)
    cart.add_item(tablet)

    print(cart)

    # Create an order
    order = Order(szymon, cart)

    # Attempt to place an order
    order.place_order()

    laptop.change_price(3000)

    print(laptop)

    print(order)


if __name__ == "__main__":
    main()
