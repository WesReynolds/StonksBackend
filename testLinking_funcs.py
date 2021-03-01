import linkingFuncs


# def test_search_ticker():
#     result = linkingFuncs.search_tiker("121edscawdfvbe")
#     result2 = linkingFuncs.search_tiker("AAPL")
#     print(result)
#     print(result2)

# def test_viewDetail_info():
#     result3 = linkingFuncs.viewDetail_info("1d", "msft")
#     print(result3)

# def test_graph_info():
#     result4 = linkingFuncs.graph_info("1d", "msft")
#     print(result4)
#     print()
#     print(len(result4))

# def test_create_account():
#     assert linkingFuncs.create_account('Wesley', 'Reynolds', 'Wazzah', 'Vafdsfay') 

def test_login():
    print(linkingFuncs.login('Wazza', 'Vafdsfay'))       

def test_record_transaction():
    print(linkingFuncs.record_transaction('Wazza', 10, 'AAPL', 'SELL'))

def test_get_profile():
    print(linkingFuncs.get_profile('Wazza'))  

def test_get_watchlist():
    print(linkingFuncs.get_watchlist('Joshi'))

def test_add_watchlist():
    print(linkingFuncs.add_watchlist('Wazza', 'TSLA'))

def test_remove_watchlist():
    print(linkingFuncs.remove_watchlist('Wazza', 'TSLA'))

def test_buy():
    print(linkingFuncs.buy('Wazza', 'GME', 17))
    print(linkingFuncs.buy('Wazza', 'MSFT', 5))
    
def test_sell():
    print(linkingFuncs.sell('Wazza', 'GME', 18))
    print(linkingFuncs.sell('Wazza', 'MSFT', 5))


def main():
    #test_search_ticker()
    #test_viewDetail_info()
    #testgraph_info()
    #test_create_account()
    #test_login()
    #test_record_transaction()
    #test_buy()
    #test_sell()
    test_get_profile()
    #test_add_watchlist()
    #test_remove_watchlist()
    #test_get_watchlist()
    return 0

main()