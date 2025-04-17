_current_image_url = None

def set_current_image_url(url):
    global _current_image_url
    _current_image_url = url

def get_current_image_url():
    return _current_image_url