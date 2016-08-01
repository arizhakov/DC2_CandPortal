print "\n===== \n"
from mongoengine import *

connect('DC2_CP')

# [] http://docs.mongoengine.org/tutorial.html

# Users
class User(Document):
    # Datable Candidate Application, Section 1, "Required's"
    email = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    github_url = StringField(required=True)
    linkedin_url = StringField(required=True)
    meetup_url = StringField(required=True)
    twitter_url = StringField(required=True)
    is_open_to_positions = BooleanField(default=False)
    degrees = ListField(StringField(required=True))
    is_citizen = BooleanField(default=False)
    security_clearance = StringField(required=True) #?
    dc2_events_attanded = ListField(StringField(required=True))
    favorite_dc2_eventAndSpeaker = StringField(required=True) #?
    
    # Section 2, community engagement
    is_comm_organizer = BooleanField(default=False)
    is_volunteer_for_other_comm_events = BooleanField(default=False)
    
    
    # Stats
    created_at = DateTimeField(default=datetime.datetime.now)




'''
# Comment
class Comment(    ):
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

### Document structure defined


# Start adding User
ross = User(email='ross@example.com', 
            first_name='Ross', 
            last_name='Lawley').save()

john = User(email='john@example.com', 
            first_name='John', 
            last_name='the Hammer').save()

#or, alternatively, can add user by:
bob = User(email='bob@example.com')
bob.first_name = 'Bob'
bob.last_name = 'Ross'
bob.save()


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


for post in Post.objects:
    print post.title
    print '=' * len(post.title)

    if isinstance(post, TextPost):
        print 'Content:', post.content

    if isinstance(post, LinkPost):
        print 'Link:', post.link_url

    print



## Searching our posts by tag

#for post in Post.objects(tags='mongodb'):
#    print post.title

num_posts = Post.objects(tags='mongodb').count()
print 'Found %d posts with tag "mongodb"' % num_posts

## More?! to the User Guide!! [] http://docs.mongoengine.org/guide/index.html
'''


## Test adding a user
bob = User(email='bob@example.com')
bob.first_name = 'Bob'
bob.last_name = 'Ross'
bob.is_citizen = True
bob.save()