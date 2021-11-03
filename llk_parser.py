from abc import ABC, abstractmethod
from typing import List, Match

######################################
# CLASSE:  TOKEN                      #
######################################
class Token:
    def __init__(self, type, text, index):
        self.type = type
        self.text = text
        self.index = index

    def toString(self):
        token_name = ListLexer.tokenNames[self.type]
        return f"<'{self.text}', {token_name}, '{self.index}'>"

    def __str__(self) -> str:
        token_name = ListLexer.tokenNames[self.type]
        return f"<'{self.text}', {token_name}, '{self.index}'>"
    


######################################
# CLASS:  LEXER                      #
######################################
class Lexer(ABC):
    EOF = -1
    EOF_TYPE = 1
    carattere_corrente = 0
    carattere = ""

    def __init__(self, input) -> None:
        self.input = input
        self.carattere = self.input[self.carattere_corrente]
    
    def consume(self) -> None:
        self.advance()
        self.WS()
    
    def advance(self):
        self.carattere_corrente += 1
        if self.carattere_corrente >= len(self.input):
            self.carattere = self.EOF
        else:
            self.carattere = self.input[self.carattere_corrente]

    def match(self, x) -> None:
        if self.carattere == x:
            self.consume()
        else:
            raise Exception("Atteso " + str(x) + "; era " + str(self.carattere))

    @abstractmethod
    def nextToken(self):
        pass

    @abstractmethod
    def WS(self):
        pass

    @abstractmethod
    def getTokenName(self, tokenType):
        pass



######################################
# CLASS:  LISTLEXER                  #
######################################
class ListLexer(Lexer):
    NAME = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5
    ASSIGNEMENT = 6
    DIGIT = 7
    tokenNames = ['n/a', '<EOF>', 'NAME', 'COMMA', 'LBRACK', 'RBRACK', 'ASSIGNEMENT', 'DIGIT']
    lettere = "abcdefghijklmnopqrstuvwxyz"
    numeri = "0123456789"

    def __init__(self, input) -> None:
        super().__init__(input)
    
    def isLETTER(self) -> bool:
        if self.carattere in self.lettere or self.carattere in self.lettere.upper():
            return True
        else:
            return False

    def isNUMBER(self) -> bool:
        if self.carattere in self.numeri:
            return True
        else:
            return False

    def getTokenName(self, x):
        return super().getTokenName(x)
        #return ListLexer.tokenNames[x]

    def nextToken(self) -> Token:
        #return super().nextToken()
        while self.carattere != self.EOF:
            if self.carattere in [' ', '\t', '\n', '\r']:
                self.WS()
            elif self.carattere == ',':
                self.consume()
                return Token(self.COMMA, ',', self.carattere_corrente)
            elif self.carattere == '[':
                self.consume()
                return Token(self.LBRACK, '[', self.carattere_corrente)
            elif self.carattere == ']':
                self.consume()
                return Token(self.RBRACK, ']', self.carattere_corrente)
            elif self.carattere == '=':
                self.consume()
                return Token(self.ASSIGNEMENT, '=', self.carattere_corrente)
            else:
                if self.isLETTER():
                    return self.Name()
                elif self.isNUMBER():
                    return self.Numeric()
                else:
                    raise Exception("Carattere non valido " + str(self.carattere))

        return Token(self.EOF_TYPE, '<EOF>', self.carattere_corrente + 1)

    def Name(self) -> Token:
        buf = ""
        while self.isLETTER():
            buf += self.carattere
            self.LETTER()
        
        return Token(self.NAME, buf, self.carattere_corrente)
    
    def Numeric(self) -> Token:
        buf = ""
        while self.isNUMBER():
            buf += str(self.carattere)
            self.NUMBER()
        
        return Token(self.DIGIT, buf, self.carattere_corrente)
    
    def LETTER(self):
        if self.isLETTER():
            self.consume()
        else:
            raise Exception("Atteso LETTER; trovato " + str(self.carattere))

    def NUMBER(self):
        if self.isNUMBER():
            self.consume()
        else:
            raise Exception("Atteso NUMBER; trovato " + str(self.carattere))

    def WS(self):
        while self.carattere in [' ', '\t', '\n', '\r']:
            self.advance()



######################################
# CLASS:  PARSER                     #
######################################
class Parser(ABC):
    def __init__(self, input) -> None:
        self.input = input
        self.lookahead = []
        self.k = 2
        self.p = 0

        for i in range(1, self.k + 1):
            self.lookahead_buffer()

    def lookahead_buffer(self) -> None:
        token = self.input.nextToken()
        self.lookahead.append(token)
        #print(self.lookahead[self.p].text)
        self.p = (self.p + 1) % self.k

    def consume(self) -> None:
        token = self.input.nextToken()
        self.lookahead[self.p] = token
        #print(self.lookahead[self.p].text)
        self.p = (self.p + 1) % self.k
        
    def LT(self, i) -> Token:
        return self.lookahead[(self.p + i - 1) % self.k]
    
    def LA(self, i):
        return self.LT(i).type
    
    def match(self, x):
        if self.LA(1) == x:
            self.consume()
        else:
            raise Exception("Atteso " + self.input.getTokenName(x) + "; trovato " + self.LT(1).toString())
    


######################################
# CLASS:  LISTPARSER                 #
######################################
class ListParser(Parser):
    def __init__(self, input) -> None:
        super().__init__(input)
        self.elema = ""
        self.elemb = ""

    def list(self):
        self.elema = self.lookahead[self.p].text
        self.match(ListLexer.LBRACK)
        self.translator(ListLexer.LBRACK, self.elema, self.elemb)
        self.elements()
        self.elema = self.lookahead[self.p].text
        self.match(ListLexer.RBRACK)
        self.translator(ListLexer.RBRACK, self.elema, self.elemb)

    def elements(self):
        self.element()
        while self.LA(1) == ListLexer.COMMA:
            self.match(ListLexer.COMMA)
            self.element()
    
    def element(self):
        if self.LA(1) == ListLexer.NAME and self.LA(2) == ListLexer.ASSIGNEMENT:
            self.elema = self.lookahead[self.p].text
            self.match(ListLexer.NAME)
            self.match(ListLexer.ASSIGNEMENT)
            self.elemb = self.lookahead[self.p].text
            
            if self.lookahead[self.p].type == ListLexer.NAME:
                self.match(ListLexer.NAME)
            elif self.lookahead[self.p].type == ListLexer.DIGIT:
                self.match(ListLexer.DIGIT)
            
            self.translator(ListLexer.ASSIGNEMENT, self.elema, self.elemb)
        elif self.LA(1) == ListLexer.NAME:
            self.elema = self.lookahead[self.p].text
            self.match(ListLexer.NAME)

            self.translator(ListLexer.NAME, self.elema, self.elemb)
        elif self.LA(1) == ListLexer.DIGIT:
            self.elema = self.lookahead[self.p].text
            self.match(ListLexer.DIGIT)

            self.translator(ListLexer.DIGIT, self.elema, self.elemb)
        elif self.LA(1) == ListLexer.LBRACK:
            self.list()
        else:
            raise Exception("Atteso NAME o LIST; trovato " + self.LT(1).toString())
    
    def translator(self, type, elementA, elementB):
        if type == ListLexer.ASSIGNEMENT:
            if str.isalpha(elementB):
                print(f"Assegna alla Variabile '{elementA.upper()}' il valore della variabile '{elementB.upper()}'")
            else:
                print(f"Assegna alla Variabile '{elementA.upper()}' il valore {elementB}")
        elif type == ListLexer.NAME:
            print(f"Alla Variabile '{elementA.upper()}' non è stato assegnato alcun valore")
        elif type == ListLexer.LBRACK:
            print(f"Aperta parentesi {elementA}")
        elif type == ListLexer.RBRACK:
            print(f"Chiusa parentesi {elementA}")
        elif type == ListLexer.DIGIT:
            print(f"Il Numero {elementA} non è assegnato ad alcuna variabile")
