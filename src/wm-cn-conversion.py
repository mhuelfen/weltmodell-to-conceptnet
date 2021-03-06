# encoding: utf-8

'''
Script to convert the weltmodell into the conceptnet.

@author: Michael A. Huelfenhaus
'''
import sys
import csv
import hashlib

from getopt import getopt, GetoptError

help_message = '''
usage: python wm-cn-conversion.py <weltmodell_tsv_file> <result_json_file>

Converts a weltmodell tsv file into the plain conceptnet json format.

Only binary relations are used.

Warning! the json file follows the convention of conceptnet and this
leads to non valid json, because the single lines are not in a an array.
'''

# global values for all json items.
context = '/ctx/all'
base_concept_url = '/c/en/'
base_rel_url = '/r/'
source_uri = '/s/site/weltmodell'
sources = '[ "' + source_uri + '"]'
dataset = '/d/weltmodell'
license = 'license'

letters = "abcdefghijklmnopqrstuvwxyz" 

def make_id(uri, weight, surface_text):
    '''
    Make a SHA-1 hash of the information that makes this line unique.
    '''
    m = hashlib.sha1()
    m.update(uri)
    m.update(weight)
    m.update(surface_text)
    return m.hexdigest()


def make_json_line(wm_line, concepts):
    '''
    Transforms an weltmodell line into a conceptnet json line.
    '''
    # extract realtion

    rel = wm_line[1].replace('{___}','').strip().replace(' ','_')

    rel_url = base_rel_url + rel
    start_url = base_concept_url + concepts[0].strip().replace(' ','_')
    end_url = base_concept_url + concepts[1].strip().replace(' ','_')

    features = '["' + start_url + ' ' + rel_url + ' -","' + start_url + ' ' + rel_url + ' -","' + '- ' +rel_url + ' ' + end_url + '"]'

    uri = '/a/[' + rel_url + ',' + start_url + ',' + end_url + ']'

    norm_pmi = wm_line[14]
    weight = norm_pmi

    # TODO add all verbargs to surface text
    surface_text = wm_line[19]

    # make id
    id_str = make_id(uri, weight, surface_text)

    json_items= [uri, weight, dataset, end_url, surface_text, start_url, license,
        id_str
, source_uri, sources, context, features, rel_url]
    #make json line
    json_line = '{'
    json_line += '"uri": "' + uri + '",'
    json_line += '"weight": ' + norm_pmi + ','
    json_line += '"dataset": "' + dataset + '",'
    json_line += '"surfaceText": "' + surface_text + '",'
    json_line += '"start": "' + start_url + '",'
    json_line += '"license": "' + license + '",'
    json_line += '"id": "' + id_str + '",'
    json_line += '"source_uri": "' + source_uri + '",'
    json_line += '"sources": ' + sources + ','
    json_line += '"context": "' + context + '",'
    json_line += '"features": ' + features + ','
    json_line += '"rel": "' + rel_url + '"'
    json_line += '}'

    # print wm_line
    return json_line

def convert_wm(wm_path, result_path):
    '''
    Converts a weltmodell tsv file into a conceptnet plain json file.
    '''
    convert_count = 0
    # start writing result file
    with open(result_path, 'w') as result_file:
         # read wm file
        with open(wm_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                # print row
                # filter for binary relations
                concepts = row[4][1:-1].split(', ')
                #print len(concepts) , row[4]
                if len(concepts) == 2:
                    # make json line for this wm entry
                    json_line =  make_json_line(row, concepts)
                    #print json_line
                    result_file.write(json_line + '\n')
                    convert_count += 1
                    if convert_count  % 1000 == 0:
                        print convert_count, 'binary relation lines converted'
    print 'wm to cn conversion complete: ', convert_count, 'binary relations converted. result written to', result_path 

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