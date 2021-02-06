import linkingFuncs

def main():

    # result = linkingFuncs.search_tiker("121edscawdfvbe")
    # result2 = linkingFuncs.search_tiker("AAPL")
    # print(result)
    # print(result2)

    # result3 = linkingFuncs.viewDetail_info("1d", "msft")
    # print(result3)

    result4 = linkingFuncs.graph_info("1d", "msft")
    print(result4)
    print()
    print(len(result4))

    return 0

main()