print "\n===== \n"
from mongoengine import *
import datetime

connect('DC2_CP')

# [] http://docs.mongoengine.org/tutorial.html

# Users
class User(Document):
    # Datable Candidate Application, Section 1, "Required's"
    first_name = StringField(required=True,
                             default='')
    last_name = StringField(required=True,
                            default='')
    email = StringField(required=True,
                        default='')    
    github_url = StringField(required=True,
                             default='')
    linkedin_url = StringField(required=True,
                               default='')
    meetup_url = StringField(required=True,
                             default='')
    twitter_url = StringField(required=True,
                              default='')
    is_open_to_positions = BooleanField(required=True,
                                        default=False)
    degrees = ListField(StringField(required=True),
                        default=list)
    is_citizen = BooleanField(required=True,
                              default=False)
    security_clearance = ListField(StringField(required=True),
                                   default=list)
    dc2_events_attanded = ListField(StringField(required=True),
                                    default=list)
    favorite_dc2_eventAndSpeaker = StringField(required=True,
                                               default='') 
    
    # Datable Candidate Application, Section 2, "Community Engagement"
    is_comm_organizer = BooleanField(required=True, 
                                     default=False)
    is_volunteer_for_other_comm_events = BooleanField(required=True,
                                                      default=False)
    is_presenter_of_own_work_at_event = BooleanField(required=True, 
                                                     default=False)
    where_presented = StringField()
    is_provider_of_successful_intro = BooleanField(required=True, 
                                                   default=False)
    
    # Datable Candidate Application, Section 3, "Experience"
    experience_level = StringField(max_length=1, 
                                   choices=(('E', 'Entry 0 years'),
                                            ('J', 'Junior 1-3 years'), 
                                            ('M', 'Mid-level 3-5 years'),
                                            ('S', 'Senior 5+ years'),
                                            ('V', 'Veteran 10+ years')))
    sectors = ListField(StringField(required=True),
                        default=list)
    is_startup_exp = BooleanField(required=True,
                                  default=False)
    is_client_relationships = BooleanField(required=True, 
                                           default=False)
    is_freelance = BooleanField(required=True,
                                default=False)
    team_exp = ListField(StringField(required=True),
                         default=list)
    
    # Datable Candidate Application, Section 4, "Data Practitioner Background"
    three_data_projects = StringField(required=True,
                                      default='') 
    data_science_techniques = ListField(StringField(required=True),
                                        default=list)
    last_time_committed_code = StringField(max_length=2, 
                                           choices=(('T', 'Today'),
                                                    ('1W', 'Within last week'), 
                                                    ('1M', 'Within last month'),
                                                    ('6M', 'Within last 6 months'),
                                                    ('No', 'Not committed to coding')))
    languages_and_libraries = ListField(StringField(required=True),
                                        default=list)
    
    # Datable Candidate Application, Section 5, "About You"
    links_to_personals = ListField(URLField(required=True),
                                   default=list)
    self_description = StringField(required=True,
                                   default='')
        
    # User Stats
    created_at = DateTimeField(default=datetime.datetime.now)
    total_log_ins = IntField(default=0)


## Test adding a user
bob = User(email='bob@example.com')
bob.first_name = 'Bob'
bob.last_name = 'Ross'
bob.is_citizen = True
bob.save()
bob.degrees = ["B.S."]
bob.save()
bob.degrees.append("M.S.")
bob.save()
bob.last_time_committed_code = "T"
bob.save()


# choices!!
'''
SIZE = (('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'))


class Shirt(Document):
    size = StringField(max_length=3, choices=SIZE)
'''

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
