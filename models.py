# Four classes designed: Customer, FoodItem, Menu, and Transaction.
# Customer: a ByteBites user; holds their purchase_history, can be verified from it, and can view a Menu.
# FoodItem: a single menu item with a name, price, category, and popularity_rating.
# Menu: the catalog of FoodItems; supports adding items and filtering by category.
# Transaction: one customer's order; collects selected FoodItems and computes the total.
from __future__ import annotations


class FoodItem:
    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


class Menu:
    def __init__(self):
        self.items: list[FoodItem] = []

    def add_item(self, item: FoodItem) -> None:
        self.items.append(item)

    def filter_by_category(self, category: str) -> list[FoodItem]:
        return [i for i in self.items if i.category.lower() == category.lower()]


class Transaction:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.items: list[FoodItem] = []
        customer.purchase_history.append(self)

    def add_item(self, item: FoodItem) -> None:
        self.items.append(item)

    def compute_total(self) -> float:
        return round(sum(item.price for item in self.items), 2)


class Customer:
    def __init__(self, name: str):
        self.name = name
        self.purchase_history: list[Transaction] = []

    def is_verified(self) -> bool:
        return any(t.items for t in self.purchase_history)

    def view_menu(self, menu: Menu) -> list[FoodItem]:
        return list(menu.items)


if __name__ == "__main__":
    menu = Menu()
    burger = FoodItem("Spicy Burger", 8.5, "Food", 4.7)
    soda = FoodItem("Large Soda", 2.5, "Drinks", 4.2)
    cake = FoodItem("Choco Cake", 4.0, "Desserts", 4.9)
    for item in (burger, soda, cake):
        menu.add_item(item)

    assert menu.filter_by_category("drinks") == [soda]

    customer = Customer("Ava")
    assert customer.view_menu(menu) == [burger, soda, cake]
    assert not customer.is_verified()

    txn = Transaction(customer)
    assert customer.purchase_history == [txn]
    assert txn.compute_total() == 0.0
    assert not customer.is_verified()

    txn.add_item(burger)
    txn.add_item(soda)
    assert txn.compute_total() == 11.0
    assert customer.is_verified()

    float_txn = Transaction(customer)
    float_txn.add_item(FoodItem("A", 0.1, "Food", 1.0))
    float_txn.add_item(FoodItem("B", 0.2, "Food", 1.0))
    assert float_txn.compute_total() == 0.3
    print("All checks passed.")
