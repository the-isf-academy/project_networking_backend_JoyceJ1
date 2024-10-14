# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField
import datetime



class Scavenger_hunt(Model):
    # user_posted = StringField()
    location = StringField()
    hint = StringField()
    # image = BlobField()
    description = StringField()
    year = IntegerField()
    month = IntegerField*()
    day = IntegerField()
    time_limit = BooleanField()
    code = StringField()
    complete = BooleanField()
    active = BooleanField()
    # user_completed = StringField()
    # comments = StringField()
    likes = IntegerField()
    

    def json_response(self):

        return {
            # 'user_posted' : self.user_posted,
            'description' : self.description,
            # 'image' : self.image,
            'time_limit' : print(f"{self.year}-{self.month}-{self.day}"),
            # 'comments' : self.comments,
            'likes' : self.likes,
        }
    
    def hint_response(self):

        return {

            'description' : self.description,
            'hint' : self.hint,
            # 'image' : self.image,
            'time_limit' : print(f"{self.year}-{self.month}-{self.day}"),
            # 'comments' : self.comments,
            'likes' : self.likes,
        }

    def increase_likes(self):
        #add likes by 1
        self.likes += 1
        self.save()

    def create_code(self):
        if len(self.code) < 5:
            print("Your code needs to be at least 6 letters long!")

    def check_code(self, user_code):
        #checks if the code is correct
        if self.code == user_code:
            print("Congratulations!")
            self.complete = True
            self.active = False
        else:
            print("Not Correct...")
        self.save()
    
    def calculate_time(self, current_time):
        current_time = datetime.datetime.now()
        #checks the year
        if current_time.year > self.year:
            self.time_limit = False
        #checks the month
        else:
            if current_time.month > self.month:
                self.time_limit = False
            #checks the day
            else:
                if current_time.day > self.month:
                    self.time_limit = False
        self.save()

    def check_active(self):
        if self.complete == False and self.time_limit == True:
            self.active = True
        self.save()