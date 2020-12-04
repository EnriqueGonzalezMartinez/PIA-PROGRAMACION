import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n1", dest="num1", type=int, required=True)
parser.add_argument("-a", dest="altura", type=int)
parser.add_argument("-b", dest="base", type=int)
params = parser.parse_args()

if(params.num1 == 1 and params.altura != None):
    print(f'-n1: {params.num1}\t-a: {params.altura}')
elif(params.num1 == 2 and params.base != None):
    print(f'-n1: {params.num1}\t-b: {params.base}')
else:
    print('Uno de los parametros requeridos no fue ingresado, intente de nuevo.')