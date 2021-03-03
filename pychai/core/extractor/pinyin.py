'''拼音拆分模块'''
from typing import List

from ...base import Character
from .characterFeatureExtractor import CharacterFeatureExtractor


class Pinyin(CharacterFeatureExtractor):
    '''拼音拆分器'''
    def __init__(self, characters: List[Character]):
        super().__init__(characters)

    # TODO: 实现方法
    def extract(self):
        pass

    # TODO: 实现方法
    @classmethod
    def require(cls):
        pass