from django.utils import timezone




def persian_numbers_converter(mystr):
    jnumbers = {
        '0' : '۰',
        '1' : '۱',
        '2' : '۲',
        '3' : '۳',
        '4' : '۴',
        '5' : '۵',
        '6' : '۶',
        '7' : '۷',
        '8' : '۸',
        '9' : '۹',
    }

    for e, p in jnumbers.items():
        mystr = mystr.replace(e, p)
    return mystr


def elapsed_time(created):
    time = (timezone.now() - created).total_seconds()

    if time < 1:
        return 'right_now'
    elif time < 60:
        return f'{int(time)} seconds ago'
    elif time < 3600:
        if time // 60 == 1:
            return '1 minute ago'
        return f'{int(time//60)} minutes ago'
    elif time < 86400:
        if time // 3600 == 1:
            return '1 hour ago'
        return f'{int(time // 3600)} hours ago'
    elif time < 604800:
        if time // 86400 == 1:
            return '1 day ago'
        return f'{int(time // 86400)} days ago'
    elif time // 604800 == 1:
        return '1 week ago'
    return f'{int(time // 604800)} weeks ago'


def get_title(title, length=None):
    length = length or 30
    return title if len(title) < length else title[:length]


def format_price(number, lang='en'):
    if number is None:
        return 0

    reversed_number = str(number)[::-1]
    formatted_parts = []

    for i in range(0, len(reversed_number), 3):
        part = reversed_number[i:i + 3]
        formatted_parts.append(part)

    if lang == 'en':
        return ",".join(formatted_parts)[::-1]
    
    return persian_numbers_converter(",".join(formatted_parts)[::-1])

