from typing import Any, Iterable, List, Tuple, Optional
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain

def merge_chain_plain(message_chain: MessageChain) -> MessageChain:
    result = []

    plain = []
    for i in message_chain.__root__:
        if not isinstance(i, Plain):
            if plain:
                result.append(Plain("".join(plain)))
                plain.clear() # 清空缓存
            result.append(i)
        else:
            plain.append(i.text)
    else:
        if plain:
            result.append(Plain("".join(plain)))
            plain.clear() # 清空缓存
    return MessageChain.create(type(message_chain.__root__)(result)) # 维持 Mutable 状态

def silce_chain_start(message_chain: MessageChain, slice_start: Tuple[int, Optional[int]]):
    first_slice = message_chain.__root__[slice_start[0]:]
    if slice_start[1] and first_slice: # text slice
        if not isinstance(first_slice[0], Plain):
            raise TypeError("the sliced chain does not starts with a Plain: {}".format(first_slice[0]))
        final_text = first_slice[0].text[slice_start[1]:]
        return MessageChain.create([
            *([Plain(final_text)] if final_text else []),
            *first_slice[1:]
        ])
    return MessageChain.create(first_slice)

def silce_chain_stop(message_chain: MessageChain, slice_stop: Tuple[int, Optional[int]]):
    first_slice = message_chain.__root__[:slice_stop[0]]
    if slice_stop[1] and first_slice: # text slice
        if not isinstance(first_slice[-1], Plain):
            raise TypeError("the sliced chain does not starts with a Plain: {}".format(first_slice[0]))
        final_text = first_slice[-1].text[:slice_stop[1]]
        return MessageChain.create([
            *first_slice[:-1],
            *([Plain(final_text)] if final_text else [])
        ])
    return MessageChain.create(first_slice)

class InsertGenerator:
    base: Iterable[Any]
    insert_items: List[Any]

    def __init__(self, base_iterable: Iterable, pre_items: List[Any] = None) -> None:
        self.base = base_iterable
        self.insert_items = pre_items or []
    
    def __iter__(self):
        for i in self.base:
            if self.insert_items:
                yield from self.insert_items.pop()
            yield i