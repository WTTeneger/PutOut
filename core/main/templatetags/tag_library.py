from django import template

register = template.Library()


@register.filter()
def to_int(value):
    return int(value)



@register.filter()
def get_item(dictionary, key):

    for obj in dictionary:
        if obj[0] == key:
            return obj[1]


@register.filter()
def addf(first, second):
    T = float(first) + float(second)
    return round(T, 2)
    # return range(, 2)


@register.filter()
def lenght(first):
    return len(first)


@register.filter()
def transto(first):
    return len(first)
