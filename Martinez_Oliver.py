# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 02:09:48 2019

@author: Oliver Martinez
"""

import re
import string

def write_to_file(results, name):
    new_ind = open(name+'.txt', 'wt', encoding='utf-8')
    new_ind.writelines('\t'.join(str(j) for j in i) + '\n' for i in results)
    

def run_queries(inv_ind, queries):
    # Create resulting matrix       
    Q_results = [["" for x in range(2)] for y in range(len(queries))]
    
    for i in range(len(queries)):
        Q_results[i][0] = queries[i]
    
    # Process the queries
    for i in range(len(queries)):
        #Split each word from the query
        q1 = queries[i].split(' ')[0].lower()
        q2 = queries[i].split(' ')[2].lower()
        logical = queries[i].split(' ')[1]
        
        # Write down all instances of the word and their appearance from the inverted index.
        temp_results = ''
        for j in range(len(inv_ind)):
            if inv_ind[j][0] == q1 or inv_ind[j][0] == q2:
                
                # iterate through the inverted index to find the documents
                for k in range(len(inv_ind[0])):
                    if inv_ind[j][k] != '':
                        temp_results += inv_ind[j][k] + " "
                    
        print(temp_results)
        
        # Check if query has 'OR' or 'AND' and write to result
        if logical == "OR":
            if temp_results.find("d1") > 1:
                Q_results[i][1] += "d1 "
            if temp_results.find("d2") > 1:
                Q_results[i][1] += "d2 "
            if temp_results.find("d3") > 1:
                Q_results[i][1] += "d3 "
            if temp_results.find("d4") > 1:
                Q_results[i][1] += "d4 "
            if temp_results.find("d5") > 1:
                Q_results[i][1] += "d5 "
            if temp_results.find("d6") > 1:
                Q_results[i][1] += "d6"
        if logical == "AND":
            if temp_results.count('d1') > 1:
                Q_results[i][1] += "d1 "
            if temp_results.count('d2') > 1:
                Q_results[i][1] += "d2 "
            if temp_results.count('d3') > 1:
                Q_results[i][1] += "d3 "
            if temp_results.count('d4') > 1:
                Q_results[i][1] += "d4 "
            if temp_results.count('d5') > 1:
                Q_results[i][1] += "d5 "
            if temp_results.count('d6') > 1:
                Q_results[i][1] += "d6"
        print()
        
        # Write '-1' for the queries with no results
        if Q_results[i][1] == "":
             Q_results[i][1] = "-1"
        
    print(Q_results)
            
    return Q_results

# Create the inverted index
def create_index(terms, d1, d2, d3, d4, d5, d6):
    
    # Iterate though all terms note which document they appear in
    for term in range(len(terms)):
        if terms[term][0] in d1:
            terms[term][1] = "d1"
        if terms[term][0] in d2:
            terms[term][2] = "d2"
        if terms[term][0] in d3:
            terms[term][3] = "d3"
        if terms[term][0] in d4:
            terms[term][4] = "d4"
        if terms[term][0] in d5:
            terms[term][5] = "d5"
        if terms[term][0] in d6:
            terms[term][6] = "d6"
    
    return terms
  
# Obtain the list of unique words
def remove_duplicates(d1, d2, d3, d4, d5, d6):
    
    d = d1 + d2 + d3 + d4 + d5 + d6
    term_list = []
    
    # duplicae word removal
    for term in d: 
        if term not in term_list: 
            term_list.append(term) 
            
    # Fromat the result into a 2d array        
    a = [["" for x in range(7)] for y in range(len(term_list))]
    for x in range(len(a)):
        a[x][0] = term_list[x]
    
    return a 
  
# Extracts words from file
def convert_txt_file(doc):
    doc = doc.read()
    doc_words = re.sub('['+string.punctuation+']', '', doc).split() # removes punctuations too
    return doc_words


# Open all text files
doc1 = convert_txt_file(open("doc1.txt", "r"))
doc2 = convert_txt_file(open("doc2.txt", "r"))
doc3 = convert_txt_file(open("doc3.txt", "r"))
doc4 = convert_txt_file(open("doc4.txt", errors = "ignore")) # file has different encoding
doc5 = convert_txt_file(open("doc5.txt", "r"))
doc6 = convert_txt_file(open("doc6.txt", "r"))
queries = open("query.txt", "r").read().split('\n') # Last value is empty

terms = remove_duplicates(doc1, doc2, doc3, doc4, doc5, doc6)



inverted_index = create_index(terms, doc1, doc2, doc3, doc4, doc5, doc6)

#    print(inverted_index)

successful_queries = run_queries(inverted_index, queries)

write_to_file(inverted_index, "index_Martinez")
write_to_file(successful_queries, "answer")
