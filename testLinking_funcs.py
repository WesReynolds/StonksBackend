import linkingFuncs


def test_update_cache():
    print(linkingFuncs.update_cache())

def test_search_ticker():
    result = linkingFuncs.search_tiker("AAPL")
    result2 = linkingFuncs.search_tiker("GE")
    result3 = linkingFuncs.search_tiker("GME")
    result4 = linkingFuncs.search_tiker("GOOG")
    result5 = linkingFuncs.search_tiker("MSFT")
    result6 = linkingFuncs.search_tiker("BA")
    print(result)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
    print(result6)

def test_viewDetail_info():
    result3 = linkingFuncs.viewDetail_info("1d", "msft")
    print(result3)

def test_graph_info():
    result4 = linkingFuncs.graph_info("1d", "msft")
    print(result4)
    print()
    print(len(result4))

def test_create_account():
    assert linkingFuncs.create_account('Wesley', 'Reynolds', 'Wazzah', 'Vafdsfay') 

def test_login():
    print(linkingFuncs.login('Wazza', 'Vafdsfay'))       

def test_record_transaction():
    print(linkingFuncs.record_transaction('Wazza', 10, 'AAPL', 'SELL'))

def test_get_profile():
    print(linkingFuncs.get_profile('Wazza'))  

def test_get_watchlist():
    print(linkingFuncs.get_watchlist('Joshi'))

def test_add_watchlist():
    print(linkingFuncs.add_watchlist('Joshi', 'AMZN'))

def test_remove_watchlist():
    print(linkingFuncs.remove_watchlist('Wazza', 'TSLA'))

def test_buy():
    print(linkingFuncs.buy('Wazza', 'BAC', 15))
    
def test_sell():
    print(linkingFuncs.sell('Wazza', 'GME', 18))
    print(linkingFuncs.sell('Wazza', 'MSFT', 5))

def test_get_trending():
    print(linkingFuncs.get_trending(5))

def test_get_movers():
    print(linkingFuncs.get_movers(5))

def main():
    #test_update_cache()
    #test_search_ticker()
    #test_viewDetail_info()
    #testgraph_info()
    #test_create_account()
    #test_login()
    #test_record_transaction()
    #test_buy()
    #test_sell()
    #test_get_profile()
    #test_add_watchlist()
    #test_remove_watchlist()
    #test_get_watchlist()
    #test_get_trending()
    #test_get_movers()
    return 0

main()