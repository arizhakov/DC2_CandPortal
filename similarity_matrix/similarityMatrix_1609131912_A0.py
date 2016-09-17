from math import *
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd


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
print "=============\n"


# 1. import MongoDB as pandas df, to process with numpy.
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
    
    ## preview data
    #print "data.size", data.size
    #print "data.head", data.head
    #with pd.option_context('display.max_rows', 10, 'display.max_columns', 10):
    #    print data.ix[:5,:5]
    #print data.ix[:5,:5]
    
    return data



# 2. generate sensitivity matrix

# 2.1. get 2 candidates

# 2.2. get similarity between 2 candidates
    '''
    Measures of similarity between two vectors
        Euclidean distance
        1-norm
        ∞-norm
        => Cosine measure (most widely used in lit.)
        Gabriel graph
        A measure derived from a consensus matrix
        Other ideas: Delaunay triangulation, Hamming distance or variation
    '''


#num_questions = len(vector_1)
#all_yes = np.array([1]*num_questions)
#all_no  = np.array([0]*num_questions)
#MAX_DIFF = np.sqrt( np.sum(np.square( all_yes-all_no )) )
def get_max_diff(v1):
    return sqrt(float(len(v1)))

# <>
def compare_T1(v1,v2):
    # Compare all questions of a certain type, and return value of 0-1
    return answer_diffs # value 0-1

# <>
def question_similarity(v1,v2):
    #print "---"
    #print v1
    #print v2
    equal = np.array(v1)==np.array(v2) # Future tests look at each question separately as they are much more complicated that T/F
    ### <> what if not exactly equal but close? machine error?
    #print equal
    xx = np.where(equal)[0]
    #print xx
    answer_diffs = np.zeros(len(v1))
    #print answer_diffs
    answer_diffs[xx] = 1
    #print answer_diffs
    # return vectors between 0 and 1 for each question
    #print "---"    
    return answer_diffs

def get_normalized_EuclidDist(vector_differences,maximum_difference):
    '''
    AKA "candidate_difference"
    '''
    
    #print "candidate_difference | vector_differences: ", vector_differences
    #print "candidate_difference | MAX_DIFF: ", MAX_DIFF        
    
    return np.sqrt(np.sum(np.square(np.array(vector_differences))))/maximum_difference # diff = np.array(v1)-np.array(v2)

def get_two_candidate_sim(v_1,v_2):
    #    print "get_two_candidate_sim | vector1: ", vector1
    #    print "get_two_candidate_sim | vector2: ", vector2
    
    max_diff = get_max_diff(v_1)
    #print "get_two_candidate_sim | MAX_DIFF: ", MAX_DIFF #ok
    
    v_diff = np.array(v_1)-np.array(v_2) # may need abs()?
    #print "get_two_candidate_sim | v_diff: ", v_diff
    
    #num = np.sqrt( np.sum(np.square( np.array(v_diff) )) )
    #print "get_two_candidate_sim | num: ", num
    
    candidateDifference = get_normalized_EuclidDist(v_diff, max_diff)
    #print "get_two_candidate_sim | candidateDifference: ", candidateDifference

    candidateSimilarity = 1 - candidateDifference
    #print "get_two_candidate_sim | candidateSimilarity: ", candidateSimilarity
    
    
    #print question_similarity(vector1,vector2)
    
    return candidateSimilarity

def get_candidate_sim_matrix(data):
    
    # 1. get subset of dataframe
    df = data.loc[:, ['is_BD_sales_or_client_relationships', 
                      'is_citizen',
                      'is_comm_organizer',
                      'is_freelance']]
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

def test():
#    method_0_SimpleDiffSimilarity(vector_3, vector_6)
#    method_1_RootSumSqSimilarity(vector_3, vector_6)
#    method_2_cosineCoefSimilarity(vector_3, vector_6)
#    method_3_JaccardCoefSimilarity(vector_3, vector_6)
#    method_4_DiceCoefSimilarity(vector_3, vector_6)
#    method_5_EuclidDistSimilarity(vector_3, vector_6)
#    method_6_NormEuclidDistSimilarity(vector_3, vector_6)
#    method_7_WeightEuclidDistSimilarity(vector_3, vector_6)
#    #print "np.square([1,2,3]): ", np.square([1,2,3]) 
#    #print "np.sum(np.square([1,2,3])): ", np.sum(np.square([1,2,3]))
    TF = False
    if TF:
        vector_1 = [True,True,False,True,False]
        vector_2 = [True,True,False,True,False]
        vector_3 = [True,False,False,False,False]
        vector_4 = [False,False,False,False,False]
        vector_5 = [True,True,True,True,True]
        vector_6 = [False,False,True,False,True] #opposite of vector_1
    else:
        vector_1 = [1,1,0,1,0]
        vector_2 = [1,1,0,1,0]
        vector_3 = [1,0,0,0,0]
        vector_4 = [0,0,0,0,0]
        vector_5 = [1,1,1,1,1]
        vector_6 = [0,0,1,0,1] #opposite of vector_1
        #7,8 for testing MAX_DIFF to be 1
        vector_7 = np.ones(5)
        vector_8 = np.zeros(5)

    #print "test | vector_1: ", vector_1
    #print "test | vector_3: ", vector_3
    
    #vector1 = vector_1
    #vector2 = vector_6
    
    #print "candidateSimilarity:", get_two_candidate_sim(vector_8, vector_8)

def test_M():
    data1 = import_db_as_df()
    M = get_candidate_sim_matrix(data1)
    
    #print M
    #np.savetxt("candidate_sim_matrix.csv", M, delimiter=",")
    #plt.imshow(M, cmap='hot', interpolation='nearest')
    plt.imshow(M, cmap='rainbow', interpolation='nearest')

def test_string_compare():
    # http://stackoverflow.com/questions/8897593/similarity-between-two-text-documents
    # ? http://stackoverflow.com/questions/2380394/simple-implementation-of-n-gram-tf-idf-and-cosine-similarity-in-python?noredirect=1&lq=1
    # "Equivalent to CountVectorizer followed by TfidfTransformer." http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    # http://stackoverflow.com/questions/32128802/how-to-use-sklearns-countvectorizerand-to-get-ngrams-that-include-any-punctua
    # http://stackoverflow.com/questions/23850256/how-can-i-pass-a-preprocessor-to-tfidfvectorizer-sklearn-python

    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.tokenize import TreebankWordTokenizer

    test_text_1 = ["I'd like an apple",
                   "An apple a day keeps the doctor away",
                   "Never compare an apple to an orange",
                   "I prefer scikit-learn to Orange",
                   "I'd like an apple",
                   "I'd like an orange"]
    test_text_2 = ["I'd like an apple",
                   "I'd like an apple orange"]
    
    #<> add a stemming step? couse be useful for typos
                   
    vect = TfidfVectorizer(min_df=0,
                           stop_words="english",
                           #tokenizer=TreebankWordTokenizer().tokenize, #to get dashes,etc
                           lowercase=True) 
    tfidf = vect.fit_transform(test_text_2) #This is equivalent to fit followed by transform, but more efficiently implemented.
    sim_M = (tfidf * tfidf.T).A
    print "tfidf\n", tfidf       
    print      
    print "vect.get_feature_names()\n", vect.get_feature_names() 
    print                  
    print "similiarity matrix\n", sim_M
    #plt.imshow(sim_M, cmap='rainbow', interpolation='nearest')
    print "similarity between 2 sentences:", sim_M[0,1]

def get_two_string_sim(v_1,v_2):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from nltk.tokenize import TreebankWordTokenizer

    text = [v_1, v_2]
    #print test_text_2
    #<> add a stemming step? couse be useful for typos
                   
#    vect = TfidfVectorizer(min_df=0,
#                           stop_words="english",
#                           #tokenizer=TreebankWordTokenizer().tokenize, #to get dashes,etc
#                           lowercase=True) 
    vect = TfidfVectorizer(min_df=0,
                           stop_words="english")
    tfidf = vect.fit_transform(text) #This is equivalent to fit followed by transform, but more efficiently implemented.
    sim_M = (tfidf * tfidf.T).A
    #print "tfidf\n", tfidf       
    #print      
    #print "vect.get_feature_names()\n", vect.get_feature_names() 
    #print                  
    #print "similiarity matrix\n", sim_M
    #plt.imshow(sim_M, cmap='rainbow', interpolation='nearest')
    #print "similarity between 2 sentences:", sim_M[0,1]
    return sim_M[0,1]

def get_types_via_first_row(row):
    i_bool = []
    i_unic = []
    i_list = []
    for i,val in enumerate(row):
        #print i
        #print val
        if type(val) == unicode:
            #print "element is of unicode type"
            i_unic.append(i)
        elif val == False or val == True:
            #print "element is of bool type"
            i_bool.append(i)
        elif type(val) == list:
            #print "element is of list type"
            i_list.append(i)
        #print
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

# OR
#==============================================================================
# making a collection within db for each type. Eg., all T/F q’s ie of `BooleanField` in mongoengine go into 
# “class User_bool(TF1, 
# 		TF2, 
# 		…
# 		)
# ” ; 
# and all strings of `StringField` go into 
# “class User_str(TF1, 
# 		TF2, 
# 		…
# 		)
# ” ; 
# and all strings of `StringField` with ordinal data and thus choices go into 
# “class User_str_choices(TF1, 
# 		TF2, 
# 		…
# 		)
# ” ; 
# Then, can import into different pd.df’s, and thus separated by type.     
#==============================================================================

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
    #simM = simM_bool*(bool_Q/total_Q) + simM_unic*(unic_Q/total_Q)
    return simM


def main():
    #test()
    data1 = import_db_as_df()
    #test_M()
    #test_string_compare()
    #get_two_string_sim(s1,s2)
    
    #row1 = data1.loc[0,:]
    #get_types_via_first_row(row1)
    simM = combine_single_sim_matrix(data1)
    plt.imshow(simM, cmap='rainbow', interpolation='nearest')
    

if __name__ == '__main__':
    main()
