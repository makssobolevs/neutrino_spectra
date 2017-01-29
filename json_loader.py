import json

# from parsing.fission_yields import export_filename as yields_base_filename
# from parsing.symbols_qmax import export_filename as yields_symbols_qmax_filename


with open("dumps/yields_basic.json", "r") as file:
    yields_base = json.load(file)

if __name__ == "__main__":
    with open('parsing/dumps/yields_symbols_qmax.json', 'r') as file:
        yields = json.load(file)
        for el in yields:
            print(el)


