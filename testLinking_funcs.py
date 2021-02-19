import linkingFuncs


def test_search_ticker():
    result = linkingFuncs.search_tiker("121edscawdfvbe")
    result2 = linkingFuncs.search_tiker("AAPL")
    print(result)
    print(result2)

def test_viewDetail_info():
    result3 = linkingFuncs.viewDetail_info("1d", "msft")
    print(result3)

def test_graph_info():
    result4 = linkingFuncs.graph_info("1d", "msft")
    print(result4)
    print()
    print(len(result4))

def test_create_account():
    print(linkingFuncs.create_account('Wesley', 'Reynolds', 'Wazzah', 'Vafdsfay')) 

def test_login():
    print(linkingFuncs.login('Wazzah', 'Vafdsfay'))       

def test_record_transaction():
    print(linkingFuncs.record_transaction('Wazzah', 10, 'AAPL', 'SELL'))

def test_get_profile():
    print(linkingFuncs.get_profile('Wazzah'))  

def test_get_watchlist():
    print(linkingFuncs.get_watchlist('Wazzah'))

def test_add_watchlist():
    print(linkingFuncs.add_watchlist('Wazzah', 'AAPL'))
    print(linkingFuncs.add_watchlist('Wazzah', "MSFT"))

def test_remove_watchlist():
    print(linkingFuncs.remove_watchlist('Wazzah', 'AAPL'))

def main():
    #test_search_ticker()
    #test_viewDetail_info()
    #testgraph_info()
    #test_create_account()
    #test_login()
    #test_record_transaction()
    #test_get_profile(
    #test_add_watchlist()
    #test_remove_watchlist()
   
    #test_get_watchlist()

    return 0

main()