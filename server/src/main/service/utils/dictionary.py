from operator import itemgetter
from typing import Dict


def sort_dictionary(source: Dict[any, any], by_value=True, reverse=True) -> Dict[any, any]:
    if by_value:
        return {k: v for k, v in sorted(source.items(),
                                        key=itemgetter(1),
                                        reverse=reverse)}
    return {k: v for k, v in sorted(source.items(),
                                    key=itemgetter(0),
                                    reverse=reverse)}