'''
> matching algorithms most useful for going forward

First, create similarity matrix between all candidates
    Whos most like each other?
        n*n matrix, n = each candidates. [0,1]
        Score off of questions in DB
        % same 100, and not at all = 0%
        “Root sum sq” for composites 
            Independent variables treatment 
diff , N dim space
Valid assump? Maybe, but need covariance matrix to confirm cross-correlation
[] weighted sum 
Assumes same dimensionality, dependency
Same space, 1 dim space
? negatives may cancel
future : add new dims in similarity matrix, from linkedin, meetup, twitter, etc
Recommendation engine 
You like this candidate? Well how about these as well
 <> ! start work on similarity matrix on all well-structured questions(fields)
Start w simple yes/no questions, then advance
Use numpy for lin. Alg.

1608271720
Research similarity matrix. Placed lit search articles into gD.
Research how to pull data from mongodb to python for analysis.
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

# 1. import db as pandas df, to process with numpy


# 2. 