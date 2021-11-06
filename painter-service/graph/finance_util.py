import numpy as np
import pandas as pd
import locale


def calculate_rsi(closes):
    i = 0
    up_prices = []
    down_prices = []
    #  Loop to hold up and down price movements
    while i < len(closes):
        if i == 0:
            up_prices.append(0)
            down_prices.append(0)
        else:
            if (closes[i] - closes[i - 1]) > 0:
                up_prices.append(closes[i] - closes[i - 1])
                down_prices.append(0)
            else:
                down_prices.append(closes[i] - closes[i - 1])
                up_prices.append(0)
        i += 1
    x = 0
    avg_gain = []
    avg_loss = []
    #  Loop to calculate the average gain and loss
    while x < len(up_prices):
        if x < 15:
            avg_gain.append(0)
            avg_loss.append(0)
        else:
            sum_gain = 0
            sum_loss = 0
            y = x - 14
            while y <= x:
                sum_gain += up_prices[y]
                sum_loss += down_prices[y]
                y += 1
            avg_gain.append(sum_gain / 14)
            if sum_loss != 0.0:
                avg_loss.append(abs(sum_loss / 14))
            else:
                avg_loss.append(0.00001)
        x += 1
    p = 0
    rsi = []
    #  Loop to calculate RSI and RS
    while p < len(closes):
        if p < 15:
            rsi.append(np.nan)
        else:
            rs_value = (avg_gain[p] / avg_loss[p])
            rsi.append(100 - (100 / (1 + rs_value)))
        p += 1
    lower_band = np.ones(len(rsi)) * 30
    upper_band = np.ones(len(rsi)) * 70
    return rsi, lower_band.tolist(), upper_band.tolist()


def moving_average(interval, window_size=10):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def bbands(price, window_size=10, num_of_std=5):
    price_pd = pd.DataFrame(price)
    rolling_mean = price_pd.rolling(window=window_size).mean()
    rolling_std = price_pd.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band


def fibonnaci_bands(closes):
    highest = max(closes)
    lowest = min(closes)
    line = dict(color='rgb(169,169,169,0.5)', width=2)
    line_main = dict(color='rgb(0,0,0,1)', width=4)
    top = highest - lowest
    l = []
    percent_23 = top * (1 - 0.236) + lowest
    percent_38 = top * (1 - 0.382) + lowest
    percent_50 = top * (1 - 0.5) + lowest
    percent_62 = top * (1 - 0.618) + lowest
    l.append((pd.DataFrame(np.full(len(closes), lowest)), line_main, "lowest: " + pretty_number(lowest)))
    l.append((pd.DataFrame(np.full(len(closes), percent_23)), line, "23%: " + pretty_number(percent_23)))
    l.append((pd.DataFrame(np.full(len(closes), percent_38)), line, "38%: " + pretty_number(percent_38)))
    l.append((pd.DataFrame(np.full(len(closes), percent_50)), line, "50%: " + pretty_number(percent_50)))
    l.append((pd.DataFrame(np.full(len(closes), percent_62)), line, "62%: " + pretty_number(percent_62)))
    l.append((pd.DataFrame(np.full(len(closes), top * 1 + lowest)), line_main, "top: " + pretty_number(highest)))
    return l


def bollinger_bands(highs, lows, closes, n=20, m=3):
    # sourcery skip: inline-immediately-returned-variable, merge-list-append
    tp = (pd.DataFrame(highs) + pd.DataFrame(lows) + pd.DataFrame(closes)) / 3
    ma = tp.rolling(n).mean()
    sd = m * tp.rolling(n).std()
    ls_up = dict(color='rgb(255, 0, 0, 0.5)')
    ls_mid = dict(color='rgb(255,20,147, 0.5)')
    ls_low = dict(color='rgb(34,139,34, 0.5)')
    ls_fib = dict(color='rgb(169,169,169,0.5)', width=1)
    l = []
    l.append((ma, ls_mid, True, "Middle Band"))
    # l.append((ma + (0.236 * sd), ls_fib, False, "Fib band"))
    # l.append((ma + (0.382 * sd), ls_fib, False, "Fib band"))
    # l.append((ma + (0.5 * sd), ls_fib, False, "Fib band"))
    # l.append((ma + (0.618 * sd), ls_fib, False, "Fib band"))
    # l.append((ma + (0.764 * sd), ls_fib, False, "Fib band"))
    l.append((ma + (1 * sd), ls_up, True, "Upper Band"))
    # l.append((ma - (0.236 * sd), ls_fib, False, "Fib band"))
    # l.append((ma - (0.382 * sd), ls_fib, False, "Fib band"))
    # l.append((ma - (0.5 * sd), ls_fib, False, "Fib band"))
    # l.append((ma - (0.618 * sd), ls_fib, False, "Fib band"))
    # l.append((ma - (0.764 * sd), ls_fib, False, "Fib band"))
    l.append((ma - (1 * sd), ls_low, True, "Lower Band"))
    return l


def keep_significant_number_float(float_to_keep: float, number: int):
    a = round(float_to_keep, number)
    str_action = "{:.$AMOUNTf}".replace('$AMOUNT', str(number))
    return a  # float(str_action.format(float_to_keep))


# convert int to nice string: 1234567 => 1 234 567
def number_to_beautiful(nbr):
    return locale.format_string("%d", nbr, grouping=True).replace(",", " ")


def pretty_number(num):
    if round(num) > 10:
        return number_to_beautiful(round(num))
    elif 0.01 < num < 10.01:
        return str(keep_significant_number_float(num, 3))  # [0:5]
    else:
        return str(keep_significant_number_float(num, 6))  # float_to_str(num)[0:10]

