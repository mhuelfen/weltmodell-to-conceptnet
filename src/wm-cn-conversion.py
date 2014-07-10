# encoding: utf-8

'''
Script to convert the weltmodell into the conceptnet.

@author: Michael A. Huelfenhaus
'''
import sys
import json
import csv
import re

from getopt import getopt, GetoptError



help_message = '''
usage: python eval_with_api.py <question_tsv_file> <wikia_name>

This is what this script does when called from shell.

params:
    question_tsv_file : tsv file Format: question\tanswer
    wikia_name : e.g. simpsons, star-trek, wookieepedia

'''

context = '/ctx/all'
base_concept_url = '/c/en/'
base_rel_url = '/r/'
source_uri = '/s/site/weltmodell'
dataset = '/d/weltmodell'
license = ''

def make_json_line(wm_line):


    uri = '/a/[' + rel + ',' + start + ',' + end + ']'

    norm_pmi = 0
    weight = norm_pmi

    # TODO add all verbargs to surface text
    surface_text = ''

    #make json line
    json_line = ''

    # make id
    identity = ''

def convert_wm(wm_path, result_path):
     # read wm file
    with open(wm_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            # filter for binary relations
            print row

if __name__ == "__main__":
    '''
    This block is called when the .py file is started from the shell
    '''
    
    # checking command line options
    try:
        options, args = getopt(sys.argv[1:], "")
    except GetoptError:
        print >> sys.stderr, help_message
        sys.exit(2)
    
    # checking number of params     
    if len(args) != 2:
        print >> sys.stderr, help_message
        sys.exit(2)

    wm_path = args[0]
    result_path = args[1]

    convert_wm(wm_path, result_path)