# Sistema de cálculo de nómina mensual
data = [
    {"i": 1, "n": "Carlos", "t": "FT", "h": 160, "d": 2},
    {"i": 2, "n": "Ana", "t": "PT", "h": 80, "d": 0},
    {"i": 3, "n": "Luis", "t": "C", "h": 100, "d": 5}
]

l = []

def process_payroll(d, m):
    global l
    for x in d:
        if x['t'] == "FT":
            s = x['h'] * 25
            if x['d'] == 0:
                s = s + 200
            elif x['d'] <= 2:
                s = s + 100
            else:
                s = s - 50
            
            if m == "Jan" or m == "Dec":
                s = s - (s * 0.1)
            else:
                s = s - (s * 0.15)
            
            res = "ID:" + str(x['i']) + " Name:" + x['n'] + " Pay:" + str(s)
            l.append(res)
            print("Processed FT: " + x['n'])

        elif x['t'] == "PT":
            s = x['h'] * 15
            if x['d'] == 0:
                s = s + 100
            elif x['d'] <= 2:
                s = s + 50
            else:
                s = s - 25
            
            if m == "Jan" or m == "Dec":
                s = s - (s * 0.1)
            else:
                s = s - (s * 0.15)
            
            res = "ID:" + str(x['i']) + " Name:" + x['n'] + " Pay:" + str(s)
            l.append(res)
            print("Processed PT: " + x['n'])

        elif x['t'] == "C":
            s = x['h'] * 30
            if m == "Jan" or m == "Dec":
                s = s - (s * 0.05)
            else:
                s = s - (s * 0.05)
            
            res = "ID:" + str(x['i']) + " Name:" + x['n'] + " Pay:" + str(s)
            l.append(res)
            print("Processed C: " + x['n'])
        else:
            print("Unknown type")
    
    try:
        f = open("payroll_output.txt", "w")
        for item in l:
            f.write(item + "\n")
        f.close()
    except:
        print("Error writing")

process_payroll(data, "Jan")