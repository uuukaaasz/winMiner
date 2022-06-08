# coding: utf-8


class WinMinerRule(object):
    def __init__(self, antecedent, width1, consequent, width2, supp, conf):
        self.antecedent = antecedent
        self.consequent = consequent
        self.width1 = width1
        self.width2 = width2
        self.supp = supp
        self.conf = conf

    def __repr__(self):
        return '{}: {} [{}] ==> {} [{}] [{}, {}]'.format(
            type(self).__name__, self.antecedent, self.width1,
            self.consequent, self.width2, self.supp, self.conf
        )