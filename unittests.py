import unittest
import linkingFuncs


class TestLinkingFuncs(unittest.TestCase):

    def test_buy(self):
        trueValue = {'Action': True}
        falseValue = {'Action': False}

        self.assertEqual(linkingFuncs.buy("Wazza", "AAPL", 5), trueValue)   # Good entry
        self.assertEqual(linkingFuncs.buy("Wazza", "", 10), falseValue)     # Bad ticker symbol
        self.assertEqual(linkingFuncs.buy("", "AAPL", 15), falseValue)      # Bad username

    def test_sell(self):
        trueValue = {'Action': True}
        falseValue = {'Action': False}

        self.assertEqual(linkingFuncs.sell("Wazza", "AAPL", 5), trueValue)   # Good entry
        self.assertEqual(linkingFuncs.sell("Wazza", "", 10), falseValue)     # Bad ticker symbol
        self.assertEqual(linkingFuncs.sell("", "AAPL", 15), falseValue)      # Bad username
        self.assertEqual(linkingFuncs.sell("Wazza", "AAPL", 99), falseValue)    # Selling more than user owns
        self.assertEqual(linkingFuncs.sell("Wazza", "HD", 15), falseValue)      # Selling unowned stock

    def test_get_profile(self):
        profile = linkingFuncs.get_profile("Wazza")
        self.assertEqual(type(profile), dict)   # Check that it is a dictionary
        self.assertNotEqual(profile, {})        # Check that it is not empty

    def test_get_watchlist(self):
        profile = linkingFuncs.get_watchlist("Wazza")
        self.assertEqual(type(profile), dict)   # Check that it is a dictionary
        self.assertNotEqual(profile, {})        # Check that it is not empty

    def test_get_trending(self):
        profile = linkingFuncs.get_trending("Wazza")
        self.assertEqual(type(profile), dict)  # Check that it is a dictionary
        self.assertNotEqual(profile, {})  # Check that it is not empty

    def test_get_movers(self):
        profile = linkingFuncs.get_movers("Wazza")
        self.assertEqual(type(profile), dict)  # Check that it is a dictionary
        self.assertNotEqual(profile, {})  # Check that it is not empty

    def test_create_account(self):
        badAccount = {'Action': False}
        self.assertEqual(linkingFuncs.create_account("Wes", "Reynolds", "Wesley", "password"),
                         {'Action': True, 'username': "Wesley", 'firstname': "Wes", 'lastname': "Reynolds",
                          'password': "password"})
        self.assertEqual(linkingFuncs.create_account("Wes", "Reynolds", "Wazza", "hi"), badAccount)

    def test_login(self):
        self.assertEqual(linkingFuncs.login("Wazza", "myPassword"),
                         {'Action': True, 'username': "Wazza", 'firstname': "Wesley",
                          'lastname': "Reynolds", 'password': "myPassword"})
        self.assertEqual(linkingFuncs.login("Wazza", "bad"), {'Action': False})
        self.assertEqual(linkingFuncs.login("Wes", "myPassword"), {'Action': False})

    def test_remove_watchlist(self):
        goodEntry = {'Action': True}
        badEntry = {'Action': False}
        self.assertEqual(linkingFuncs.remove_watchlist("Wes", "AAPL"), badEntry)    # Account does not exist
        self.assertEqual(linkingFuncs.remove_watchlist("Wazza", "DIS"), badEntry)   # Stock not on watchlist
        linkingFuncs.add_watchlist("Wazza", "AAPL")
        self.assertEqual(linkingFuncs.remove_watchlist("Wazza", "AAPL"), goodEntry)

    def test_add_watchlist(self):
        goodEntry = {'Action': True}
        badEntry = {'Action': False}
        self.assertEqual(linkingFuncs.add_watchlist("Wes", "AAPL"), badEntry)   # Bad Account
        self.assertEqual(linkingFuncs.add_watchlist("Wazza", "IIIIIIIIII"), badEntry) # Bad Stock
        self.assertEqual(linkingFuncs.add_watchlist("Wazza", "AAPL"), goodEntry)

    def test_update_cache(self):
        self.assertEqual(linkingFuncs.update_cache(), {'Action': True})

    def test_search_tiker(self):
        self.assertEqual(linkingFuncs.search_tiker("IIIIIII"), {'Action': False})   # Bad Ticker symbol
        stock = linkingFuncs.search_tiker("AAPL")
        self.assertEqual(type(stock), dict)     # Check that a dictionary is returned
        self.assertNotEqual(stock, {})      # Check that the dictionary is not empty


if __name__ == '__main__':
    unittest.main()
