# views.py

from banjo.urls import route_get, route_post
from settings import BASE_URL
from .models import Scavenger_hunt, User
import datetime

@route_post(BASE_URL + 'create_user', args={'username': str})
def create_user(args):
    if User.objects.filter(username=args['username']).exists():
        return {'error': 'Username already exists. Please choose a different username.'}
    
    new_user = User(
        username=args['username']
    )
    new_user.save()
    return{'user':new_user.user_info_response()}


@route_post(BASE_URL + 'new', args={'username': str, 'location': str, 'hint': str, 'description': str, 'year': int, 'month': int, 'day': int, 'code': str})
def new_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}

    new_scavenger_hunt = Scavenger_hunt(
        user_posted=user,  # Set the user who posted the hunt
        location=args['location'],
        hint=args['hint'],
        description=args['description'],
        year=args['year'],
        month=args['month'],
        day=args['day'],
        code=args['code'],
        complete=False,
        active=True,
        current=False,
        past_time=False,
        likes=0
    )

    new_scavenger_hunt.save()
    user.increase_posted_hunts()
    user.save()
    return {'scavenger hunt': new_scavenger_hunt.json_response()}


# @route_get(BASE_URL + 'all')
# def get_scavenger_hunt(args):
#     scavenger_hunt = []

#     if len(Scavenger_hunt.objects.all())  > 0:

#         for hunt in Scavenger_hunt.objects.all():
#             scavenger_hunt.append(hunt.everything())

#         return {'scavenger hunts':scavenger_hunt}

@route_get(BASE_URL + 'get', args={'username': str})
def get_active_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        return {'error': 'A current scavenger hunt is already in progress'}
    
    #if hunt_limit == True:
        #return {'err0r': 'Already completed scavenger today, try again tomorrow'}
    today = datetime.date.today()
    if Scavenger_hunt.objects.filter(completed_day=today.day, my_user=user).exists():
        return {'error': 'Already completed scavenger today, try again tomorrow'}

    active_hunts = Scavenger_hunt.objects.filter(active=True).exclude(user_posted=user)
    # active_hunts = Scavenger_hunt.objects.filter(active=True) | Scavenger_hunt.objects.filter(current=True, my_user=user)
    # active_hunts = active_hunts.exclude(my_user=user).distinct()

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
                selected_hunt.my_user = user
                selected_hunt.save()
                return {'scavenger_hunt': selected_hunt.json_response()}

    return {'error': 'No active scavenger hunts available'}

@route_get(BASE_URL + 'current', args={'username': str})
def show_current(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}

    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
            current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
            if current_scavenger_hunt.past_time == False:
                return{'scavenger hunt':current_scavenger_hunt.json_response()}
            else:
                return{'scavenger hunt':'over time limit'}
    else:
        return{'Error':'no scavenger hunt exists'}

#adds likes to completed scavenger hunts
@route_post(BASE_URL + 'like', args={'username': str, 'hunt_id': int})
def increase_like(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    if Scavenger_hunt.objects.filter(id=args['hunt_id'], my_user=user, complete=True).exists():
        completed_hunt = Scavenger_hunt.objects.get(id=args['hunt_id'], my_user=user)
        completed_hunt.increase_likes()
        return{'scavenger hunt':completed_hunt.json_response()}
    else:
        return{'Error':'no completed scavenger hunt exists'}

@route_get(BASE_URL + 'hint', args={'username': str})
def get_hint(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    #if the user has a current scavenger hunt
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
        current_scavenger_hunt.calculate_time()
        if current_scavenger_hunt.past_time ==  False:
            return{'scavenger hunt':current_scavenger_hunt.hint_response()}
        else:
            return{'scavenger hunt':'over time limit'}
    else:
        return{'Error':'no scavenger hunt exists'}
    
@route_post(BASE_URL + 'check', args={'username': str, 'code': str})
def complete_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
        if current_scavenger_hunt.check_code(args['code']) == True and current_scavenger_hunt.past_time == False:
            current_scavenger_hunt.current = False
            current_scavenger_hunt.completed_user = user
            current_scavenger_hunt.calc_time_completed()
            current_scavenger_hunt.save()
            user.increase_user_completed()
            return{'Correct!':'scavenger hunt completed'}
        else:
            return {'error': 'Inaccurate code or over time limit'}
    else:
        return {'error': 'No scavenger hunt exists'}



# @route_get(BASE_URL + 'completed_hunts', args={'username': str})
# def complete_scavenger_hunt(args):
#     try:
#         user = User.objects.get(username=args['username'])
#     except User.DoesNotExist:
#         return {'error': 'User does not exist. Please create a user first.'}
#     #check user
#     completed_scavenger_hunts = []

#     if len(Scavenger_hunt.objects.filter(complete=True, my_user=user)) > 0:

#         for hunt in Scavenger_hunt.objects.filter(complete=True, my_user=user):
#             completed_scavenger_hunts.append(hunt.completed_response())

#         return {'scavenger hunts':completed_scavenger_hunts}
#     else:
#         return {'scavenger hunts':'No completed scavenger hunt'}

@route_post(BASE_URL + 'delete_user', args={'username': str})
def delete_user(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    user.delete_with_hunts()
    return {'status': 'User and related scavenger hunts deleted'}

@route_post(BASE_URL + 'delete_hunt', args={'username': str, 'hunt_id': int})
def delete_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}

    if Scavenger_hunt.objects.filter(id=args['hunt_id'], user_posted=user).exists():
        delete_hunt = Scavenger_hunt.objects.get(id=args['hunt_id'], user_posted=user)
        delete_hunt.delete()
        return {'status': 'Scavenger hunt deleted successfully'}
    else:
        return {'error': 'No scavenger hunt found'}

# @route_get(BASE_URL + 'view_user', args={'username': str})
# def create_user(args):
#     try:
#         user = User.objects.get(username=args['username'])
#     except User.DoesNotExist:
#         return {'error': 'User does not exist. Please create a user first.'}
    
#     return{'user':user.user_info_response()}

@route_get(BASE_URL + 'view_user', args={'username': str})
def view_user(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}

    # Get completed scavenger hunts for the user
    completed_scavenger_hunts = []
    if Scavenger_hunt.objects.filter(complete=True, my_user=user).exists():
        for hunt in Scavenger_hunt.objects.filter(complete=True, my_user=user):
            completed_scavenger_hunts.append(hunt.completed_response())
    elif completed_scavenger_hunts == []:
        completed_scavenger_hunts = 'No scavenger hunts completed'

    # Get scavenger hunts posted by the user
    
    posted_scavenger_hunts = []
    if Scavenger_hunt.objects.filter(user_posted=user).exists():
        for hunt in Scavenger_hunt.objects.filter(user_posted=user):
            posted_scavenger_hunts.append(hunt.completed_response())
    elif completed_scavenger_hunts == []:
        completed_scavenger_hunts = 'No scavenger hunts posted'

    users_ranked = User.objects.order_by('-user_completed')
    rank = list(users_ranked).index(user) + 1

    user_info = user.user_info_response()
    user_info['rank'] = rank
    user_info['completed_scavenger_hunts'] = completed_scavenger_hunts
    user_info['posted_scavenger_hunts'] = posted_scavenger_hunts

    return {'user': user_info}

@route_get(BASE_URL + 'rankings')
def get_rankings(args):
    # Get all users ordered by completed hunts, descending
    users = User.objects.order_by('-user_completed')
    rank_list = []
    for index, user in enumerate(users, start=1):
        user_info = user.user_rank_response()
        user_info['rank'] = index
        rank_list.append(user_info)
    return {'ranking_list': rank_list}
