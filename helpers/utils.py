from django.urls import reverse, resolve


# gets the absolute path and returns the resolve of the url
def url_resolve(url, *args, **kwargs):
    url = reverse(url, args=[*args], kwargs=kwargs.get("kwargs"))
    return resolve(url)
