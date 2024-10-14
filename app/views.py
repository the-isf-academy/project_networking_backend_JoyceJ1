# views.py

from banjo.urls import route_get, route_post
from settings import BASE_URL
from .models import Scavenger_hunt

@route_post(BASE_URL + 'new', args={'location':str, 'hint': str, 'description': str, 'year': int, 'month': int, 'day': int, 'code': str})
def new_scavenger_hunt(args):
    new_scavenger_hunt = Scavenger_hunt(
        location = args['location'],
        hint = args['hint'],
        description = args['description'],
        year = args['year'],
        month = args['month'],
        day = args['day'],
        code = args['code'],
        complete = False,
        active = True,
        likes = 0
    )

    new_scavenger_hunt.save()

    return {'scavenger hunt': new_scavenger_hunt.json_response()}


@route_get(BASE_URL + 'get')
def get_scavenger_hunt(args):
    if Scavenger_hunt.active == True:
        get_scavenger_hunt = Scavenger_hunt.objects.order_by('?')
        return{'riddle':get_scavenger_hunt[0].json_response()}
    

@route_post(BASE_URL + 'like')
def increase_like(args):
    #if the user has a current scavenger hunt
    current_scavenger_hunt = Scavenger_hunt.objects.exists()
    current_scavenger_hunt.increase_likes()
        
    return{'fortune':current_scavenger_hunt.json_response()}
