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
        current = False,
        likes = 0
    )

    new_scavenger_hunt.save()

    return {'scavenger hunt': new_scavenger_hunt.json_response()}


@route_get(BASE_URL + 'get')
def get_scavenger_hunt(args):
    for scavenger_hunt in Scavenger_hunt.objects.filter(active=True):
        if scavenger_hunt.check_active() == True:
            print(scavenger_hunt)
            get_scavenger_hunt = scavenger_hunt.objects.order_by('?')
            get_scavenger_hunt[0].current = True
            get_scavenger_hunt[0].active = False
            print(scavenger_hunt)
            print(get_scavenger_hunt)
            return{'scavenger hunt':get_scavenger_hunt[0].json_response()}
    else:
        return{'Error':'you already have a scavenger hunt!'}
    

#adds likes to the scavenger hunt
@route_post(BASE_URL + 'like')
def increase_like(args):
        if Scavenger_hunt.objects.filter(current=True).exists:
            current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
            current_scavenger_hunt.increase_likes()
        
            return{'scavenger hunt':current_scavenger_hunt.json_response()}
        else:
            return{'Error':'no scaveneger hunt exists'}

@route_get(BASE_URL + 'hint')
def get_hint(args):
    #if the user has a current scavenger hunt
    if Scavenger_hunt.objects.filter(current=True).exists:
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
        return{'scavenger hunt':current_scavenger_hunt.hint_response()}
    
@route_post(BASE_URL + 'complete', args={'code': str})
def complete_scavenger_hunt(args):
    if Scavenger_hunt.objects.filter(current=True).exists:
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
        if current_scavenger_hunt.check_code(args['code']) == True:
            return{'Correct!':'scavenger hunt completed'}
        else:
            return {'Error':'unaccurate code, try again'}
        
