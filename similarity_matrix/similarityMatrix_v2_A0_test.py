# -*- coding: utf-8 -*-

from math import *
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd
from scipy.spatial.distance import cosine, euclidean

#utilities
import time


'''
create similarity matrix between all candidates
    Whos most like each other?
        n*n matrix, n = each candidates. [0,1]
        Score off of questions in DB
        % same 100, and not at all = 0%
        “Root sum sq” for composites 
        start work on similarity matrix on all well-structured questions(fields)
            Start w simple yes/no questions, then advance
        Use numpy for lin. Alg.

References:
[1] https://en.wikipedia.org/wiki/Cosine_similarity
[2] http://bioinformatics.oxfordjournals.org/content/22/18/2298.full
[3] https://en.wikipedia.org/wiki/Euclidean_distance
[4] https://www.mathworks.com/matlabcentral/answers/293532-how-to-calculate-normalized-euclidean-distance-on-two-vectors?requestedDomain=www.mathworks.com
[5] http://www.econ.upf.edu/~michael/stanford/maeb4.pdf

'''

# 1. Import MongoDB as pandas dataframe for future processing and analysis.
def import_db_as_df():
    '''
    -> pull data from mongodb to python for analysis.
    “Pymongo” lib
        Check old work from Udacity course
    “Monary” lib
        https://monary.readthedocs.io/index.html
        Types https://monary.readthedocs.io/reference.html?highlight=type
        https://www.youtube.com/watch?v=oteFpXIKBYg
        https://monary.readthedocs.io/examples/string.html 
        https://monary.readthedocs.io/installation.html 
    http://alexgaudio.com/2012/07/07/monarymongopandas.html 
    https://docs.mongodb.com/getting-started/python/insert/
    http://stackoverflow.com/questions/17805304/how-can-i-load-data-from-mongodb-collection-into-pandas-dataframe?noredirect=1&lq=1
    http://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas?noredirect=1&lq=1
    http://djcinnovations.com/index.php/archives/164
    http://djcinnovations.com/index.php/archives/103
    '''
    client = MongoClient() #client = MongoClient('localhost:27017')
    db = client['DC2_CP'] #db = client.database_name
    collection = db['general_info'] #collection = db.collection_name
    data = pd.DataFrame(list(collection.find())) #continue with this. <>
        
    return data


# 2. Similarity matrix computation.
### General functions (i.e., can be used for Boolean, MC, etc. functionality).
## Distance functions.
def get_euclidean_dist(v1, v2):
    return euclidean(np.array(v1), np.array(v2))

### processing Boolean-specific response.
def get_max_diff_boolean(v1):
    return sqrt(float(len(v1)))
def get_two_candidate_sim_boolean(v1, v2):
    max_diff = get_max_diff_boolean(v1)
    candidate_diff = get_euclidean_dist(v1, v2) / max_diff   # normalized Euclidean distance
    candidate_sim = 1 - candidate_diff
    return candidate_sim



### Multiple Choice responses
# Assmp1: know that answers are MC, and the order <<> how to know this beforehand?>
# Approach 1: tell up front
# Approach 2: collect all responses, put in list, get only unique vals
# But still dont know order...

def test_MC():
    ## MC testing
    # fibo = [1,2,3,5,8]
    example_MC_ans = ["A", "B", "A", "C", "D", "E", "E"]
    example_MC_order = ["A", "B", "C", "D", "E"]

    def get_nth_fibonacci(n):
        """
        return n-th Fibonacci number, where 1st number in sequence is 0, 2nd = 1, 3rd = 1, 4th = 2, etc.

        e.g.:
        n Fib.
        _ _
        0 0
        1 1
        2 1
        3 2
        4 3
        5 5
        6 8
        7 13
        8 21
        9 34
        """

        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return get_nth_fibonacci(n - 1) + get_nth_fibonacci(n - 2)

    def get_fib_list(n):
        fibo = []
        shift = 2  # start Fib. seq. at a shifted window
        for i in range(shift, n + shift):
            fibo.append(get_nth_fibonacci(i))
        return fibo

    fibo = get_fib_list(len(example_MC_order))
    # print fibo

    # max_fibo = max(fibo)

    example_MC_ans_num = []
    shift = 2  # start Fib. seq. at a shifted window
    for i in example_MC_ans:
        example_MC_ans_num.append(float(get_nth_fibonacci(example_MC_order.index(i) + shift)))
    print example_MC_ans_num

    max_example_MC_ans_num = max(example_MC_ans_num) # get max value of this q's answers. note: not the same as max in order list.

    example_MC_ans_num_norm = np.divide(example_MC_ans_num, max_example_MC_ans_num)
    print example_MC_ans_num_norm

#<> separate out all the Boolean, MC, etc questions - how??
#<> find example MC Q.
#<> combine 2,3 MC Q's together. do above for each Q, then send each pair of norm. Fib. Cand's rows to Euler. dist. func.
##<> 1. convert MC answer to Fib-scaled num.
##<> 2. scale by max
##<> 3. feed each row aka C's array into sim. M.



def get_two_string_sim(v_1,v_2):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.tokenize import TreebankWordTokenizer

    text = [v_1, v_2]
    #<> add a stemming step? couse be useful for typos
                   
#    vect = TfidfVectorizer(min_df=0,
#                           stop_words="english",
#                           #tokenizer=TreebankWordTokenizer().tokenize, #to get dashes,etc
#                           lowercase=True) 
    vect = TfidfVectorizer(min_df=0,
                           stop_words="english")
    tfidf = vect.fit_transform(text) #This is equivalent to fit followed by transform, but more efficiently implemented.
    sim_M = (tfidf * tfidf.T).A
    return sim_M[0,1]

def get_types_via_first_row(row):
    i_bool = []
    i_unic = []
    i_list = []
    for i,val in enumerate(row):
        if type(val) == unicode:
            i_unic.append(i)
        elif val == False or val == True:
            i_bool.append(i)
        elif type(val) == list:
            i_list.append(i)
    return i_bool, i_unic, i_list

def get_candidate_sim_matrix_bool(df):
    num_candidates = df.shape[0]
    candidate_sim_matrix = np.eye(num_candidates) # initialize candidate_sim_matrix
    # loop for all unique pairs
    for i in range(num_candidates - 1):
        for j in range(i+1, num_candidates):
            candidateSimilarity = get_two_candidate_sim(df.ix[i,:],
                                                        df.ix[j,:])
            candidate_sim_matrix[i,j] = candidateSimilarity
            candidate_sim_matrix[j,i] = candidateSimilarity
    return candidate_sim_matrix #matrix of NxN candidates with answer difference values between 0-1

def get_candidate_sim_matrix_unic(df):
    num_candidates = df.shape[0]
    candidate_sim_matrix = np.eye(num_candidates) # initialize candidate_sim_matrix
    # loop for all unique pairs
    for i in range(num_candidates - 1):
        for j in range(i+1, num_candidates):
#            s_pad = "xxxx"
#            v1 = df.ix[i,:] + s_pad # not efficient, but can be optimized later
#            v2 = df.ix[j,:] + s_pad # not efficient, but can be optimized later
            v1 = ','.join(df.ix[i,:]) # not efficient, but can be optimized later
            v2 = ','.join(df.ix[j,:]) # not efficient, but can be optimized later
            candidateSimilarity = get_two_string_sim(v1,v2) #<> throwing the error. have to example the v1, v2 coming in
            candidate_sim_matrix[i,j] = candidateSimilarity
            candidate_sim_matrix[j,i] = candidateSimilarity
    return candidate_sim_matrix #matrix of NxN candidates with answer difference values between 0-1

def get_candidate_sim_matrix_list(df):
    num_candidates = df.shape[0]
    candidate_sim_matrix = np.eye(num_candidates) # initialize candidate_sim_matrix
    # loop for all unique pairs
    for i in range(num_candidates - 1):
        for j in range(i+1, num_candidates):
            # join list into string
            list1 = []
            for item in df.ix[i,:]:
                list1.append(','.join(item))
            list2 = []
            for item in df.ix[j,:]:
                list2.append(','.join(item))
            v1 = ','.join(list1) # not efficient, but can be optimized later
            v2 = ','.join(list2) # not efficient, but can be optimized later
            candidateSimilarity = get_two_string_sim(v1,v2)
            candidate_sim_matrix[i,j] = candidateSimilarity
            candidate_sim_matrix[j,i] = candidateSimilarity
    return candidate_sim_matrix #matrix of NxN candidates with answer difference values between 0-1

def combine_single_sim_matrix(data):
#==============================================================================
#     1 - find types
#     
#     2 - find sim matrix for each type 
#         a - 'get_candidate_sim_matrix' for T/F, 1/0 vectors
#         b - 'get_two_string_sim' for strings,sentences
#         c - ? for multiple-choice Q's
#     3 - combine sim matrix by wt avg by num. of elements/Qs in each sim matrix
#==============================================================================    
    row0 = data.ix[0, :] # first row
    i_bool, i_unic, i_list = get_types_via_first_row(row0) #get indices of types as lists
    #print i_bool
    df_bool = data.ix[:, i_bool]
    df_unic = data.ix[:, i_unic]
    df_list = data.ix[:, i_list]
    bool_Q = df_bool.shape[1]
    unic_Q = df_unic.shape[1]
    list_Q = df_list.shape[1]
    total_Q = float(data.shape[1])
    
    df_bool = df_bool.drop('total_log_ins',1)
    simM_bool = get_candidate_sim_matrix_bool(df_bool)
    simM_unic = get_candidate_sim_matrix_unic(df_unic)
    simM_list = get_candidate_sim_matrix_list(df_list)
    simM = simM_bool*(bool_Q/total_Q) + simM_unic*(unic_Q/total_Q) + simM_list*(list_Q/total_Q)
    return simM


def main():
    #test()
    ###data1 = import_db_as_df()
    #test_M()
    #test_string_compare()
    #get_two_string_sim(s1,s2)
    
    #row1 = data1.loc[0,:]
    #get_types_via_first_row(row1)
    ###simM = combine_single_sim_matrix(data1)
    ###plt.imshow(simM, cmap='rainbow', interpolation='nearest')
    ###plt.show(block=True)  # for PyCharm displaying

    ## new boolean testing
    # V1 = [True, False, True, False, True, False, True, True, False, True]
    # V2 = [False, False, True, False, True, True, True, False, True, False]
    # t0 = time.clock()
    # print get_two_candidate_sim_Boolean(V1, V2)
    # print time.clock() - t0
    # t0 = time.clock()
    # print get_two_candidate_sim(V1,V2)
    # print time.clock() - t0

    test_MC()


if __name__ == '__main__':
    print "====="
    main()
    print "====="
