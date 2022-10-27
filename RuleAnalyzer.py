import argparse
import logging
import os
import pyfiglet

def openFile(filename):
    lineArray = []
    with open("./data/"+filename) as file:
        lineArray = file.readlines()
    return lineArray

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Natural Lang Processor")
    print("#########################################################")
    print(ascii_banner)
    print("#########################################################")
    logging.basicConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', '-n', type=str, help='Name of data file')
    
    args = parser.parse_args()

    document = openFile(args.name)

