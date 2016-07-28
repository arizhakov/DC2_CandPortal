print "\n===== \n"
from mongoengine import *

connect('tumblelog')

# [] http://docs.mongoengine.org/tutorial.html

'''
In our Tumblelog application we need to store several different types of 
information. We will need to have a collection of users, so that we may link 
posts to an individual. We also need to store our different types of posts 
(eg: text, image and link) in the database. To aid navigation of our Tumblelog, 
posts may have tags associated with them, so that the list of posts shown to the 
user may be limited to posts that have been assigned a specific tag. Finally, it 
would be nice if comments could be added to posts. We’ll start with users, as 
the other document models are slightly more involved.
'''

# Users
class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

# Comment
class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    # also, add to the Post class

# Posts
class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30)) # adding 'tags'
    comments = ListField(EmbeddedDocumentField(Comment)) # adding 'comments'

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()

# Tags
    # add to the Post class



# Document structure defined

# Start adding User
ross = User(email='ross@example.com', 
            first_name='Ross', 
            last_name='Lawley').save()

john = User(email='john@example.com', 
            first_name='John', 
            last_name='the Hammer').save()

'''
or, can do:
    ross = User(email='ross@example.com')
    ross.first_name = 'Ross'
    ross.last_name = 'Lawley'
    ross.save()
'''

# add a couple of posts
post1 = TextPost(title='Fun with MongoEngine', author=john)
post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
post1.tags = ['mongodb', 'mongoengine']
post1.save()

post2 = LinkPost(title='MongoEngine Documentation', author=ross)
post2.link_url = 'http://docs.mongoengine.com/'
post2.tags = ['mongoengine']
post2.save()

## Accessing data
#for post in Post.objects:
#    print post.title

## Retrieving type-specific information

#for post in TextPost.objects:
#    print post.content

## self play 
#for post in Post.objects:
#    print post.comments.content
'''
for post in Post.objects:
    print post.title
    print '=' * len(post.title)

    if isinstance(post, TextPost):
        print 'Content:', post.content

    if isinstance(post, LinkPost):
        print 'Link:', post.link_url

    print
'''
## Searching our posts by tag

#for post in Post.objects(tags='mongodb'):
#    print post.title

num_posts = Post.objects(tags='mongodb').count()
print 'Found %d posts with tag "mongodb"' % num_posts

## More?! to the User Guide!! [] http://docs.mongoengine.org/guide/index.html

