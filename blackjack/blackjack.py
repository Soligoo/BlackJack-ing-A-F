
from random import *
#per dare un po di colore e aumentare la leggibilità per gli utenti che giocano
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"
#classe carta che verrà utilizzata nelle altre classi
class Carte:
    def __init__(self,seme,numero):
        self.seme = seme
        self.valore = numero
    def __str__(self):
        return f"{self.valore} di {self.seme}"
#classe del mazzo che contiene sia le carte sia le varie azioni possibili, n è il numero di mazzi che si vogliono utilizzare,
#tendenzialmente si usano 6 mazzi ma se ne possono usare quanti si vuole
class Mazzo:
    def __init__(self):
        n = 6
        semi = [LIGHT_RED+"cuori ♡"+END, LIGHT_RED+"quadri ♦"+END, LIGHT_WHITE+"fiori ♣"+END, LIGHT_WHITE+"picche ♤"+END]
        valore = [2,3,4,5,6,7,8,9,"J","Q","K","A"]
        self.carte = [Carte(seme,numero) for seme in semi for numero in valore] * n

    def mischia(self,n=1):
        for j in range(n): #mischia il mazzo n volte perché boh mi andava di metterlo
            shuffle(self.carte)

    def pesca(self): #pesca una carta
        return self.carte.pop()


    def __repr__(self):
        return "\n".join(str(carta)for carta in self.carte)

#classe madre persona che da le funzioni di base dei giocatori e del dealer
class Persona:
    def __init__(self,nome):
        self.nome = nome
        self.mano = []


    def pesca_persona(self,mazzo): #pesca una carta che poi viene aggiunta alla mano del giocatore o dealer
        self.mano.append(mazzo.pesca())

    def punteggio(self): #calcolare il punteggio della mano tenendo conto anche del fatto che l'asso puo essere un 1 o un 11
        punteggio = 0
        assi = 0
        for carta in self.mano:
            if carta.valore in ["J","Q","K"]:
                punteggio += 10
            elif carta.valore == "A":
                assi += 1
            else:
                punteggio += carta.valore

        for j in range(assi):
            if punteggio +11 <= 21:
                punteggio += 11
            else: punteggio += 1
        return punteggio





#classe giocatori con le varie azioni che ogni giocatore puo fare
class Giocatore(Persona):
    def __init__(self,nome):
        super().__init__(nome)
        self.crediti = 10000
        self.puntata = 0
        self.blackjack = False
        self.vittoria = False



    def punta(self, n): #permette di puntare n crediti
        self.puntata = n


    def conto(self): #autoesplicativa ma inutile
        print(CYAN+"crediti = "+str(self.crediti)+END)

    def raddoppia(self): #consente di raddoppiare cioè di raddoppiare la puntata iniziale e pescare una sola singola carta
        self.puntata *= 2



    def split(self): #nel caso si hanno due carte uguali in mano si puo decidere di dividere cioè giocare due mani insieme
        if len(self.mano) == 2 and (self.mano[0].numero == self.mano[1].numero):
            print(f"puoi eseguire uno split con le seguenti carte {self.mano}")
            mano1=[self.mano[0].numero]
            mano2=[self.mano[1].numero]
            return mano1,mano2

        else:
            print("Non puoi eseguire uno split con le seguenti carte")
            return None

    def vincita(self): #calcola quanto il giocatore abbia vinto o perso
        if self.blackjack: # il blackjack (le prime due carte che si ottengono fanno 21) viena pagato in modo diverso, non 1 a 1 ma 1 a 1.5
            self.crediti += (self.puntata*1.5)

        elif self.vittoria:
            self.crediti += self.puntata
        else:
            self.crediti -= self.puntata






    def __str__(self):
        mano_str = ", ".join(str(carta) for carta in self.mano)
        return f"{self.nome} ha in mano {mano_str}\npunteggio = {self.punteggio()}"

#dealer, classe esistente cosi è piu facile (per me) usarla dopo nel gioco
class Dealer(Persona):
    def __init__(self,nome):
        super().__init__(nome)


#classe del gioco contenente tutte le funzioni necessarie
class Gioco:
    def __init__(self,numero_giocatori=1):
        self.mazzo = Mazzo() #si crea un mazzo qui in modo che tutti i giocatori peschino da un unico mazzo
        self.mazzo.mischia(3)

        self.dealer = Dealer("Dealer")
        self.giocatori = [Giocatore(f"giocatore {i+1}") for i in range(numero_giocatori)] #cosi possono giocare più persone

    def puntate(self): #ottine l'ingresso delle puntate di tutti i giocatori prima che vengano distribuite le carte come dalle regole
        for giocatore in self.giocatori:
            if giocatore.crediti > 0:
                while True:
                    try:
                        print(f"----------\n{giocatore.nome}\n----------")
                        giocatore.conto()
                        x = int(input("inserisci quanto vuoi puntare "))
                        if x > giocatore.crediti or x <= 0:
                            print("puntata non valida, inserisci un valore tra 1 e il tuo saldo disponibile")
                        else:
                            giocatore.punta(x)
                            print(f"----------\n{giocatore.nome} ha puntato {x} crediti\n----------")
                            break
                    except ValueError:
                        print("input non valido inserisci un numero intero")
            else:
                print(f"{giocatore} ha finito i crediti, è {RED}fuori dai giochi!{END}")

    def prima_pescata(self): #vengono distribuite 2 carte a ogni giocatore come da regole
        for giocatore in self.giocatori:
            if giocatore.crediti > 0:
                giocatore.pesca_persona(self.mazzo)
                giocatore.pesca_persona(self.mazzo)

        self.dealer.pesca_persona(self.mazzo)
        self.dealer.pesca_persona(self.mazzo)

    def turno_giocatore(self,giocatore): #come si svolge il turno di gioco
        print(f"è il turno del {giocatore.nome}\n---")
        print(f"il dealer ha come carta scoperta il {self.dealer.mano[0]}\n------") #nel gioco il dealer mostra solo una carta
        while True:
            print(giocatore)
            if giocatore.punteggio == 21 and len(giocatore.mano) == 2: #quando un giocatore fa blackjack vince immediatamente e non puo chiedere carta, vale solo se lo si fa con le prime fue carte
                print(f"{GREEN}{ITALIC}{UNDERLINE}{giocatore.nome} ha fatto Blackjack!!{END}\n---------")
                giocatore.blackjack = True
                break
            scelta = input(f"puoi: \n{YELLOW}chiedere carta (C){END}\n{BLUE}stare(S){END}\n{GREEN}raddoppiare(R){END}\n").upper() # il giocatore sceglie l'azione che vuole eseguire
            if scelta == "C":
                giocatore.pesca_persona(self.mazzo)
                print(f"{giocatore.nome} ha pescato {giocatore.mano[-1]}")
                if giocatore.punteggio() > 21: #si vede se il giocatore ha sballato e se quindi ha perso
                    print(f"{giocatore.nome} ha {RED}sballato{END} con un punteggio di {giocatore.punteggio()}")
                    break
            elif scelta == "S":
                print(f"{giocatore.nome} ha deciso di {BLUE}stare{END}" )
                break
            elif scelta == "R" and len(giocatore.mano) == 2:
                print(f"{giocatore.nome} raddoppia" )

                if giocatore.crediti >= giocatore.crediti - giocatore.puntata:
                    giocatore.raddoppia()
                    giocatore.pesca_persona(self.mazzo)
                    print(f"{giocatore.nome} ha pescato {giocatore.mano[-1]}")
                    if giocatore.punteggio() > 21:  # si vede se il giocatore ha sballato e se quindi ha perso
                        print(f"{giocatore.nome} ha {RED}sballato{END} con un punteggio di {giocatore.punteggio()}")
                        break
                    break
                else:
                    print("crediti insufficienti")
                    continue


            else: #nel caso qualcuno non sappia leggere
                print(f"{RED}{UNDERLINE}scelta non valida{END}")


    def turno_dealer(self): #il dealer pesca fino a quando non fa almeno 17
        print("---------\nturno del dealer")
        while self.dealer.punteggio() < 17:
            print("il dealer pesca")
            self.dealer.pesca_persona(self.mazzo)
        print(f"il dealer finisce il turno con un punteggio di {self.dealer.punteggio()}\n---------")


    def vincitore(self): #qui si vede se il giocatore ha vinto o perso la sua puntata
        print("calcolo vincitore")
        pv = self.dealer.punteggio()
        if pv > 21:
            print(f"{GREEN}il dealer ha sballato, i giocatori ancora dentro il gioco vincono{END}\n---------")
            for giocatore in self.giocatori:
                if giocatore.punteggio() <= 21:
                    giocatore.vittoria= True
        else:
            for giocatore in self.giocatori:
                pg = giocatore.punteggio()

                if pg > 21:
                    print(f"{RED}{giocatore.nome} ha sballato con un punteggio di {pg}{END}\n---------")
                    giocatore.vittoria = False
                elif pg == pv:
                    print(f"{YELLOW}{giocatore.nome} ha pareggiato con il dealer{END}\n---------")
                    giocatore.puntata = 0
                elif pg > pv:
                    print(f"{GREEN}{giocatore.nome} ha vinto con un punteggio di {pg}{END}\n---------")
                    giocatore.vittoria = True
                else:
                    print(f"{RED}{giocatore.nome} ha perso contro il dealer con un punteggio di {pg} contro {pv}{END}\n---------")

    def calcolo_vincite(self): #qui si assegnano le vincite
        for giocatore in self.giocatori:
            giocatore.vincita()
            if giocatore.vittoria:
                print(f"{GREEN}{giocatore.nome} ha vinto {giocatore.puntata} crediti!!{END}\n---------")
            else:
                print(f"{RED}{giocatore.nome} ha perso {giocatore.puntata} crediti!!{END}\n---------")

    def azzero_mani(self): #toglie le carte in mano a ogni giocatore e al dealer
        for giocatore in self.giocatori:
            giocatore.mano = []
            giocatore.puntata = 0
        self.dealer.mano = []

    def logica_turno(self): #svolgimento del turno di gioco, tenuta in considerazione dei crediti del giocatore
        self.puntate()
        self.prima_pescata()

        for j in self.giocatori:
            if j.crediti >0:
                self.turno_giocatore(j)
            else:   continue

        self.turno_dealer()

        self.vincitore()

        self.calcolo_vincite()

        self.azzero_mani()




    def inizio(self): #funzione che da inizio al gioco, si possono scegliere diverse modalità
        while True:
            mod = input(f"""inserire: 
{UNDERLINE}N{END} per giocare ad un numero limitato di round 
{UNDERLINE}I{END} per infiniti round
{UNDERLINE}X{END} per uscire 
{UNDERLINE}R{END} per regole e buone pratiche di gioco\n""").upper()
            if mod== "N":
                while True: #tenuta in conto degli errori di ingresso degli utenti
                    try:
                        v = int(input("inserire il numero di round che si vuole giocare "))
                        break
                    except ValueError:
                        print("il numero di round non valido")

                for i in range(v):
                    print(f"---------\nRound {i+1}\n---------")
                    self.logica_turno()
                for j in self.giocatori:
                    print(f"{j.nome} finisce la partita con {j.crediti} crediti!")
                break

            elif mod == "I":
                while True:
                    self.logica_turno()
                    break
            elif mod == "X":
                print("arrivederci!")
                break
            else: #tenuta in conto degli errori di ingresso degli utenti
                print("input invalido")

def num_giocatori():

    while True:
        try:
            d = int(input("inserisci il numero di giocatori "))
            if d <= 0:
                print("inserire un numero di giocatori maggiore di 0")
                continue
            break
        except ValueError:
            print("inserire numero intero")
    return d
