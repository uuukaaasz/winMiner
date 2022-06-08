# coding: utf-8
from numpy import *
from itertools import combinations, permutations
from . import WinMinerRule


class WinMiner(object):
    def __init__(self, sequence):
        self.sequence = sequence

    def createC1(self):
        C1 = {}
        for event in self.sequence:
            mo = tuple((event[0], event[0] + self.step))
            evt1 = tuple(event[1])
            if evt1 in C1:
                if mo not in C1[evt1]:
                    C1[evt1].add(mo)
            else:
                C1[evt1] = set((mo,))
        return C1

    def createLargeEpisodeSet(self, Ck):
        Lk = Ck.copy()
        for episode in Ck:
            if len(Ck[episode]) < self.minFrequent:
                del Lk[episode]
        return Lk

    def checkSubsetFrequency(self, candidate, Lk, k):
        if k > 1:
            subsets = list(combinations(candidate, k))
        else:
            return True
        for elem in subsets:
            if not elem in Lk:
                return False
        return True

    def createCandidates(self, Lk, L1, k):
        candidatesK = []
        lkKeys = sorted(set([item for t in Lk for item in t]))
        generatedCans = list(permutations(lkKeys, k))
        for can in generatedCans:
            if self.checkSubsetFrequency(can, Lk, k - 1):
                candidatesK.append(can)
        if len(candidatesK) == 0:
            return dict()
        else:
            Ck = {}
            if k == 2:
                for can in candidatesK:
                    Ck[can] = set()
                    for mok in Lk[tuple(can[0])]:
                        for mo1 in L1[tuple(can[1])]:
                            if mo1[0] >= mok[1] and mo1[1] - mok[0] <= self.max_width:
                                Ck[can].add(tuple((mok[0], mo1[1])))
            else:
                for can in candidatesK:
                    Ck[can] = set()
                    for mok in Lk[can[:-1]]:
                        for mo1 in L1[tuple(can[-1])]:
                            if mo1[0] >= mok[1] and mo1[1] - mok[0] <= self.max_width:
                                Ck[can].add(tuple((mok[0], mo1[1])))
            for episode, setOfMOs in Ck.items():
                rem = set()
                for mo1 in setOfMOs:
                    for mo2 in setOfMOs.difference(mo1):
                        if (mo1[0] == mo2[0] and mo1[1] < mo2[1]) or (mo1[0] > mo2[0] and mo1[1] == mo2[1]) or (
                                mo1[0] > mo2[0] and mo1[1] < mo2[1]):
                            rem.add(mo2)
                Ck[episode] = setOfMOs.difference(rem)
            return Ck

    def win_miner(self, max_width, step, minFrequent):
        self.minFrequent = minFrequent
        self.max_width = max_width
        self.step = step
        C1 = self.createC1()
        L1 = self.createLargeEpisodeSet(C1)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.createCandidates(L[k - 2], L1, k)
            Lk = self.createLargeEpisodeSet(Ck)
            L.append(Lk)
            k += 1
        if L[-1] == {}:
            L.pop()

        return L


class WinMinerRules(object):
    def __init__(self, largeEpisodeSet, max_width, step, minConfidence):
        self.largeEpisodeSet = largeEpisodeSet
        self.max_width = max_width
        self.step = step
        self.minConf = minConfidence

    def isAlphaOccurInBeta(self, mob, mos_alpha):
        for moa in mos_alpha:
            if mob[0] <= moa[0] and moa[1] <= mob[1]:
                return True
        return False

    def calcConfidence(self, mos_beta, wid1, mos_alpha, wid2):
        denominator = 0.0
        numerator = 0
        for mob in mos_beta:
            if mob[1] - mob[0] <= wid1:
                denominator += 1
                if self.isAlphaOccurInBeta((mob[0], mob[0] + wid2), mos_alpha):
                    numerator += 1
        if denominator == 0:
            return 0
        else:
            return numerator / denominator

    def calcSupport(self, mos_alpha, wid2):
        support = 0
        for moa in mos_alpha:
            if moa[1] - moa[0] <= wid2:
                support += 1
        return support

    def generateRules(self):
        bigRuleList = []
        time_bound = list(range(self.step, self.max_width, self.step))
        time_bound.append(self.max_width)
        for i in range(1, len(self.largeEpisodeSet)):
            for episode in self.largeEpisodeSet[i]:
                for j in range(1, i + 1):
                    lhsList = list(combinations(episode, j))
                    for lhs in lhsList:
                        for rightWid in time_bound:
                            for leftWid in time_bound:
                                conf = self.calcConfidence(self.largeEpisodeSet[j - 1][lhs], leftWid,
                                                           self.largeEpisodeSet[i][episode], rightWid)
                                if conf >= self.minConf:
                                    bigRuleList.append(WinMinerRule(list(lhs), leftWid, list(episode), rightWid,
                                                                    self.calcSupport(self.largeEpisodeSet[i][episode],
                                                                                   rightWid), conf))

        return bigRuleList

    def printRules(self, ruleList):
        for rule in ruleList:
            print(rule)