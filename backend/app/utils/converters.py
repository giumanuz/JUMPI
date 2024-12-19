import re

def snake_to_camel_case(snake_str: str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def snake_to_camel(snake_obj):
    if isinstance(snake_obj, dict):
        return {snake_to_camel_case(k): snake_to_camel(v) for k, v in snake_obj.items()}
    elif isinstance(snake_obj, list):
        return [snake_to_camel(i) for i in snake_obj]
    else:
        return snake_obj


def camel_to_snake_case(camel_str: str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel_str]).lstrip('_')


def camel_to_snake(camel_obj):
    if isinstance(camel_obj, dict):
        return {camel_to_snake_case(k): camel_to_snake(v) for k, v in camel_obj.items()}
    elif isinstance(camel_obj, list):
        return [camel_to_snake(i) for i in camel_obj]
    else:
        return camel_obj

def merge_lines(text):
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip() 