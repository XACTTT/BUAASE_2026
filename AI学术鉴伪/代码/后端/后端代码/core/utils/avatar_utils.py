def safe_avatar_url(user):
    """安全获取用户头像URL，头像不存在时返回None"""
    avatar = getattr(user, 'avatar', None)
    if avatar and avatar.name and avatar.storage.exists(avatar.name):
        return avatar.url
    return None
