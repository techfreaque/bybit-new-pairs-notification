import time

from pybit import HTTP


def get_spot_symbols():
    session = HTTP("https://api.bybit.com")
    return session.query_symbol(spot=True)


def get_futures_symbols():
    session = HTTP("https://api.bybit.com")
    return session.query_symbol()


def difference(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


while True:
    spot_symbols_raw = get_spot_symbols()["result"]
    futures_symbols_raw = get_futures_symbols()["result"]
    spot_symbols = []
    futures_symbols = []

    for symbol in range(0, len(futures_symbols_raw)):
        futures_symbols.append(futures_symbols_raw[symbol]["name"])

    for spot_symbol in range(0, len(spot_symbols_raw)):
        spot_symbols.append(spot_symbols_raw[spot_symbol]["name"])

    live_symbols = spot_symbols + list(set(futures_symbols) - set(spot_symbols))
    symbols_count = len(live_symbols)
    current_pairs_file = None
    try:
        current_pairs_file = open("current_pairs_list.txt")
    except:
        current_pairs_file = open("current_pairs_list.txt", "w+")

    prev_pairs_list_raw = current_pairs_file.readlines()[1:]
    previous_pairs_list = []
    for current_pair in prev_pairs_list_raw:
        previous_pairs_list.append(current_pair.rstrip("\n"))

    new_pairs = difference(previous_pairs_list, live_symbols)

    if previous_pairs_list:
        for pair in new_pairs:
            is_new_on_Futures = ""
            is_new_on_spot = ""

            for old_pair in futures_symbols:
                if pair == old_pair:
                    is_new_on_Futures = " Futures"
            for old_pair in spot_symbols:
                if pair == old_pair:
                    is_new_on_spot = " Spot"
            and_str = ""
            if is_new_on_spot == " Spot" and is_new_on_Futures == " Futures":
                and_str = " and"

            new_pair_str = pair + is_new_on_Futures + and_str + is_new_on_spot
            new_pair_file = open(new_pair_str, "w+")
            new_pair_file.close()

    open("current_pairs_list.txt", "w").close()
    current_pairs_file = open("current_pairs_list.txt", "w+")
    supported_count_str = "Currently bybit has a total of " + str(symbols_count) + " pairs listed\n"
    current_pairs_file.write(supported_count_str)

    for symbol in live_symbols:
        current_pairs_str = current_pairs_file.write(symbol + "\n")
    current_pairs_file.close()
    if previous_pairs_list:
        print("bybit added " + str(len(new_pairs)) + " pair(s) " + str(new_pairs))
        print("next check in 60 seconds")
    else:
        print("started checking for new traded pairs every 60 seconds \n from now on you'll get notified when a new pair is available, even if this program is not running all the time")
    time.sleep(60)
