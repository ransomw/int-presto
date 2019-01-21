import sys
from functools import partial

from pi import model as m
from pi_test.util_load_tests import load_tests_from_classes

from .base import Base

class SelfRefM2MTests(Base):

    def testPlaceholder(self):
        self.assertTrue(True)

    def testCreate(self):
        restaurant = m.Restaurant(name="Five Guys")
        burger = m.Item(restaurant=restaurant,
                        name="burger")
        fries = m.Item(restaurant=restaurant,
                       name="fries")
        ketchup = m.Item(restaurant=restaurant,
                         name="ketchup")
        burger.mods.append(fries)
        burger.mods.append(ketchup)
        fries.mods.append(ketchup)
        m.save_models(restaurant)

    def testRead(self):
        self.testCreate()
        restaurants = m.Restaurant.all()
        self.assertEqual(len(restaurants), 1)
        restaurant = restaurants[0]
        self.assertEqual(restaurant.name, "Five Guys")
        items = {item.name: item for item in restaurant.items}
        self.assertEqual(set(items.keys()), set([
            "burger",
            "fries",
            "ketchup",
        ]))
        self.assertEqual(
            set([mod.name for mod in items["burger"].mods]),
            set(["fries", "ketchup"]))
        self.assertEqual(
            set([mod.name for mod in items["fries"].mods]),
            set(["ketchup"]))

    def testSerialize(self):
        self.testCreate()
        restaurants = m.Restaurant.all()
        self.assertEqual(len(restaurants), 1)
        restaurant = restaurants[0]
        print(m.restaurant_schema.dump(restaurant).data)


load_tests = partial(load_tests_from_classes, sys.modules[__name__], [
    SelfRefM2MTests,
])
