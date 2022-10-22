from operator import itemgetter
from typing import Dict, List


def sort_dictionary(source: Dict[any, any], by_value=True, reverse=True) -> List[any]:
    if by_value:
        return sorted(source.items(), key=itemgetter(1), reverse=reverse)
    return sorted(source.items(), key=itemgetter(0), reverse=reverse)
