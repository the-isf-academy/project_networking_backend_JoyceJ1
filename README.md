# Scavenger Hunt API

## API Overview
### Introduction

Understanding APIs
An Application Programming Interface (API) is like a bridge between different software applications. It allows them to communicate with each other and exchange data, handles with data tranfer. They make systems work together seemlessly.

How GET and POST requests work:
Client Action --> HTTP Request --> Server Processing --> HTTP Response --> Client Recieves Data
|      	| Client Action                                                                        	| HTTP Request                                                                                         	| Server Processing                                           	| HTTP Response                                                                                                       	| Client Receives Data                                                                   	|
|------	|--------------------------------------------------------------------------------------	|------------------------------------------------------------------------------------------------------	|-------------------------------------------------------------	|---------------------------------------------------------------------------------------------------------------------	|----------------------------------------------------------------------------------------	|
| **Get**  	| The client initiates the process by typing a URL into the browser and pressing enter 	| The browser sends an HTTP GET request to the server.                                                 	| The server receives the GET request and processes it        	| The server sends back an HTTP response containing the requested data                                                	| The browser displays the response                                                      	|
| **Post** 	| The client fills out a form or sends data through the browser.                       	| The browser sends an HTTP POST request to the server, including the data in the body of the request. 	| The server receives the POST request and processes the data 	| The server sends back an HTTP response, which could be a confirmation message or the result of processing the data. 	| The browser displays the response, and the client sees the result of the POST request. 	|

<p>The Scavenger Hunt API provides a way to manage scavenger hunts, including creating new hunts, managing user accounts, and tracking user progress and rankings. The target audience is the ISF comminuty.</p>

## Class

_________


### User Class
<p>model represents a user in the system. Here are its fields:</p>

| **Field Name**         	| **Type**     	| **Description**                                         	|
|------------------------	|--------------	|---------------------------------------------------------	|
| username               	| StringField  	| The username of the user.                               	|
| user_completed         	| IntegerField 	| The number of scavenger hunts the user has completed.   	|
| posted_scavenger_hunts 	| IntegerField 	| The number of scavenger hunts the user has posted.      	|
| rank                   	| IntegerField 	| The user's rank based on the number of completed hunts. 	|

_____

### User Model

The `User` model represents a user in the system. Here are its methods explained in detail:

#### `user_info_response()`
- **Method**:
    ```python
    def user_info_response(self):
        return {
            'username': self.username,
            'rank': self.rank,
            'posted hunts': self.posted_scavenger_hunts,
            'completed hunts': self.user_completed
        }
    ```
- **Explanation**: This method returns a dictionary containing key user information, such as `username`, `rank`, number of `posted hunts`, and number of `completed hunts`. 
- **Return Value**:
    ```json
    {
        "username": "example_user",
        "rank": 1,
        "posted hunts": 5,
        "completed hunts": 10
    }
    ```

#### `delete_with_hunts()`
- **Method**:
    ```python
    def delete_with_hunts(self):
        Scavenger_hunt.objects.filter(my_user=self).delete()
        self.delete()
    ```
- **Explanation**: This method `filter`s and use `.delete()` to delete all scavenger hunts associated with the user `my_user` and then deletes the user itself. It ensures there are no orphaned scavenger hunts left behind when a user is deleted.
- **Usage**:
    ```python
    user_instance.delete_with_hunts()
    ```

#### `increase_user_completed()`
- **Method**:
    ```python
    def increase_user_completed(self):
        self.user_completed += 1
        self.save()
        self.update_rank()
    ```
- **Explanation**: This method increments the `user_completed` count by one each time it is called using the `+= 1`. It then `save()`s the updated user object and `update_rank()` based on the new number of completed scavenger hunts.
- **Usage**:
    ```python
    user_instance.increase_user_completed()
    ```

#### `increase_posted_hunts()`
- **Method**:
    ```python
    def increase_posted_hunts(self):
        self.posted_scavenger_hunts += 1
        self.save()
    ```
- **Explanation**: This method increments the `posted_scavenger_hunts` count by one and saves the updated user object `+= 1`. It is called whenever a user posts a new scavenger hunt.
- **Usage**:
    ```python
    user_instance.increase_posted_hunts()
    ```

#### `update_rank()`
- **Method**:
    ```python
    def update_rank(self):
        self.rank = User.objects.filter(user_completed__gt=self.user_completed).count() + 1
        self.save()
    ```
- **Explanation**: This method calculates the user's rank (`self.rank`) based on the number of scavenger hunts they have completed compared to other users with `user_completed__gt`. It sets the user's rank to `+ 1` than the count of users who have completed more hunts.
- **Usage**:
    ```python
    user_instance.update_rank()
    ```

_____


### Scavenger Hunt Class
<p>The Scavenger_hunt model represents a scavenger hunt. Here are its fields:</p>

| **Field Name** 	| **Type**     	| **Description**                                              	|
|----------------	|--------------	|--------------------------------------------------------------	|
| Field Name     	| Type         	| Description                                                  	|
| user_posted    	| ForeignKey   	| The user who posted the scavenger hunt.                      	|
| my_user        	| ForeignKey   	| The user engaging with the scavenger hunt.                   	|
| completed_user 	| ForeignKey   	| The user who completed the scavenger hunt.                   	|
| location       	| StringField  	| The location of the scavenger hunt.                          	|
| hint           	| StringField  	| The hint for the scavenger hunt.                             	|
| description    	| StringField  	| The description of the scavenger hunt.                       	|
| year           	| IntegerField 	| The year by which the scavenger hunt needs to be completed.  	|
| month          	| IntegerField 	| The month by which the scavenger hunt needs to be completed. 	|
| day            	| IntegerField 	| The day by which the scavenger hunt needs to be completed.   	|
| past_time      	| BooleanField 	| Indicates whether the hunt is past its completion date.      	|
| code           	| StringField  	| The code to complete the scavenger hunt.                     	|
| complete       	| BooleanField 	| Indicates whether the hunt is completed.                     	|
| active         	| BooleanField 	| Indicates whether the hunt is active.                        	|
| likes          	| IntegerField 	| The number of likes for the scavenger hunt.                  	|
| current        	| BooleanField 	| Indicates whether the hunt is currently being engaged.       	|
| time_completed 	| StringField  	| The time the hunt was completed.                             	|
| completed_day  	| IntegerField 	| The day the hunt was completed.                              	|

_____

### Scavenger Hunt Model

#### `completed_response()`
- **Method**:
    ```python
    def completed_response(self):
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
    ```
- **Explanation**: This method returns a dictionary containing detailed information about a completed scavenger hunt. The fields included are `scavenger_hunt_id`, `location`, `hint`, `description`, `time_limit`, `time_completed`, `code`, `likes`, and `user_completed`. This is useful for displaying comprehensive details of a scavenger hunt.

- **Return Value**:
    ```json
    {
        "scavenger_hunt_id": 1,
        "location": "B606",
        "hint": "In a bar of stars",
        "description": "Lollipop candy",
        "time_limit": "2024-12-31",
        "time_completed": "2024-12-25",
        "code": "X12345",
        "likes": 10,
        "user_completed": "example_user"
    }
    ```

#### `json_response()`
- **Method**:
    ```python
    def json_response(self):
        return {
            'description': self.description,
            'time_limit': f"{self.year}-{self.month}-{self.day}",
            'likes': self.likes
        }
    ```
- **Explanation**: This method provides a simplified JSON response with essential details about a scavenger hunt. The fields included are `description`, `time_limit`, and `likes`. This is useful for scenarios where only brief information about a hunt is needed.

- **Return Value**:
    ```json
    {
        "description": "Lollipop candy",
        "time_limit": "2024-12-31",
        "likes": 10
    }
    ```

#### `hint_response()`
- **Method**:
    ```python
    def hint_response(self):
        return {
            'description': self.description,
            'hint': self.hint,
            'time_limit': f"{self.year}-{self.month}-{self.day}",
            'likes': self.likes
        }
    ```
- **Explanation**: This method returns a dictionary that includes the `description`, `hint`, `time_limit`, and `likes` for a scavenger hunt. It is particularly useful for providing hints to users without revealing the entire scavenger hunt details.

- **Return Value**:
    ```json
    {
        "description": "Lollipop candy",
        "hint": "In a bar of stars",
        "time_limit": "2024-12-31",
        "likes": 10
    }
    ```

#### `increase_likes()`
- **Method**:
    ```python
    def increase_likes(self):
        self.likes += 1
        self.save()
    ```
- **Explanation**: This method increments the `likes` count for a scavenger hunt `+= 1` and then `save()`s the updated count. It is useful for tracking the popularity of different scavenger hunts.

- **Usage**:
    ```python
    hunt_instance.increase_likes()
    ```

#### `check_code()`
- **Method**:
    ```python
    def check_code(self, user_code):
        if self.code == user_code:
            self.complete = True
            self.active = False
            self.save()
            return True
        else:
            return False
    ```
- **Explanation**: This method checks if the provided `user_code` matches the scavenger hunt's code. If it matches, it marks the hunt as `complete` and `inactive`, then saves these changes. This is essential for validating the completion of a scavenger hunt. Returns True if the code matches and the hunt with be set as completed, False adn still active otherwise.

- **Return Value**:
    ```python
    hunt_instance.check_code('X12345')  
    ```

#### `calculate_time()`
- **Method**:
    ```python
    def calculate_time(self):
        current_date = datetime.date.today()
        hunt_date = datetime.date(self.year, self.month, self.day)
        if current_date > hunt_date:
            self.past_time = True
            self.active = False
        else:
            self.past_time = False
            self.active = True
        self.save()
    ```
- **Explanation**: This method calculates whether the scavenger hunt is `past_time` based on the current date and the hunt's `hunt_date`. It updates the `past_time` and `active` fields accordingly and saves the changes. This is critical for determining the validity period of a scavenger hunt.

- **Usage**:
    ```python
    hunt_instance.calculate()
    ```

#### `check_active()`
- **Method**:
    ```python
       def check_active(self):
        return not self.complete and not self.current and not self.past_time and self.active
    ```
- **Explanation**: This method checks if the active is True, the complete if False, and if the current is False.

- **Usage**:
    ```python
    hunt_instance.check_active()
    ```

#### `calc_time_completed()`
- **Method**:
    ```python
    def calc_time_completed(self):
        complete_time = datetime.datetime.now()
        self.time_completed = f"{complete_time.year}-{complete_time.month}-{complete_time.day}"
        self.completed_day = complete_time.day
        self.save()
    ```
- **Explanation**: Calculates the time when the hunt was completed

--------

## Endpoints

### Create User
| **Endpoint** 	| `/create_user` 	|        	|
|--------------	|----------------	|--------	|
| **Method**   	| POST           	|        	|
| **Args**     	| `username`     	| String 	|

**Description**: Creates a new user with a unique username.

**Code**:
```python
@route_post(BASE_URL + 'create_user', args={'username': str})
def create_user(args):
    if User.objects.filter(username=args['username']).exists():
        return {'error': 'Username already exists. Please choose a different username.'}
    new_user = User(username=args['username'])
    new_user.save()
    return {'user': new_user.user_info_response()}
```
**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/create_user
{
    "username": "Joyce"
}
```

**Response**:
```python
{
    "user": {
        "username": "Joyce",
        "rank": 0,
        "posted hunts": 0,
        "completed hunts": 0
    }
}
```

**Error Messages**:

```python
{'error': 'Username already exists. Please choose a different username.'}
```
Returned when the username provided already exists in the database.

--------

### New Scavenger Hunt
| **Endpoint** 	| `/new`        	|         	|
|----------	|-------------	|---------	|
| **Method**   	| POST        	|         	|
| **Args**    	| `username`    	| String  	|
|          	| `location`    	| String  	|
|          	| `hint`        	| String  	|
|          	| `description` 	| String  	|
|          	| `year`        	| Integer 	|
|          	| `month`       	| Integer 	|
|          	| `day`         	| Integer 	|
|          	| `code`        	| String  	|

**Description**: Creates a new scavenger hunt and links it to a user, storing it as a scavenger hunt posted by that user.

**Code**:
```python
@route_post(BASE_URL + 'new', args={'username': str, 'location': str, 'hint': str, 'description': str, 'year': int, 'month': int, 'day': int, 'code': str})
def new_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    new_scavenger_hunt = Scavenger_hunt(
        user_posted=user,
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
```

**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/new
{
    "username": "john_doe",
    "location": "Central Park",
    "hint": "Near the big fountain",
    "description": "Find the hidden key",
    "year": 2023,
    "month": 12,
    "day": 25,
    "code": "abc123"
}
```

**Response**:
```python
{
    "scavenger hunt": {
        "location": "Central Park",
        "hint": "Near the big fountain",
        "description": "Find the hidden key",
        "time_limit": "2023-12-25",
        "code": "abc123",
        "likes": 0
    }
}
```

**Error Messages**:
```python
{
    "error": "User does not exist. Please create a user first."
}
```
Returned when the provided username does not exist in the database. Need to create a user first, check the `create_user` endpoint.

---------

### Get Active Scavenger Hunt
| **Endpoint** 	| `/new`        	|         	|
|----------	|-------------	|---------	|
| **Method**   	| POST        	|         	|
| **Args**     	| `username`    	| String  	|
|          	| `location`    	| String  	|
|          	| `hint`        	| String  	|
|          	| `description` 	| String  	|
|          	| `year`        	| Integer 	|
|          	| `month`       	| Integer 	|
|          	| `day`         	| Integer 	|
|          	| `code`        	| String  	|

**Description**: Retrieves an active scavenger hunt for a user, the user cannot get scavenger hunts posted by themselves; scavenger hunts that other people are already doing; if they already have a scavenger hunt that is not completed yet; if they already completed a scavenger hunt on that day.

**Code**:
```python
@route_get(BASE_URL + 'get', args={'username': str})
def get_active_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        return {'error': 'A current scavenger hunt is already in progress'}
    today = datetime.date.today()
    if Scavenger_hunt.objects.filter(completed_day=today.day, my_user=user).exists():
        return {'error': 'Already completed scavenger today, try again tomorrow'}
    active_hunts = Scavenger_hunt.objects.filter(active=True).exclude(user_posted=user)
    for hunt in active_hunts:
        hunt.calculate_time()
        if hunt.check_active():
            selected_hunt = active_hunts.order_by('?').first()
            if selected_hunt:
                selected_hunt.current = True
                selected_hunt.active = False
                selected_hunt.my_user = user
                selected_hunt.save()
                return {'scavenger_hunt': selected_hunt.json_response()}
    return {'error': 'No active scavenger hunts available'}

```

**Example Usage**:
```python
GET http://127.0.0.1:5000/ScavengerHunt/new
{
    "username" = "Joyce"
}

```

**Response**:
```python
{
    "scavenger_hunt": {
        "location": "Central Park",
        "hint": "Near the big fountain",
        "description": "Find the hidden key",
        "time_limit": "2023-12-25",
        "code": "abc123",
        "likes": 0
    }
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'error': 'A current scavenger hunt is already in progress'}
{'error': 'Already completed scavenger today, try again tomorrow'}
{'error': 'No active scavenger hunts available'}
```

----------

### Show Current Scavenger Hunt
| **Endpoint** 	| `/current` 	|        	|
|----------	|----------	|--------	|
| **Method**   	| GET      	|        	|
| **Args**     	| `username` 	| String 	|


**Description**: Displays the current scavenger hunt in progress for a user, the scavenger hunt in progress is the scavenger hunt that the user gets. Current is different to user get as the user can only get one time that shows the scavenger hunt they got, but the current can show unlimited times of the scavenger hunt the user gets.

**Code**:
```python
@route_get(BASE_URL + 'current', args={'username': str})
def show_current(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}

    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
            current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
            current_scavenger_hunt.calculate_time()
            if current_scavenger_hunt.past_time == False:
                return{'scavenger hunt':current_scavenger_hunt.json_response()}
            elif current_scavenger_hunt.past_time == True:
                return{'scavenger hunt':'over time limit'}
    else:
        return{'Error':'no scavenger hunt exists'}
```

**Example Usage**:
```python
GET http://127.0.0.1:5000/ScavengerHunt/current
{
    "username" = "Joyce"
}
```

**Response**:
```python
{
    "scavenger hunt": {
        "location": "Central Park",
        "hint": "Near the big fountain",
        "description": "Find the hidden key",
        "time_limit": "2023-12-25",
        "code": "abc123",
        "likes": 0
    }
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'Error': 'no scavenger hunt exists'}
{'scavenger hunt':'over time limit'}
```

------

### Increase Like
| **Endpoint** 	| `/like`    	|         	|
|----------	|----------	|---------	|
| **Method**   	| POST     	|         	|
| **Args**     	| `username` 	| String  	|
|          	| `hunt_id`  	| Integer 	|

**Description**: Adds a like to a completed scavenger hunt, the `hunt_id` can be found when calling the `view_user` endpoint.

**Code**:
```python
@route_post(BASE_URL + 'like', args={'username': str, 'hunt_id': int})
def increase_like(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    if Scavenger_hunt.objects.filter(id=args['hunt_id'], my_user=user, complete=True).exists():
        completed_hunt = Scavenger_hunt.objects.get(id=args['hunt_id'], my_user=user)
        completed_hunt.increase_likes()
        return {'scavenger hunt': completed_hunt.json_response()}
    else:
        return {'Error': 'no completed scavenger hunt exists'}
```

**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/like
{
    "username": "john_doe",
    "hunt_id": 1
}

```

**Response**:
```python
{
  "scavenger hunt": {
    "description": "blablabla",
    "time_limit": "2025-12-4",
    "likes": 1
  }
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'Error': 'no completed scavenger hunt exists'}
```

-----

### Get Hint
| **Endpoint** 	| `/hint`     	|        	|
|----------	|-----------	|--------	|
| **Method**   	| GET       	|        	|
| **Args**     	| `username`  	| string 	|
|          	|           	|        	|

**Description**: Retrieves a hint for the current scavenger hunt.

**Code**:
```python
@route_get(BASE_URL + 'hint', args={'username': str})
def get_hint(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
        current_scavenger_hunt.calculate_time()
        if current_scavenger_hunt.past_time == False:
            return {'scavenger hunt': current_scavenger_hunt.hint_response()}
        else:
            return {'scavenger hunt': 'over time limit'}
    else:
        return {'Error': 'no scavenger hunt exists'}
```

**Example Usage**:
```python
GET http://127.0.0.1:5000/ScavengerHunt/hint
{
    "username" = "john_doe"
}
```

**Response**:
```python
{
    "scavenger hunt": {
        "description": "Find the hidden key",
        "hint": "Near the big fountain",
        "time_limit": "2023-12-25"
    }
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'scavenger hunt': 'over time limit'}
{'Error': 'no scavenger hunt exists'}
```

 -------

### Complete Scavenger Hunt
| **Endpoint** 	| `/check`   	|        	|
|----------	|----------	|--------	|
| **Method**   	| POST     	|        	|
| **Args**     	| `username` 	| string 	|
|          	| `code`     	| string 	|

**Description**: Marks a scavenger hunt as completed by checking the code that the user (that got the scavenger hunt) inputs to the code that the `posted_used` input.

**Code**:
```python
@route_post(BASE_URL + 'check', args={'username': str, 'code': str})
def complete_scavenger_hunt(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    
    if Scavenger_hunt.objects.filter(current=True, my_user=user).exists():
        current_scavenger_hunt = Scavenger_hunt.objects.filter(current=True, my_user=user)[0]
        current_scavenger_hunt.calculate_time()
        if current_scavenger_hunt.check_code(args['code']) == True and current_scavenger_hunt.past_time == False:
            current_scavenger_hunt.current = False
            current_scavenger_hunt.completed_user = user
            current_scavenger_hunt.calc_time_completed()
            current_scavenger_hunt.save()
            user.increase_user_completed()
            return{'Correct!':'scavenger hunt completed'}
        elif current_scavenger_hunt.check_code(args['code']) == False and current_scavenger_hunt.past_time == False:
            return {'error': 'Inaccurate code, try again'}
        elif current_scavenger_hunt.past_time == True:
            return {'scavenger hunt':'over time limit'}
    else:
        return {'error': 'No scavenger hunt exists'}
```

**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/check
{
    "username": "john_doe",
    "code": "abc123"
}
```

**Response**:
```python
{
    "Correct!": "scavenger hunt completed"
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'error': 'Inaccurate code, try again'}
{'scavenger hunt':'over time limit'}
{'error': 'No scavenger hunt exists'}
```

------

### Delete User
| **Endpoint** 	| `/delete_user` 	|        	|
|----------	|--------------	|--------	|
| **Method**   	| POST         	|        	|
| **Args**     	| `username`     	| String 	|
|          	|              	|        	|

**Description**: Deletes a user and associated scavenger hunts.

**Code**:
```python
@route_post(BASE_URL + 'delete_user', args={'username': str})
def delete_user(args):
    try:
        user = User.objects.get(username=args['username'])
    except User.DoesNotExist:
        return {'error': 'User does not exist. Please create a user first.'}
    user.delete_with_hunts()
    return {'status': 'User and related scavenger hunts deleted'}
```

**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/delete_user
{
    "username": "john_doe"
}
```

**Response**:
```python
{
    "status": "User and related scavenger hunts deleted"
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
```

------

### Delete Scavenger Hunt
| **Endpoint** 	| `/delete_hunt` 	|         	|
|----------	|--------------	|---------	|
| **Method**   	| POST         	|         	|
| **Args**     	| `username`     	| String  	|
|          	| `hunt_id`      	| Integer 	|

**Description**: The user that the posted scavenger can delete the specific scavenger hunt, by using getting the hunt_id.

**Code**:
```python
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
```

**Example Usage**:
```python
POST http://127.0.0.1:5000/ScavengerHunt/delete_hunt
{
    "username": "john_doe",
    "hunt_id": 1
}
```

**Response**:
```python
{
    "status": "Scavenger hunt deleted successfully"
}

```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
{'error': 'No scavenger hunt found'}
```

-------

### View User
| **Endpoint** 	| `/view_user` 	|        	|
|----------	|------------	|--------	|
| **Method**   	| GET        	|        	|
| **Args**     	| `username`   	| String 	|
|          	|            	|        	|


**Description**: Retrieves detailed information about a user, including completed and posted scavenger hunts.

**Code**:
```python
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
    elif posted_scavenger_hunts == []:
        posted_scavenger_hunts = 'No scavenger hunts posted'

    users_ranked = User.objects.order_by('-user_completed')
    rank = list(users_ranked).index(user) + 1

    user_info = user.user_info_response()
    user_info['rank'] = rank
    user_info['completed_scavenger_hunts'] = completed_scavenger_hunts
    user_info['posted_scavenger_hunts'] = posted_scavenger_hunts

    return {'user': user_info}
```

**Example Usage**:
```python
GET http://127.0.0.1:5000/ScavengerHunt/view_user
{
    "username" = "Joyce"
}
```

**Response**:
```python
{
    "user": {
        "username": "john_doe",
        "rank": 1,
        "completed_scavenger_hunts": [],
        "posted_scavenger_hunts": []
    }
}
```

**Error Messages**:
```python
{'error': 'User does not exist. Please create a user first.'}
```

------

### Get Rankings
| **Endpoint** 	| `/rank` 	|   	|
|----------	|-------	|---	|
| **Method**   	| GET   	|   	|
| **Args**     	| `None`  	|   	|
|          	|       	|   	|


**Description**: Gets a list of users ranked by number of completed scavenger hunts.

**Code**:
```python
@route_get(BASE_URL + 'rank')
def get_rankings(args):
    # Get all users ordered by completed hunts, descending
    users = User.objects.order_by('-user_completed')
    rank_list = []
    for index, user in enumerate(users, start=1):
        user_info = user.user_rank_response()
        user_info['rank'] = index
        rank_list.append(user_info)
    return {'ranking_list': rank_list}
```

**Example Usage**:
```python
GET http://127.0.0.1:5000/ScavengerHunt/rank

```

**Response**:
```python
{
    "ranking_list": [
        {
            "username": "john_doe",
            "rank": 1,
            "completed hunts": 5
        }
    ]
}
```

## All error messages and suggestions to solve:
```python
{'error': 'Username already exists. Please choose a different username.'}
#The string entered for the username in the create_user endpoint already exists, please enter a different username.
{'error': 'User does not exist. Please create a user first.'}
#When calling endpoints that need to enter an username, if the username is not a user (create_user), then the username does not exist.
{'error': 'A current scavenger hunt is already in progress'}
#The user already got an avaliable scavenger hunt as their current scavenger hunt (can be seen in the current endpoint), so they cannot get another unless they complete the current scavenger hunt.
{'error': 'Already completed scavenger today, try again tomorrow'}
#The user cannot get another scavenger hunt as they have already completed a scavenger hunt today. The user will be able to get a new scavenger hunt the next day.
{'error': 'No active scavenger hunts available'}
#There are no scavenger hunts that other users posted, they might not be active (other people are working on the scavenger hunt; the time limit has passed; scavenger hunts are already completed etc...).
{'Error':'no completed scavenger hunt exists'}
#The user can only like the scavenger hunts that they completed, the user has no completed scavenger hunt. User needs to get a scavenger hunt using the get endpoint and then complete the hunt using the code endpoint.
{'scavenger hunt':'over time limit'}
#The current scavenger hunt exceeded the time limit that the user posted set, so the scavenger hunt is not active anymore.
{'error': 'Inaccurate code, try again'}
#The code that the user entered trying to complete the current scavenger hunt is not the same as the code that the uer posted set, the scavenger hunt is not completed.
{'error': 'No scavenger hunt exists'}
#The user does not have a current scavenger hunt, use the get endpoint to get a scavenger hunt.
{'error': 'No scavenger hunt found'}
#The hunt id that the user provided is not found, which means that either the scavenger hunt with the id does not exist, or the user did not post the hunt so that they can not delete other user's scavenger hunt.
```



## Setup

Open terminal

💻 Enter the poetry shell
```python
poetry shell
```

💻 Call banjo server
```python
banjo --debug
```

>return:
```python
Starting development server at http://127.0.0.1:5000/
Quit the server with CONTROL-C.
```

Open HTTPie

Enter BASE_URL:
```python
http://127.0.0.1:5000/ScavengerHunt/
```

Call endpoints after the BASE_URL, explained above.


### Contents

Here's what is included:
- `\app`
    - `models.py` - `Scavenger Hunt` model and `User` model
    - `views.py` - endpoints
- `database.sqlite`  
- `README.md` 

**To start a Banjo server:** `banjo` 
- [Banjo Documentation](https://the-isf-academy.github.io/banjo_docs/)



