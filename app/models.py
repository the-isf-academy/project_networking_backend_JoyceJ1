# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField, ForeignKey
import datetime

class User(Model):
    username = StringField()
    user_completed = IntegerField()
    posted_scavenger_hunts = IntegerField()

    def user_info_response(self):
        return{
            'username' : self.username,
            'posted hunts' : self.posted_scavenger_hunts,
            # 'all posted hunts' : Scavenger_hunt.,
            'completed hunts' : self.user_completed
            # 'all completed hunts': Scavenger_hunt.completed_response()
        }

    def delete_with_hunts(self):
        Scavenger_hunt.objects.filter(my_user=self).delete()
        self.delete()

    def increase_user_completed(self):
        self.user_completed += 1
        self.save()

    def increase_posted_hunts(self):
        self.posted_scavenger_hunts += 1
        self.save()


class Scavenger_hunt(Model):
    # user_posted = ForeignKey(User, related_name='posted_hunts')  # User who posted the hunt
    my_user = ForeignKey(User)  # User engaging with the hunt
    completed_user = StringField()
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
            'scavenger hunt id' : self.id,
            'location' : self.location,
            'hint' : self.hint,
            'description' : self.description,
            'time limit' : f"{self.year}-{self.month}-{self.day}",
            'time completed' : self.time_completed,
            'code' : self.code,
            'likes' : self.likes,
            # 'user posted' : self.user_posted,
            'user completed' : self.completed_user
        }

    def json_response(self):

        return {
            # 'my_user' : self.my_user,
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
