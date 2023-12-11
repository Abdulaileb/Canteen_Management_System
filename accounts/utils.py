def is_manager(user):
    return user.is_authenticated and user.is_manager