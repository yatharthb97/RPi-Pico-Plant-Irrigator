# Source https://stackoverflow.com/a/30169668/11733629


def is_leap_year(year):
    """ if year is a leap year return True
        else return False """
    if year % 100 == 0:
        return year % 400 == 0
    return year % 4 == 0

def yearday(D, M, Y):
    """ given year, month, day return day of year
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
    return N

def ymd(Y, N):
    """ given year = Y and day of year = N, return year, month, day
        Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
    if is_leap_year(Y):
        K = 1
    else:
        K = 2
    M = int((9 * (K + N)) / 275.0 + 0.98)
    if N < 32:
        M = 1
    D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
    return D, M, Y