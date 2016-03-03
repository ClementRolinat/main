from random import randint
import time
from math import *

def potentiel(x,y,vitesse,ecosysteme):
    xp=x
    yp=y
    score=0
    for i in range(-vitesse,vitesse+1):
        for j in range (-vitesse,vitesse+1):
            coord=(x+i,y+j)
            s=0
            for an in ecosysteme:
                d=sqrt((an.x-coord[0])**2+(an.y-coord[1])**2)
                if d<2:
                    if d!=0:
                        s+=-1/d # fait baisser le score si le point testé est trop près d'autres animaux
                else:
                    s+=1/d # augmente le score sinon
            if s>score:
                score=s
                xp=coord[0]
                yp=coord[1]
    return xp,yp


def signnourriture(x,y,d): #Fonction pour se rapprocher de la nourriture
    if x>map.limiteDN:
        if y>map.limiteHN:
            return -d,-d
        elif y<map.limiteBN:
            return -d,d
        else:
            return -d,0
    elif x<map.limiteGN:
        if y>map.limiteHN:
            return d,-d
        elif y<map.limiteBN:
            return d,d
        else:
            return d,0
    else:
        if y>map.limiteHN:
            return 0,-d
        elif y<map.limiteBN:
            return 0,d
        else:
            return 0,0


def signeau(x,y,d): #Fonction pour se rapprocher de l'eau
    if x>map.limiteDE:
        if y>map.limiteHE:
            return -d,-d
        elif y<map.limiteBE:
            return -d,d
        else:
            return -d,0
    elif x<map.limiteGE:
        if y>map.limiteHE:
            return d,-d
        elif y<map.limiteBE:
            return d,d
        else:
            return d,0
    else:
        if y>map.limiteHE:
            return 0,-d
        elif y<map.limiteBE:
            return 0,d
        else:
            return 0,0
        
def coordTroupeau(ecosysteme):
    x=0
    y=0
    for an in ecosysteme:
        x+=an.x
        y+=an.y
    return int(x/len(ecosysteme)),int(y/len(ecosysteme))

def coordHerbivore(cH,cC,d):
    if cC>cH:
        return -d
    elif cC<cH:
        return d
    else:
        return 0

def coordCarnivore(cC,cH,d):
    if cH>cC:
        return d
    elif cH<cC:
        return -d
    else:
        return 0
    

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





class Animal(object):
    def __init__(self,abscisse,ordonnee,rapidite,cEau=30,cNourriture=30):
        self.x=abscisse
        self.y=ordonnee
        self.xp=abscisse # abscisse prévue, initialisée arbitrairement
        self.yp=ordonnee # ordonnée prévue, initialisée arbitrairement
        self.vitesse=rapidite
        self.eEau=randint(cEau//2, cEau) # état eau
        self.eNourriture=randint(cNourriture//2, cNourriture) # état nourriture
        self.maxEau=cEau
        self.maxNourriture=cNourriture
        
    @property
    def x(self):
        return self.__x
        
    @x.setter
    def x(self,abscisse):
        if abscisse>map.limitex:
            self.__x=map.limitex
        elif abscisse<-map.limitex:
            self.__x=-map.limitex
        else:
            self.__x=abscisse
        
            
    @property
    def y(self):
        return self.__y
        
    @y.setter
    def y(self,ordonnee):
        if ordonnee>map.limitey:
            self.__y=map.limitey
        elif ordonnee<-map.limitey:
            self.__y=-map.limitey
        else:
            self.__y=ordonnee
        
    @property
    def xp(self):
        return self.__xp
        
    @xp.setter
    def xp(self,abscisse):
        if abscisse>map.limitex:
            self.__xp=map.limitex
        elif abscisse<-map.limitex:
            self.__xp=-map.limitex
        else:
            self.__xp=abscisse
            
    @property
    def yp(self):
        return self.__yp
        
    @yp.setter
    def yp(self,ordonnee):
        if ordonnee>map.limitey:
            self.__yp=map.limitey
        elif ordonnee<-map.limitey:
            self.__yp=-map.limitey
        else:
            self.__yp=ordonnee
            
    def boire(self):
        self.eEau=self.maxEau
    
    def manger(self):
        self.eNourriture=self.maxNourriture
        
    def bouger(self,ecosysteme):
        for an in ecosysteme:
            if an.x!=self.x or an.y!=self.y or an.xp!=self.xp or an.yp!=self.yp or an.eEau!=self.eEau or an.eNourriture!=self.eNourriture:
                if self.xp==an.x and self.yp==an.y: 
                    if an.x==an.xp and an.y==an.yp: # on vérifie si l'animal dont on prend la place est à sa place finale
                        if self.x<=an.x: # le cas d'égalité n'est normalement pas possible
                            self.xp=self.xp-randint(0,2)
                        if self.x>an.x:
                            self.xp=self.xp+randint(0,2)
                        if self.y<=an.y: # le cas d'égalité n'est normalement pas possible
                            self.yp=self.yp-randint(0,2)
                        if self.y>an.y:
                            self.yp=self.yp+randint(0,2)
                        self.bouger(ecosysteme)
                        break
            else:
                self.x=self.xp
                self.y=self.yp
        
    def __str__(self):
        return "%c : position (%i, %i) etat_eau %i/%i etat_nourriture %i/%i"%(self.car(), self.x, self.y, self.eEau, self.maxEau, self.eNourriture, self.maxNourriture)
        

    def afaim(self):
        return self.eNourriture<=10
    
    def asoif(self):
        return self.eEau<=10
        
    def mort(self):
        return self.eEau <=0 or self.eNourriture <=0
    
class Herbivore(Animal):
    def __init__(self,abscisse,ordonnee,rapidite=4):
        super().__init__(abscisse,ordonnee,rapidite)
        
    def car(self):
        return ('H')
        
    def decider(self,ecosysH,ecosysC):
        self.eNourriture -= 1
        self.eEau-=1
        dHC=2*(2*map.limitex)^2
        #On regarde à quelle distance sont les carnivores
        if len(ecosysC)>0:#si il y'a au moins un carnivore, l'herbivore peut prendre la fuite            
            xC=ecosysC[0].x
            yC=ecosysC[0].y
            for an in ecosysC:
                d=sqrt((an.x-self.x)**2+(an.y-self.y)**2)
                if d<dHC:
                    xC=an.x
                    yC=an.y
                    dHC=d
                    
        if dHC<6: #si le carnivore est àmoins de 6 (de distance), alors l'herbivore fuit.
            self.xp = self.x + coordCarnivore(xC,self.x,self.vitesse)
            self.yp = self.y + coordCarnivore(yC,self.y,self.vitesse)
        else: #Si l'herbivore ne prend pas la fuite, on regarde si il a faim ou soif
            if self.afaim() or self.asoif(): # teste si il a faim ou soif
                if map.position(self.x,self.y)==1: # si il est dans la zone ou il peut boire, il boit
                    self.boire()
                    print("J'ai bu")
                if map.position(self.x,self.y)==2: # si il est dans la zone ou il peut manger, il mange
                    self.manger()
                    print("j'ai mangé")
                if self.afaim() or self.asoif(): # teste de nouveau si il a faim ou soif
                    if self.eNourriture-self.eEau>=0: # si il a plus soif que faim, il va boire
                        self.xp = self.x + signeau(self.x,self.y,self.vitesse//2)[0] #j'ai mis self.vitesse//2 pour que si on a besoin de le faire "courrir", on ai juste à mettre self.vitesse, pour fuir un prédateur par exemple
                        self.yp = self.y + signeau(self.x,self.y,self.vitesse//2)[1]
                    else: # si il a plus faim que soif, il va manger
                        self.xp = self.x + signnourriture(self.x,self.y,self.vitesse//2)[0]
                        self.yp = self.y + signnourriture(self.x,self.y,self.vitesse//2)[1]
            if len(ecosysH)>1 and not self.afaim() and not self.asoif(): # si il a ni faim ni soif, il cherche à se rapprocher des autres herbivore
                self.xp,self.yp = potentiel(self.x,self.y,self.vitesse//2,ecosysH)

                # if coordTroupeau(ecosysH)[0]>self.x:
                #     self.xp = self.x + self.vitesse//2
                # elif coordTroupeau(ecosysH)[0]<self.x:
                #     self.xp = self.x - self.vitesse//2
                # else:
                #     self.xp = self.x
                # if coordTroupeau(ecosysH)[1]>self.y:
                #     self.yp = self.y + self.vitesse//2
                # elif coordTroupeau(ecosysH)[1]<self.y:
                #     self.yp = self.y - self.vitesse//2
                # else:
                #     self.yp = self.y
            if len(ecosysH)==1 and not self.afaim() and not self.asoif():
                self.xp = self.x + randint(-self.vitesse//2, self.vitesse//2)
                self.yp = self.y + randint(-self.vitesse//2, self.vitesse//2)

        

class Carnivore(Animal):
     def __init__(self,abscisse,ordonnee,rapidite=6):
        super().__init__(abscisse,ordonnee,rapidite)
        
     def car(self):
        return "C"
    
     def decider(self,ecosysH,ecosysC):
         self.eNourriture -= 1
         self.eEau-=1
         if len(ecosysH)>0:#si il y'a au moins un herbivore, on cherche l'herbivore le plus proche
             proie=ecosysH[0]
             dHC=sqrt((ecosysH[0].x-self.x)**2+(ecosysH[0].y-self.y)**2)
             xH=ecosysH[0].x
             yH=ecosysH[0].y
             for an in ecosysH:
                 d=sqrt((an.x-self.x)**2+(an.y-self.y)**2)
                 if d<dHC :
                     proie=an
                     xH=an.x
                     yH=an.y
                     dHC=d
             if self.asoif()or self.afaim(): # teste si il a soif ou soif
                 if self.eNourriture-self.eEau>=0: # si il a plus soif que faim, il regarde si il peut boire
                    if map.position(self.x,self.y)==1: # si il est dans la zone ou il peut boire, il boit
                        self.boire()
                        print("J'ai bu")
                 else: #si il a plus faim que soif, il regarde si il peut manger
                     if dHC<2: # si il est proche d'un herbivore, il le mange
                        ecosys.remove(proie)
                        self.manger()
                 if self.afaim() or self.asoif(): # teste de nouveau si il a faim ou soif
                     if self.eNourriture-self.eEau>=0: # si il a plus soif que faim, il va boire
                         self.xp = self.x + signeau(self.x,self.y,self.vitesse//2)[0]
                         self.yp = self.y + signeau(self.x,self.y,self.vitesse//2)[1]
                     else:# si il a plus faim que soif, il va manger
                         if dHC>4:
                             self.xp = self.x + coordHerbivore(xH,self.x,self.vitesse//2)
                             self.yp = self.y + coordHerbivore(yH,self.y,self.vitesse//2)
                         else:
                             self.xp = self.x + coordHerbivore(xH,self.x,self.vitesse)
                             self.yp = self.y + coordHerbivore(yH,self.y,self.vitesse)
             if not self.afaim() and not self.asoif(): #si il n'a ni faim ni soif, il se déplace aléatoirement
                 self.xp = self.x + randint(-self.vitesse//2, self.vitesse//2)
                 self.yp = self.y + randint(-self.vitesse//2, self.vitesse//2)
        
         else: #il n'y a plus d'herbivore
            if self.asoif():
                if map.position(self.x,self.y)==1: # si il est dans la zone ou il peut boire, il boit
                    self.boire()
                    print("J'ai bu")
                if self.asoif():
                    self.xp = self.x + signeau(self.x,self.y,self.vitesse//2)[0]
                    self.yp = self.y + signeau(self.x,self.y,self.vitesse//2)[1]
            else:
                self.xp = self.x + randint(-self.vitesse//2, self.vitesse//2)
                self.yp = self.y + randint(-self.vitesse//2, self.vitesse//2)

# comme les deux types de carnivores auront des comportements assez différents, ça peut être bien d'avoir 2 classes ?        
class Meute(Carnivore):
    def __init__(self,abscisse,ordonnee):
        super().__init__(abscisse,ordonnee)

        
class Solitaire(Carnivore):
    def __init__(self,abscisse,ordonnee):
        super().__init__(abscisse,ordonnee)
        
        
class Ecosysteme(list): #Affiche la carte, l'eau, la nourriture et les annimaux
    def __init__(self, nbanH, nbanC):
        for i in range(nbanH): #Liste avec d'abord tout les Herbivores
            self.append(Herbivore(randint(-map.limitex, map.limitex), randint(-map.limitey, map.limitey)))
        for i in range(nbanC): #La suite de la liste est composé des carnivores
            self.append(Carnivore(randint(-map.limitex, map.limitex), randint(-map.limitey, map.limitey)))
                
    def __str__(self):
        pos = {}
        for an in self:
            pos[(an.x, an.y)]=an.car()
        s = ""
        for j in range(map.limitey,-map.limitey-1, -1):
            for i in range(-map.limitex, map.limitex+1):
                if (i, j) in pos:
                    s += pos[(i,j)]
                elif map.position(i,j)==1:
                    s += "~"
                elif map.position(i,j)==2:
                    s += '"'
                else:
                    s += "."
            s += "\n"
        return s  
        
    def enterrer(self):
        morts=[]
        for an in self:
            if an.mort():
                print('Enterré : '+str(an))
                morts.append(an)
        for an in morts:
            ecosys.remove(an)

    def nbAnnimaux(self):
        nbH = 0
        nbC = 0
        for an in self:
            if an.car()=='H':
                nbH += 1
            elif an.car()=='C':
                nbC += 1
        return nbH, nbC           


if __name__ == "__main__":

    map=Terrain(30,20,(0,0),6,(0,0),12)
    ecosysH = []
    ecosysC = []
    nbH = 4
    nbC=0
    nbtour = 40
    ecosys=Ecosysteme(nbH,nbC)

   
    for t in range(nbtour):
        ecosysH = []
        ecosysC = []
        nbH, nbC = ecosys.nbAnnimaux()
        for i in range(nbH): #Liste avec que les Herbivores
            ecosysH.append(ecosys[i])
        for i in range(nbH,nbC+nbH): #Liste avec que les carnivores
            ecosysC.append(ecosys[i])
            
        print("### Tour %i ###"%(t))
        
        for an in ecosysH: #On fait décider tout les Herbivores
            an.decider(ecosysH,ecosysC)
        for an in ecosysC: #On fait décider tout les Carnivores
            an.decider(ecosysH,ecosysC)
        ecosys.enterrer() #Verifie qui est mort et le supprime
        for an in ecosys: 
            an.bouger(ecosys)
            print(an)
        
        print(ecosys)
        time.sleep(1)
        