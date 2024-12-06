def snake_to_camel_case(snake_str: str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def snake_to_camel_dict(snake_dict: dict):
    return {snake_to_camel_case(k): v for k, v in snake_dict.items()}


def camel_to_snake_case(camel_str: str):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel_str]).lstrip('_')


def camel_to_snake_dict(camel_dict: dict):
    return {camel_to_snake_case(k): v for k, v in camel_dict.items()}
