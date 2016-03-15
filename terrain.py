# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 21:42:50 2016

@author: Clément
"""

class Terrain(object):
    def __init__(self,limitex,limitey,coordE,tailleE,coordN,tailleN):

        self.limitex=limitex
        self.limitey=limitey

        self.limiteGE=coordE[0]-tailleE#limite gauche eau
        self.limiteDE=coordE[0]+tailleE#limite droite eau
        self.limiteHE=coordE[1]+tailleE#limite haute eau
        self.limiteBE=coordE[1]-tailleE#limite basse eau

        self.limiteGN=coordN[0]-tailleN#limite gauche nourriture
        self.limiteDN=coordN[0]+tailleN#limite droite nourriture
        self.limiteHN=coordN[1]+tailleN#limite haute nourriture
        self.limiteBN=coordN[1]-tailleN#limite basse nourriture



    @property
    def limiteGE(self):
        return self.__limiteGE

    @limiteGE.setter
    def limiteGE(self,e):
        if e>self.limitex:
            self.__limiteGE=None
        elif e<-self.limitex:
            self.__limiteGE=-self.limitex
        else:
            self.__limiteGE=e

    @property
    def limiteDE(self):
        return self.__limiteDE

    @limiteDE.setter
    def limiteDE(self,e):
        if e>self.limitex:
            self.__limiteDE=self.limitex
        elif e<-self.limitex:
            self.__limiteDE=None
        else:
            self.__limiteDE=e

    @property
    def limiteHE(self):
        return self.__limiteHE

    @limiteHE.setter
    def limiteHE(self,e):
        if e>self.limitey:
            self.__limiteHE=self.limitey
        elif e<-self.limitey:
            self.__limiteHE=None
        else:
            self.__limiteHE=e

    @property
    def limiteBE(self):
        return self.__limiteBE

    @limiteBE.setter
    def limiteBE(self,e):
        if e>self.limitey:
            self.__limiteBE=None
        elif e<-self.limitey:
            self.__limiteBE=-self.limitey
        else:
            self.__limiteBE=e


    @property
    def limiteGN(self):
        return self.__limiteGN

    @limiteGN.setter
    def limiteGN(self,n):
        if n>self.limitex:
            self.__limiteGN=None
        elif n<-self.limitex:
            self.__limiteGN=-self.limitex
        else:
            self.__limiteGN=n

    @property
    def limiteDN(self):
        return self.__limiteDN

    @limiteDN.setter
    def limiteDN(self,n):
        if n>self.limitex:
            self.__limiteDN=self.limitex
        elif n<-self.limitex:
            self.__limiteDN=None
        else:
            self.__limiteDN=n

    @property
    def limiteHN(self):
        return self.__limiteHN

    @limiteHN.setter
    def limiteHN(self,n):
        if n>self.limitey:
            self.__limiteHN=self.limitey
        elif n<-self.limitey:
            self.__limiteHN=None
        else:
            self.__limiteHN=n

    @property
    def limiteBN(self):
        return self.__limiteBN

    @limiteBN.setter
    def limiteBN(self,n):
        if n>self.limitey:
            self.__limiteBN=None
        elif n<-self.limitey:
            self.__limiteBN=-self.limitey
        else:
            self.__limiteBN=n


    def position(self,x,y):
        if (self.limiteGE is not None) and (self.limiteDE is not None) and (self.limiteHE is not None) and (self.limiteBE is not None):
            if ((x >= self.limiteGE) and (x <= self.limiteDE)) and ((y >= self.limiteBE) and (y <= self.limiteHE)):
                return 1
        if (self.limiteGN is not None) and (self.limiteDN is not None) and (self.limiteHN is not None) and (self.limiteBN is not None):
            if ((x >= self.limiteGN) and (x <= self.limiteDN)) and ((y >= self.limiteBN) and (y <= self.limiteHN)):
                return 2
        return 0
