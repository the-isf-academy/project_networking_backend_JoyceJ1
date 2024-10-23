# Project Networking


> **Don't forget to edit this `README.md` file**
>
> If you're interested in how to format markdown, click [here](https://www.markdownguide.org/basic-syntax/#images-1)

## API Overview
### Introduction
<p>The Scavenger Hunt API provides a way to manage scavenger hunts, including creating new hunts, managing user accounts, and tracking user progress and rankings.The target audience is the ISF comminuty.</p>

Understanding APIs
How APIs Work
APIs (Application Programming Interfaces) are sets of rules and protocols for building and interacting with software applications. They define how different software components should interact. APIs are used to enable the communication between different software systems, often allowing data to be shared and functionalities to be extended.

### Class

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
    hunt_instance.calculate
    ```


### Endpoints

*Replace this with a guide to your endpoints and model. You can write a Markdown chart [here](https://www.tablesgenerator.com/markdown_tables)*



#Describe the differebce between get and current 
#Enter '' for strings
#Explain user cannot get scavenger hunts posted by themselves
---

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
    - `models.py` - `Fortune` model
    - `views.py` - endpoints
- `database.sqlite`  
- `README.md` 

**To start a Banjo server:** `banjo` 
- [Banjo Documentation](https://the-isf-academy.github.io/banjo_docs/)



