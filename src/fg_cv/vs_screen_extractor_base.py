from abc import ABC, abstractmethod


class VsScreenExtractorBase(ABC):
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self):
        self.frame = None

    def set_frame(self, frame) -> None:
        self.frame = frame

    @abstractmethod
    def get_ringname(self, player_num: int, debug_ringname:bool = False) -> str:
        """Return the name of the given player."""
        pass

    @abstractmethod
    def get_character(self, player_num: int) -> str:
        """Return the character name of the given player."""
        pass

    @abstractmethod
    def get_stage(self) -> str:
        """Return the stage name."""
        pass
