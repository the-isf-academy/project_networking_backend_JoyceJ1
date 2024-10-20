# views.py

from banjo.urls import route_get, route_post
from settings import BASE_URL
from .models import Scavenger_hunt
import datetime

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
        past_time = False,
        likes = 0
    )

    new_scavenger_hunt.save()

    return {'scavenger hunt': new_scavenger_hunt.json_response()}

# @route_get(BASE_URL + 'all')
# def get_scavenger_hunt(args):
#     scavenger_hunt = []

#     if len(Scavenger_hunt.objects.all())  > 0:

#         for hunt in Scavenger_hunt.objects.all():
#             scavenger_hunt.append(hunt.everything())

#         return {'scavenger hunts':scavenger_hunt}
    

@route_get(BASE_URL + 'get')
def get_active_scavenger_hunt(args):
    if Scavenger_hunt.objects.filter(current=True).exists():
        return {'error': 'A current scavenger hunt is already in progress'}
    
    #if hunt_limit == True:
        #return {'err0r': 'Already completed scavenger today, try again tomorrow'}
    today = datetime.date.today()
    if Scavenger_hunt.objects.filter(completed_day=today.day).exists():
        return {'error': 'Already completed scavenger today, try again tomorrow'}

    active_hunts = Scavenger_hunt.objects.filter(active=True)

    for hunt in active_hunts:
        # print(f"Processing Hunt: {hunt.description}, Date: {hunt.year}-{hunt.month}-{hunt.day}")
        hunt.calculate_time()
        # print(f"After calculation: Past Time: {hunt.past_time}, Active: {hunt.active}")
        
        if hunt.check_active():
            selected_hunt = active_hunts.order_by('?').first()
            if selected_hunt:
                # print(f"Selected Hunt: {selected_hunt.description}, Date: {selected_hunt.year}-{selected_hunt.month}-{selected_hunt.day}")
                selected_hunt.current = True
                selected_hunt.active = False
                selected_hunt.save()
                return {'scavenger_hunt': selected_hunt.json_response()}

    return {'error': 'No active scavenger hunts available'}

@route_get(BASE_URL + 'current')
def show_current(args):
    if Scavenger_hunt.objects.filter(current=True).exists():
            current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
            if current_scavenger_hunt.past_time == False:
                return{'scavenger hunt':current_scavenger_hunt.json_response()}
            else:
                return{'scavenger hunt':'over time limit'}
    else:
        return{'Error':'no scavenger hunt exists'}

#adds likes to the scavenger hunt
@route_post(BASE_URL + 'like')
def increase_like(args):
        if Scavenger_hunt.objects.filter(current=True).exists():
            current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
            current_scavenger_hunt.calculate_time()
            if current_scavenger_hunt.past_time ==  False:
                current_scavenger_hunt.increase_likes()
        
                return{'scavenger hunt':current_scavenger_hunt.json_response()}
            else:
                return{'scavenger hunt':'over time limit'}
        else:
            return{'Error':'no scavenger hunt exists'}

@route_get(BASE_URL + 'hint')
def get_hint(args):
    #if the user has a current scavenger hunt
    if Scavenger_hunt.objects.filter(current=True).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
        current_scavenger_hunt.calculate_time()
        if current_scavenger_hunt.past_time ==  False:
            return{'scavenger hunt':current_scavenger_hunt.hint_response()}
        else:
            return{'scavenger hunt':'over time limit'}
    else:
        return{'Error':'no scavenger hunt exists'}
    
@route_post(BASE_URL + 'check', args={'code': str})
def complete_scavenger_hunt(args):
    if Scavenger_hunt.objects.filter(current=True).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True)[0]
        if current_scavenger_hunt.check_code(args['code']) == True and current_scavenger_hunt.past_time == False:
            current_scavenger_hunt.current = False
            current_scavenger_hunt.calc_time_completed()
            current_scavenger_hunt.save()
            return{'Correct!':'scavenger hunt completed'}
        else:
            return {'error': 'Inaccurate code or over time limit'}
    else:
        return {'error': 'No scavenger hunt exists'}


@route_get(BASE_URL + 'completed_hunts')
def complete_scavenger_hunt(args):
    completed_scavenger_hunts = []

    if len(Scavenger_hunt.objects.filter(complete=True)) > 0:

        for hunt in Scavenger_hunt.objects.filter(complete=True):
            completed_scavenger_hunts.append(hunt.completed_response())

        return {'scavenger hunts':completed_scavenger_hunts}
    else:
        return {'scavenger hunts':'No completed scavenger hunt'}

