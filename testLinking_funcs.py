import linkingFuncs


def test_1():
    result = linkingFuncs.search_tiker("121edscawdfvbe")
    result2 = linkingFuncs.search_tiker("AAPL")
    print(result)
    print(result2)

def test_2():
    result3 = linkingFuncs.viewDetail_info("1d", "msft")
    print(result3)

def test_3():
    result4 = linkingFuncs.graph_info("1d", "msft")
    print(result4)
    print()
    print(len(result4))

def main():
    test_1()
    #test_2()
    #test_3()
    return 0

main()