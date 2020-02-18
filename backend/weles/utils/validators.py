from typing import Dict, Union, Text


def url_or_file_validator(data: Dict) -> Union[None, Text]:
    """
    This function is not typical validator. It is more universal approach that allow to be used inside forms
    and serializers, so you can share same validation code. Unfortunately Django forms and REST Framework serializers
    do not share ValidationError exception even though they are named the same
    :param data: dictionary with data
    :return: None if everything is OK, error message in case of problems
    """
    if not data.get('file') and not data.get('url'):
        return "You need to provide one of this fields: file or URL"

    if data.get('file') and data.get('url'):
        return "You cannot provide both of this fields: file or URL"
