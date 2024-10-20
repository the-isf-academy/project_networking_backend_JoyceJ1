# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField, ForeignKey
import datetime

# class User(Model):
#     user_name = StringField()

class Scavenger_hunt(Model):
    # user_posted = ForeignKey(User)
    location = StringField()
    hint = StringField()
    # image = BlobField()
    description = StringField()
    year = IntegerField()
    month = IntegerField()
    day = IntegerField()
    past_time = BooleanField()
    code = StringField()
    complete = BooleanField()
    active = BooleanField()
    # user_completed = StringField()
    # comments = StringField()
    likes = IntegerField()
    current = BooleanField()
    time_completed = StringField()
    completed_day = IntegerField()

    # def everything(self):
    #     return{
    #         'location' : self.location,
    #         'timelimit' : f"{self.year}-{self.month}-{self.day}",
    #         'past time' : self.past_time,
    #         'complete' : self.complete,
    #         'active' : self.active,
    #         'current' : self.current,
    #         'current_time' : datetime.datetime.now(),

    #     }
    
    def completed_response(self):
        return{
            'location' : self.location,
            'hint' : self.hint,
            'description' : self.description,
            'time limit' : f"{self.year}-{self.month}-{self.day}",
            'time completed' : self.time_completed,
            'code' : self.code,
            'likes' : self.likes
        }

    def json_response(self):

        return {
            # 'user_posted' : self.user_posted,
            'description' : self.description,
            # 'image' : self.image,
            'time_limit' : f"{self.year}-{self.month}-{self.day}",
            # 'comments' : self.comments,
            'likes' : self.likes,
        }
    
    def hint_response(self):

        return {

            'description' : self.description,
            'hint' : self.hint,
            # 'image' : self.image,
            'time_limit' : f"{self.year}-{self.month}-{self.day}",
            # 'comments' : self.comments,
            'likes' : self.likes,
        }

    def increase_likes(self):
        #add likes by 1
        self.likes += 1
        self.save()

    # def check_code(self):
    #     if len(self.code) < 5:
    #         print("Your code needs to be at least 6 letters long!")

    def check_code(self, user_code):
        #checks if the code is correct
        if self.code == user_code:
            self.complete = True
            self.active = False
            self.save()
            return True
        else:
            return False

    
    # def calculate_time(self):
    #     current_time = datetime.datetime.now()
    #     #checks the year
    #     if current_time.year > self.year:
    #         self.past_time = True
    #         self.active = False
    #     #checks the month
    #     elif current_time.year == self.year:
    #         if current_time.month > self.month:
    #             self.past_time = True
    #             self.active = False
    #         #checks the day
    #         elif current_time.year == self.year and current_time.month == self.month:
    #             if current_time.day > self.day:
    #                 self.past_time = True
    #                 self.active = False
    #     self.save()

    def calculate_time(self):
        current_date = datetime.date.today()
        hunt_date = datetime.date(self.year, self.month, self.day)
        
        print(f"Current Date: {current_date}")
        print(f"Hunt Date: {hunt_date}")

        if current_date > hunt_date:
            self.past_time = True
            self.active = False
        else:
            self.past_time = False
            self.active = True

        print(f"Past Time: {self.past_time}, Active: {self.active}")
        self.save()


    def check_active(self):
        return not self.complete and not self.current and not self.past_time
    
    def calc_time_completed(self):
        complete_time = datetime.datetime.now()
        self.time_completed = f"{complete_time.year}-{complete_time.month}-{complete_time.day}"
        self.completed_day = complete_time.day
        self.save()

    # def hunt_limit(self):
    #     if self.completed_day == datetime.datetime.now().day:
    #         print(f"{self.completed_day},{datetime.datetime.now().day}")
    #         return True
