import datetime
import string
import json


DATETIME_FORMAT = '%Y/%m/%d %H:%M'


class Ttm(object):
    """docstring for Ttm"""
    def __init__(self, date, check):
        super(Ttm, self).__init__()
        self.date = date
        self.check_type = 'Check-in' if int(check) == 1 else 'Check-out'
        self.comment = 'Esqueci'


    def __str__(self):
        return "{} {} {}".format(datetime.datetime.strftime(self.date, DATETIME_FORMAT),
                                 self.check_type,
                                 self.comment)


def get_ttms(dates):
    return [Ttm(datetime.datetime.strptime(date.strip().split('|')[0], DATETIME_FORMAT), date.strip().split('|')[1]) for date in dates]


def send_ttm_to_server(ttm):
    print "Sending: {}".format(ttm)


def main():
    dates_from_file = []
    with open('hours.txt', 'r') as fh:
        dates_from_file = fh.readlines()

    ttms = get_ttms(dates_from_file)
    for ttm in ttms:
        send_ttm_to_server(ttm)

if __name__ == '__main__':
    main()
