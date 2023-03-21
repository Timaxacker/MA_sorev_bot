class date(object):
    def __init__(self):
        self.rand = 1

    def bin_(self, Inp=int):
        Out_Mas = []
        Ost = str(int(Inp % 2))
        Out_Mas.append(Ost)
        while Inp >= 2:
            Inp /= 2
            Ost = str(int(Inp % 2))
            Out_Mas.append(Ost)
        Out = ""
        while len(Out_Mas) > 0: Out += Out_Mas.pop()
        return int(Out)


    def pesvRandN(self):
        self.rand = (65539 * self.rand + 1) % 2147483648
        return self.rand


    def encrypt(self, args=list, lenBl=16, shifr=1, razdT="110111101", razdN="101111110", term="111111111"):
        tranStatusIn = {"Новичок": "N", "Опытный": "O", "Эксперт": "E"}
        tranLettersIn = {"а": "000000", "б": "000001", "в": "000010", "г": "000011", "д": "000100", "е": "000101",
                         "ё": "000110", "ж": "000111", "з": "001000", "и": "001001", "й": "001010", "к": "001011",
                         "л": "001100", "м": "001101", "н": "001110", "о": "001111", "п": "010000", "р": "010001",
                         "с": "010010", "т": "010011", "у": "010100", "ф": "010101", "х": "010110", "ц": "010111",
                         "ч": "011000", "ш": "011001", "щ": "011010", "ь": "011011", "ы": "011100", "ъ": "011101",
                         "е": "011110", "ю": "011111", "я": "100000", "N": "100001", "O": "100010", "E": "100011",
                         ".": "100100", ",": "100101"}
        self.rand = shifr
        outProm = ""
        for arg in args:
            typeArg = type(arg)
            if typeArg == str:
                if arg in tranStatusIn:
                    outProm += tranLettersIn[tranStatusIn[arg]]
                    outProm += razdT
                    continue
                for ch in arg:
                    if ch in tranLettersIn:
                        outProm += tranLettersIn[ch]
                outProm += razdT
            elif typeArg == int:
                outProm += str(self.bin_(arg))
                outProm += razdN
            else: return None
        outProm += term
        out = []
        prom = "0b"
        for ch in outProm:
            prom += ch
            if len(prom) == lenBl + 2:
                out.append(int(prom, 2) + self.pesvRandN())
                prom = "0b"
        if len(prom) > 2:
            out.append(int(prom, 2) + self.pesvRandN())
        return out


    def decrypt(self, textIn, lenBl=16, shifr=1, razdT="110111101", razdN="101111110", term="111111111"):
        if textIn is None: return None
        tranStatusFrom = {"N": "Новичок", "O": "Опытный", "E": "Эксперт"}
        tranLettersFrom = {"000000": "а", "000001": "б", "000010": "в", "000011": "г", "000100": "д", "000101": "е",
                           "000110": "ё", "000111": "ж", "001000": "з", "001001": "и", "001010": "й", "001011": "к",
                           "001100": "л", "001101": "м", "001110": "н", "001111": "о", "010000": "п", "010001": "р",
                           "010010": "с", "010011": "т", "010100": "у", "010101": "ф", "010110": "х", "010111": "ц",
                           "011000": "ч", "011001": "ш", "011010": "щ", "011011": "ь", "011100": "ы", "011101": "ъ",
                           "011110": "е", "011111": "ю", "100000": "я", "100001": "N", "100010": "O", "100011": "E",
                           "100100": ".", "100101": ","}
        text = ""
        self.rand = shifr
        for k in range(len(textIn) - 1):
            promP = str(self.bin_(textIn.pop(0) - self.pesvRandN()))
            prom = ""
            for i in range(lenBl - len(promP)):
                prom += "0"
            prom += promP
            text += prom
        text += str(self.bin_(textIn.pop(0) - self.pesvRandN()))
        text = list(text)
        razdT = list(razdT)
        razdN = list(razdN)
        term = list(term)
        prom = []
        promL = []
        out = []
        b = 0
        for k in range(9):
            promL.append(text[k])
        for k in range(len(text) - 9):
            if b > 0:
                b -= 1
                promL.append(text[k + 9])
                promL.pop(0)
                continue
            promL.append(text[k + 9])
            promL.pop(0)
            prom.append(text[k])
            if promL == razdT:
                promI = ""
                promOut = ""
                for i in prom:
                    promI += i
                    if len(promI) == 6:
                        if promI in tranLettersFrom:
                            try:
                                promOut += tranStatusFrom[tranLettersFrom[promI]]
                            except:
                                promOut += tranLettersFrom[promI]
                        promI = ""
                out.append(promOut)
                b = 9
                prom = []
            elif promL == razdN:
                promOut = "0b"
                for i in prom:
                    promOut += i
                out.append(int(promOut, 2))
                b = 9
                prom = []
            elif promL == term: break
        return out