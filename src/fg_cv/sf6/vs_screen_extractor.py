"""VsScreen Extractor for SF6"""

from fg_cv.vs_screen_extractor_base import VsScreenExtractorBase


class VsScreenExtractor(VsScreenExtractorBase):
    def get_ringname(self, player_num: int) -> str:
        return None

    def get_character(self, player_num: int) -> str:
        return None

    def get_stage(self) -> str:
        return None
