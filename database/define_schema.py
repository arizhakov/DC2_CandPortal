#!/usr/bin/env python

#print "\n===== \n"
def define_schema():
    from mongoengine import *
    import datetime
    #import csv
    
    connect('DC2_CP')
    
    class General_info(Document):
        # Datable Candidate Application, Section 1, "Required's", part 1
    
        #"Timestamp" (from Responses_1.csv)
        timestamp = DateTimeField(required=True,
                                  default=datetime.datetime.now)
        #"First Name"
        first_name = StringField(required=True, 
                                 default='')
        #"Last Name"
        last_name = StringField(required=True,
                                default='')
        #"Email Address"
        email = StringField(required=True,
                            default='')   
                            
        meta = {'allow_inheritance': True}
    
    class Social(Document):
        # Datable Candidate Application, Section 1, "Required's", part 2
        
        #"Github Profile URL"    
        github_url = StringField(required=True,
                                 default='')
        #"LinkedIn Profile URL"
        linkedin_url = StringField(required=True,
                                   default='')
        #"Meetup Profile URL"
        meetup_url = StringField(required=True,
                                 default='')
        #"Twitter Profile URL"
        twitter_url = StringField(required=True,
                                  default='')
                                  
        meta = {'allow_inheritance': True}                            
    
    class Professional_outlook(Document):
        # Datable Candidate Application, Section 1, "Required's", part 3
    
        #"Are you currently looking for a position or willing to be contacted about positions?"
        is_open_to_positions = BooleanField(required=True,
                                            default=False)
        #"What Degrees have you earned?"
        degrees = ListField(StringField(required=True),
                            default=list)
        #"Are you a US Citizen?"
        is_citizen = BooleanField(required=True,
                                  default=False)
        #"Do you have a Security Clearance?"
        security_clearance = ListField(StringField(required=True),
                                       default=list)
        #"Data Community DC Events Attended"
        dc2_events_attanded = ListField(StringField(required=True),
                                        default=list)
        #"Favorite Data Community DC Event & Speaker"
        favorite_dc2_eventAndSpeaker = StringField(required=True,
                                                   default='')
        
        meta = {'allow_inheritance': True}
        
    class Community(Document):
        # Datable Candidate Application, Section 2, "Community Engagement"
        
        #"Are you a community organizer?"
        is_comm_organizer = BooleanField(required=True, 
                                         default=False)
        #"Do you volunteer for others' community events?"
        is_volunteer_for_other_comm_events = BooleanField(required=True,
                                                          default=False)
        #"Have you ever presented your work at an event?"
        #is_presenter_of_own_work_at_event = BooleanField(required=True, 
        #                                                 default=False)
        is_presenter_of_own_work_at_event = StringField(required=True,
                                                        default='')
        #"Where have you presented?"
        where_presented = StringField()
        #"Have you provided successful introductions to another community organizer?"
        is_provider_of_successful_intro_to_comm_org = BooleanField(required=True, 
                                                                   default=False)
        
        meta = {'allow_inheritance': True}
    
    class Experience(Document):
        # Datable Candidate Application, Section 3, "Experience"
    
        #"What's your experience level?"
        experience_level = StringField(required=True,
                                       max_length=1, 
                                       choices=(('E', 'Entry 0 years'),
                                                ('J', 'Junior 1-3 years'), 
                                                ('M', 'Mid-level 3-5 years'),
                                                ('S', 'Senior 5+ years'),
                                                ('V', 'Veteran 10+ years')),
                                                default='E')
        #"What sectors have you worked in?"
        sectors = ListField(StringField(required=True),
                                        default=list)
        #"Have you ever founded a startup, or joined a startup in the early stages, that achieved market traction or better?"
        is_startup_exp = BooleanField(required=True,
                                      default=False)
        #"Have you ever been involved with BD, sales, or managed a client relationship?"
        is_BD_sales_or_client_relationships = BooleanField(required=True, 
                                                           default=False)
        #"Have you accepted or would you accept freelance work?"
        is_freelance = BooleanField(required=True,
                                    default=False)
        #"Have you managed teams before?"
        team_manage_exp = ListField(StringField(required=True),
                                                default=list)
        
        meta = {'allow_inheritance': True}
    
    class Background(Document):
        # Datable Candidate Application, Section 4, "Data Practitioner Background"
    
        #"Please describe three data science or data related projects..."
        three_data_projects = StringField(required=True,
                                          default='') 
        #"What Data Science techniques have you worked with?"
        data_science_techniques = ListField(StringField(required=True),
                                            default=list)
        #"When was the last time you committed code?"
        last_time_committed_code = StringField(required=True,
                                               max_length=5, 
                                               choices=(('Today', 'Today'),
                                                        ('1Week', 'Within last week'), 
                                                        ('1Mnth', 'Within last month'),
                                                        ('6Mnth', 'Within last 6 months'),
                                                        ('None', 'Not committed to coding')),
                                                        default='None')
        #"What languages & libraries do you use?"
        languages_and_libraries = ListField(StringField(required=True),
                                            default=list)
        
        meta = {'allow_inheritance': True}
    
    class About_You(Document):
        # Datable Candidate Application, Section 5, "About You"
    
        #"Please Provide Any Links to Personal Websites, Resume, Portfolios, etc."
        #links_to_personals = ListField(URLField(required=True),
        #                               default=list)
        links_to_personals = StringField(required=True,
                                         default='')
        #"Describe yourself in one sentence."
        self_description = StringField(required=True,
                                       default='')  
        
        meta = {'allow_inheritance': True}
    
    class Old(Document):
        # Unique fields from Google database "Scrubbed Candidate Pool - Candidate_Pool"
        ## Note that any duplicates from "Datable Candidate Application" fields in other classes were removed in 'Old` class.
    
        #"Candidate #"
        candidate_num = StringField(required=True,
                                    default='')
        #"Startup and/or Business Experience?"
        startup_and_or_business_exp = StringField(required=True,
                                                  default='')
        #"How have you worked in/with teams?"
        have_worked_in_and_or_with_teams = StringField(required=True,
                                                       default='')                                          
    
        meta = {'allow_inheritance': True}
    
    # Users
    class User(General_info, 
               Social, 
               Professional_outlook, 
               Community, 
               Experience, 
               Background, 
               About_You,
               Old):
    
        user_id = StringField(required=True,
                              default='')
        notes = StringField(required=True,
                              default='')
        
        # User Stats
        #created_at = DateTimeField(default=datetime.datetime.now)
        total_log_ins = IntField(default=0)
    
    return User
