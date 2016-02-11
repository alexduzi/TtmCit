import datetime
import string
import json
import urllib2
import unicodedata

#02/01/2016
DATETIME_FORMAT = '%d/%m/%Y %H:%M'

class Divergence(object):
    """docstring for Divergence"""
    def __init__(self, code_divergence, name_divergence, acronym_divergence, number_order):
        self.code_divergence = int(code_divergence)
        self.name_divergence = name_divergence
        self.acronym_divergence = acronym_divergence
        self.number_order = int(number_order)
        
    def __str__(self):
        return "{} {} {} {}".format(self.code_divergence,
                                    self.name_divergence,
                                    self.acronym_divergence,
                                    self.number_order)
                                                           
    def to_dict(self):
        return { "codeDivergence": self.code_divergence, 
                 "nameDivergence": self.name_divergence, 
                 "acronymDivergence": self.acronym_divergence,
                 "numberOrder": self.number_order}                                                                                                                                      
    

class Ttm(object):
    """docstring for Ttm"""
    def __init__(self, date, divergence):
        self.date = date
        self.divergence = divergence
        self.comment = 'Esqueci'


    def __str__(self):
        return "{} {} {}".format(datetime.datetime.strftime(self.date, DATETIME_FORMAT),
                                 self.divergence,
                                 self.comment)


def get_ttms(dates):
    return [Ttm(datetime.datetime.strptime(date.strip().split(';')[0], DATETIME_FORMAT), 
                Divergence(date.split(';')[1], 
                           date.split(';')[2], 
                           date.split(';')[3],
                           date.split(';')[4])) 
            for date in dates]


def send_ttm_to_server(ttm):
        print "Sending: {}".format(ttm)
        ttm_dict = { 
                     "dateOccurrence" : datetime.datetime.strftime(ttm.date, DATETIME_FORMAT),
					 "divergence" : ttm.divergence.to_dict(),
					 "textEmployeeComment" : ttm.comment
				   }
        req = urllib2.Request('http://ttm.ciandt.com/occurrence')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(ttm_dict))
        print json.dumps(ttm_dict)
        print response
        


def main():
    dates_from_file = []
    with open('hours.txt', 'r') as fh:
        for line in fh:
            dates_from_file.append(line.strip())

    ttms = get_ttms(dates_from_file)
    for ttm in ttms:
        send_ttm_to_server(ttm)

if __name__ == '__main__':
    main()
