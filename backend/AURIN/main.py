"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

import json
import sys

#check that value is a number
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def main(file, key_col):
    MELBOURNE_LGAS = [25340, 21450, 21610, 22170, 22670, 23430, 20910, 22310, 24970, 25900, 26350, 23670,
                                   27450, 27350, 21110, 26980, 24410, 21890,
                                   20660, 24210, 25710, 27070, 24850, 25620, 24600, 25250, 23270, 24130, 25150, 27260,
                                   24650, 23110, 21180, 23270, 25060, 24330]
    SYDNEY_LGAS = [18550, 13100, 14000, 16370, 18000, 14500, 17420, 13800, 10750, 16350, 10900, 14900,
                                18400, 16100, 11500, 11450, 17150, 10750, 12850,
                                13950, 16250, 10350, 16700, 14100, 14700, 18250, 15950, 15350, 15150, 10200, 11520,
                                14800, 17200, 18500, 18050, 16550, 11100, 16650,
                                14450, 14150, 17100, 11550, 11300, 10150, 15200]
    lga_to_name = {}
    #for each location, map location name to lga_code for extendibility
    for pair in [("Melbourne",MELBOURNE_LGAS),("Sydney",SYDNEY_LGAS)]:
        name = pair[0]
        lgas = pair[1]
        for lga in lgas:
            lga_to_name[lga] = name
    #result aggregate data from the same location and stores distribution of data
    result = {"Melbourne":{"n":0},"Sydney":{"n":0}}

    with open(file) as f:
        data = json.load(f)
    for row in data['features']:
        lga = int(row['properties'][key_col])
        if lga not in lga_to_name:
            continue
        location = lga_to_name[lga]
        for key, value in row['properties'].items():
            #properties include all attributes excluding key_col
            if key == key_col:
                continue
            if key not in result[location]:
                result[location][key] = 0
            #numeric values are summed
            if is_number(value):
                result[location][key] += value
        result[location]["n"] += 1
    for location in result:
        n = result[location]["n"]
        if n != 0:
            for feature in result[location]:
                if feature != "n":
                    #calculate average of numeric values
                    result[location][feature] = round(result[location][feature]/n, 2)
        print(result[location])

    with open('result-' + file,'w') as outfile:
        json.dump(result, outfile)
    return

if __name__ == "__main__":
   main(sys.argv[1], sys.argv[2])
