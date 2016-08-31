#!/usr/bin/env python

print "\n===== \n"
from mongoengine import *
import datetime
import csv

connect('DC2_CP')

class General_info(Document):
    # Datable Candidate Application, Section 1, "Required's", part 1
    first_name = StringField(required=True,
                             default='')
    last_name = StringField(required=True,
                            default='')
    email = StringField(required=True,
                        default='')   
                        
    meta = {'allow_inheritance': True}

class Social(Document):
    # Datable Candidate Application, Section 1, "Required's", part 2
    github_url = StringField(required=True,
                             default='')
    linkedin_url = StringField(required=True,
                               default='')
    meetup_url = StringField(required=True,
                             default='')
    twitter_url = StringField(required=True,
                              default='')
                              
    meta = {'allow_inheritance': True}                            

class Professional_outlook(Document):
    # Datable Candidate Application, Section 1, "Required's", part 3
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
    
    meta = {'allow_inheritance': True}
    
class Community(Document):
    # Datable Candidate Application, Section 2, "Community Engagement"
    is_comm_organizer = BooleanField(required=True, 
                                     default=False)
    is_volunteer_for_other_comm_events = BooleanField(required=True,
                                                      default=False)
    is_presenter_of_own_work_at_event = BooleanField(required=True, 
                                                     default=False)
    where_presented = StringField()
    is_provider_of_successful_intro_to_comm_org = BooleanField(required=True, 
                                                   default=False)
    
    meta = {'allow_inheritance': True}

class Experience(Document):
    # Datable Candidate Application, Section 3, "Experience"
    experience_level = StringField(required=True,
                                   max_length=1, 
                                   choices=(('E', 'Entry 0 years'),
                                            ('J', 'Junior 1-3 years'), 
                                            ('M', 'Mid-level 3-5 years'),
                                            ('S', 'Senior 5+ years'),
                                            ('V', 'Veteran 10+ years')),
                                            default='E')
    sectors = ListField(StringField(required=True),
                        default=list)
    is_startup_exp = BooleanField(required=True,
                                  default=False)
    is_BD_sales_or_client_relationships = BooleanField(required=True, 
                                           default=False)
    is_freelance = BooleanField(required=True,
                                default=False)
    team_manage_exp = ListField(StringField(required=True),
                         default=list)
    
    meta = {'allow_inheritance': True}

class Background(Document):
    # Datable Candidate Application, Section 4, "Data Practitioner Background"
    three_data_projects = StringField(required=True,
                                      default='') 
    data_science_techniques = ListField(StringField(required=True),
                                        default=list)
    last_time_committed_code = StringField(required=True,
                                           max_length=5, 
                                           choices=(('Today', 'Today'),
                                                    ('1Week', 'Within last week'), 
                                                    ('1Mnth', 'Within last month'),
                                                    ('6Mnth', 'Within last 6 months'),
                                                    ('None', 'Not committed to coding')),
                                                    default='None')
    languages_and_libraries = ListField(StringField(required=True),
                                        default=list)
    
    meta = {'allow_inheritance': True}

class About_You(Document):
    # Datable Candidate Application, Section 5, "About You"
    links_to_personals = ListField(URLField(required=True),
                                   default=list)
    self_description = StringField(required=True,
                                   default='')  
    
    meta = {'allow_inheritance': True}

# Users
class User(General_info, 
           Social, 
           Professional_outlook, 
           Community, 
           Experience, 
           Background, 
           About_You):

    user_id = StringField()
    notes = StringField()
    
    # User Stats
    created_at = DateTimeField(default=datetime.datetime.now)
    total_log_ins = IntField(default=0)


def test():
    ## Test adding a user 1
    bob = User(email='bob@example.com')
    bob.first_name = 'Bob'
    bob.last_name = 'Ross'
    bob.is_citizen = True
    bob.save()
    bob.degrees = ["B.S."]
    bob.save()
    bob.degrees.append("M.S.")
    bob.save()
    bob.last_time_committed_code = "Today"
    bob.save()
    
    ## Test adding a user 2
    daffy = User(email='daffy@example.com', 
                first_name='Daffy', 
                last_name='Duck').save()


def test_csv():
    with open('test_candidates160808_trunc3cx10r.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, 
                                delimiter=',',
                                skipinitialspace=True)
        row_id = 0
        for row in spamreader:
            ## header row
            if row_id == 0:
                for i in row:
                    if i == "Candidate #":
                        index__user_id = row.index(i)
                    if i == "When was the last time you committed code?":
                        index__last_time_committed_code = row.index(i)
                    if i == "What languages & libraries do you use?":
                        index__languages_and_libraries = row.index(i)
                    if i == "What's your experience level?":
                        index__experience_level = row.index(i)
                    if i == "What Data Science techniques have you worked with?":
                        index__data_science_techniques = row.index(i)
                    if i == "Have you managed teams before?":
                        index__team_manage_exp = row.index(i)
                    if i == "Do you have a Security Clearance?":
                        index__security_clearance = row.index(i)
                    if i == "What Degrees have you earned?":
                        index__degrees = row.index(i)
                    if i == """ "Please describe three data science or data related projects you've worked on in the last three years. These can be features of larger projects, consulting projects, classified work described generally, or open source contributions." """:
                        index__three_data_projects = row.index(i)
                    if i == "Data Community DC Events Attended":
                        index__dc2_events_attanded = row.index(i)
                    if i == "Favorite Data Community DC Event & Speaker":
                        index__favorite_dc2_eventAndSpeaker = row.index(i)
                    if i == "Describe yourself in one sentence.":
                        index__self_description = row.index(i)
                    if i == "Have you ever presented your work at an event?":
                        index__is_presenter_of_own_work_at_event = row.index(i)
                    if i == "Where have you presented?":
                        index__where_presented = row.index(i)
                    if i == "Startup and/or Business Experience?": #<>
                        index__is_startup_exp_2 = row.index(i)
                    if i == "What sectors have you worked in?":
                        index__sectors = row.index(i)
                    if i == "How have you worked in/with teams?": # <>
                        index__worked_in_teams = row.index(i)
                    if i == "Have you accepted or would you accept freelance work?":
                        index__is_freelance = row.index(i)
                    if i == """ "Have you ever founded a startup, or joined a startup in the early stages, that achieved market traction or better?" """:
                        index__is_startup_exp = row.index(i)
                    if i == """ "Have you ever been involved with BD, sales, or managed a client relationship?" """:
                        index__is_BD_sales_or_client_relationships = row.index(i)
                    if i == "Are you a community organizer?":
                        index__is_comm_organizer = row.index(i)
                    if i == "Do you volunteer for others' community events?":
                        index__is_volunteer_for_other_comm_events = row.index(i)
                    if i == "Have you provided successful introductions to another community organizer?":
                        index__is_provider_of_successful_intro_to_comm_org = row.index(i)
                    if i == "Are you a US Citizen?":
                        index__is_citizen = row.index(i)
                row_id += 1
            ## move to other rows in csv
            else:
                user = User(user_id = row[index__user_id],
                     last_time_committed_code = convert__last_time_committed_code(row[index__last_time_committed_code]), 
                     languages_and_libraries = convert__languages_and_libraries(row[index__languages_and_libraries])).save()
                row_id += 1


def convert__last_time_committed_code(string):
    if string == "Today":
        return "Today"
    elif string == "Within the Last week":
        return "1Week"
    elif string == "Within the Last month":
        return "1Mnth"
    elif string == "Within last 6 months":
        return "6Mnth"
    else:
        return "None"

def convert__languages_and_libraries(string):
    return [x.strip() for x in string.split(',')]

def test_query():
    print "test_query"
    
    users_1Week = User.objects(last_time_committed_code = "1Week")
    for user in users_1Week:
        print user.user_id
    
def main():
    #test()
    test_csv()
    test_query()

if __name__ == '__main__':
    main()


