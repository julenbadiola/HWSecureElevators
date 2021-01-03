def RepresentsInt(s):
    try:
      int(s)
      #print(f"{s} is int")
      return True
    except ValueError:
      return False


def RepresentsOther(s):
    strs = ["primer", "segundo", "tercer", "cuarto", "quinto",
            "sexto", "séptimo", "octavo", "noveno", "décimo", "undécimo"]
    try:
        str(s)
        if s in strs:
            #print(f"{s} in other")
            return strs.index(s) + 1

    except ValueError:
        return None


def Text2Int(textnum, numwords={}):
    if RepresentsInt(textnum):
        return int(textnum)

    res = RepresentsOther(textnum)
    if res is not None:
        return res

    if not numwords:
        units = [
            "cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho",
            "nueve", "diez", "once", "doce", "trece", "catorce", "quince",
            "dieciseis", "diecisiete", "dieciocho", "diecinueve",
        ]

        tens = ["", "", "veinte", "treinta", "cuarenta",
                "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]

        scales = ["cientos", "mil", "millones", "billones", "trillones"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            #print(f"Illegal word {textnum}")
            return None

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    #print(f"{textnum} is {result + current}")
    return result + current
