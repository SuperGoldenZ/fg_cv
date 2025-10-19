"""
fg_cv: A library for extracing information from fighting games
"""

__title__ = "fg_cv"
__author__ = "Alexander Golden"
__license__ = "MIT"
__js__ = None
__js_url__ = None

from fg_cv.vs_screen_extractor import VsScreenExtractor
from fg_cv.match_over_extractor import MatchOverExtractor
from fg_cv.flexible_cv import FlexibleCv
from fg_cv.round_start_screen_extractor import RoundStartScreenExtractor
from fg_cv.combo_cv import ComboCv
from fg_cv.lifebar_cv import LifebarCv