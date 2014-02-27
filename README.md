Django Generic Follow
=====================

[![Build Status](https://travis-ci.org/gizmag/django-generic-follow.png?branch=master)](https://travis-ci.org/gizmag/django-generic-follow)

django-generic-follow is a system to allow users to follow any model in a Django
project.

## Installation / Setup

### Basics
First, install the package with pip

```bash
pip install django-generic-follow
```

Then add `generic_follow` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...,
    'generic_follow',
)
```

### User Model
If you are using the `auth.User` user model, the user instance methods will be 
set up for you. If you are using a custom User model, you will need to apply the
`UserFollowMixin`

```python
from django.contrib.auth.models import AbstractUser
from generic_follow.model_mixins import UserFollowMixin

class MyCustomUser(UserFollowMixin, AbstractUser):
    ...
```

### Target Models
To add the convenience methods to models that will be followed apply the
`TargetFollowMixin`

```python
from django.db import models
from generic_follow.model_mixins import TargetFollowMixin


class Band(TargetFollowMixin, models.Model):
    name = models.CharField(max_length=255)
```


## Usage

### Follow/Unfollow
To make a user follow a model instance use the `user.follow` method

```python
user = User.objects.first()
band = Band.objects.get(name='Foals')

user.follow(band)
```

To make a user unfollow a model instance simply call `user.unfollow`

```python
user.unfollow(band)
```

Checking if a user currently follows a model instance involves calling
`user.is_following`

```python
user.is_following(band)
# true/false
```

### Retrieval Methods

To see all model instances that a user is following call the
`user.get_follow_set` method.

```python
user.get_follow_set()
# [<Band: foals>]
```

Optionally, the `model` kwarg can be provided to only return followed instances
of that model type

```python
user.get_follow_set(Photographer)
# []
```

On the follow target, `model.get_follower_set` can be called to retrieve all
followers

```python
band.get_follower_set()
```

### Batch Operations
To make a list of users follow a given model instance call the `create_batch`
manager method

```python
user2 = ...

Follow.objects.create_batch(users=[user, user2], target=band)
```

To perform the inverse, call the `delete_batch` manager method

```python
Follow.objects.delete_batch(users=[user, user2], target=band)
```

To make some users follow a model instance, and others unfollow the same model
instance in the same command, use `update_batch`. The `users_follow` kwarg
accepts a 2-tuple of user instance, and a boolean indicating if this user should
be following the instance.

```python
Follow.objects.update_batch(
    target=band,
    users_follow=[(user, True), (user2, False)]
)
# user will now be following foals, user2 will now not be following foals
```

## Contributions

Pull requests / issues welcome!
