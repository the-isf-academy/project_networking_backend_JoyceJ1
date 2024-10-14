# models.py

from banjo.models import Model, StringField, IntegerField, FloatField, BooleanField

class Scavenger_hunt(Model):
    # user_posted = StringField()
    location = IntegerField()
    # hint = StringField()
    # image = BlobField()
    description = StringField()
    # time_limit = IntegerField()
    code = StringField()
    complete = BooleanField()
    active = BooleanField()
    # user_completed = StringField()
    # comments = StringField()
    likes = IntegerField()

    def json_response(self):

        return {
            'user_posted' : self.user_posted,
            'description' : self.description,
            # 'image' : self.image,
            # 'time_limit' : self.time_limit,
            # 'comments' : self.comments,
            'likes' : self.likes,
        }
    
    def print_location(self, block, floor, room):
        self.location = print(f'{block}{floor}{room}')

    def increase_likes(self):
        self.likes += 1
        self.save()

    def check_code(self, user_code):
        if self.code == user_code:
            print("Congratulations!")
            self.complete = True
            self.active = False
        else:
            print("Not Correct...")


