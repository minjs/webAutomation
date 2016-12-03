import csv


class Keywords:
    keywords = []

    def __init__(self):
        self.keywords = []

    def filter_keywords(self):
        for i in self.keywords:
            if len(i) <= 3:
                self.keywords.remove(i)

    def parse_text_keywords(self, filename):
        with open(filename) as f:
            self.keywords = f.readlines()
        self.filter_keywords()

    def pase_cvs_keywords(self, filename):
        with open(filename, 'rb') as csv_file:
            self.keywords = csv.reader(csv_file, delimiter=' ', quotechar='|')
        self.filter_keywords()