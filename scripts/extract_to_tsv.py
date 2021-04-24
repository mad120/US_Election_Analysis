"""
Author: Abdullatif Hassan
Date Started: November 18, 2020
"""

import random
import pandas as pd
import sys
import os
import json
import argparse

def make_tsv(names, titles, output_file):
    output_file.write("Name\ttitle\tcoding\n")
    for i in range(len(names)):
        output_file.write(names[i])
        output_file.write("\t")
        output_file.write(titles[i])
        output_file.write("\t")
        output_file.write("\n")

def get_names_and_titles(input_file, num):
    if(int(num)<len(input_file)):
        input_file = random.sample(input_file, int(num))
    names = []
    titles = []
    for line in input_file:
        data = json.loads(line)
        title = data["data"]["title"]
        name = data["data"]["name"]
        names.append(name)
        titles.append(title)
    return names, titles

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help = 'Enter Output File', required = True)
    parser.add_argument("input_json")
    parser.add_argument("num_posts")
    args = parser.parse_args()
    mock_output = open(args.o, 'w')
    mock_output.close()
    output_file = open(args.o, 'a')
    json_file = open(args.input_json, 'r').readlines()
    names, titles = get_names_and_titles(json_file, args.num_posts)
    make_tsv(names, titles, output_file)

if __name__ == '__main__':
    main()
