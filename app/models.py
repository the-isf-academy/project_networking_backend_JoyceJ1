# models.py
from banjo.models import Model, StringField, IntegerField, BooleanField, ForeignKey
import datetime

# Creates a class called User
class User(Model):
    username = StringField()  # User's username
    user_completed = IntegerField()  # Number of hunts the user has completed
    posted_scavenger_hunts = IntegerField()  # Number of hunts the user has posted

    def user_info_response(self):
        # Returns user's information including posted and completed hunts
        return {
            'username': self.username,
            'posted hunts': self.posted_scavenger_hunts,
            'completed hunts': self.user_completed
        }
    
    def user_rank_response(self):
        # Returns user's ranking information
        return {
            'username': self.username,
            'completed hunts': self.user_completed
        }
    
    def delete_with_hunts(self):
        # Deletes user and their associated hunts
        Scavenger_hunt.objects.filter(my_user=self).delete()
        self.delete()
    
    def increase_user_completed(self):
        # Increases the number of completed hunts by 1
        self.user_completed += 1
        self.save()
    
    def increase_posted_hunts(self):
        # Increases the number of posted hunts by 1
        self.posted_scavenger_hunts += 1
        self.save()

# Creates a new class called Scavenger_hunt
class Scavenger_hunt(Model):
    user_posted = ForeignKey(User, related_name='posted_hunts')  # User who posted the hunt
    my_user = ForeignKey(User, null=True, blank=True, related_name='engaged_hunts')  # User engaging with the hunt
    completed_user = ForeignKey(User, null=True, blank=True, related_name='completed_hunts')  # User who completed the hunt
    location = StringField()  # Location of the hunt
    hint = StringField()  # Hint for the hunt
    description = StringField()  # Description of the hunt
    year = IntegerField()  # Year of the hunt
    month = IntegerField()  # Month of the hunt
    day = IntegerField()  # Day of the hunt
    past_time = BooleanField()  # Indicates if the hunt is past time
    code = StringField()  # Code for the hunt
    complete = BooleanField()  # Indicates if the hunt is complete
    active = BooleanField()  # Indicates if the hunt is active
    likes = IntegerField()  # Number of likes for the hunt
    current = BooleanField()  # Indicates if the hunt is current
    time_completed = StringField()  # Time when the hunt was completed
    completed_day = IntegerField()  # Day when the hunt was completed

    def completed_response(self):
        # Returns response when hunt is completed
        return {
            'scavenger_hunt_id': self.id,
            'location': self.location,
            'hint': self.hint,
            'description': self.description,
            'time_limit': f"{self.year}-{self.month}-{self.day}",
            'time_completed': self.time_completed,
            'code': self.code,
            'likes': self.likes,
            'user_completed': self.completed_user.username if self.completed_user else 'Not been completed'
        }
    
    def json_response(self):
        # Returns JSON response for the hunt
        return {
            'description': self.description,
            'time_limit': f"{self.year}-{self.month}-{self.day}",
            'likes': self.likes,
        }
    
    def hint_response(self):
        # Returns response containing hint
        return {
            'description': self.description,
            'hint': self.hint,
            'time_limit': f"{self.year}-{self.month}-{self.day}",
            'likes': self.likes,
        }
    
    def increase_likes(self):
        # Adds a like to the hunt
        self.likes += 1
        self.save()

    def check_code(self, user_code):
        # Checks if the provided code is correct
        if self.code == user_code:
            self.complete = True
            self.active = False
            self.save()
            return True
        else:
            return False
    
    def calculate_time(self):
        # Calculates if the hunt is past time and updates its status
        current_date = datetime.date.today()
        print(current_date)
        hunt_date = datetime.date(self.year, self.month, self.day)
        print(hunt_date)

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
        # Checks if the hunt is active
        return not self.complete and not self.current and not self.past_time and self.active
    
    def calc_time_completed(self):
        # Calculates the time when the hunt was completed
        complete_time = datetime.datetime.now()
        self.time_completed = f"{complete_time.year}-{complete_time.month}-{complete_time.day}"
        self.completed_day = complete_time.day
        self.save()
