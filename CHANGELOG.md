# Table of contents

- [1.2.1](#121)
- [1.2.0](#120)
- [1.1.0](#110)
- [1.0.1](#101)
- [1.0.0](#100)
- [0.0.7](#007)
- [0.0.6](#006)
- [0.0.5](#005)
- [0.0.4](#004)
- [0.0.3](#003)
- [0.0.2](#002)

## 1.2.1
- Fixed an SF6 match over screen false positive on super and critical art flashes, which paint the Play Again dialog's navy and near-white palette over the same region of the screen
[#39](https://github.com/SuperGoldenZ/fg_cv/pull/39)

- The SF6 match over layout no longer counts a duplicated pixel probe twice, and matches on parts of the dialog panel that stay constant while the highlight sweep animates
[#39](https://github.com/SuperGoldenZ/fg_cv/pull/39)

## 1.2.0
- SF6 replay list rows now recognize the new character Yasmine, via P1 and P2 portrait references
[#36](https://github.com/SuperGoldenZ/fg_cv/pull/36)

- Portrait references smaller than the region of interest are skipped with a warning instead of raising from `cv2.matchTemplate`
[#36](https://github.com/SuperGoldenZ/fg_cv/pull/36)

## 1.1.0
- Detect VF5 online replay download screens where the Download option is highlighted but disabled
[#32](https://github.com/SuperGoldenZ/fg_cv/pull/32)

- New `DrawScreenExtractor` for detecting the VF5 round-end DRAW banner
[#33](https://github.com/SuperGoldenZ/fg_cv/pull/33)

- Fixed VF5 round start screen false positives by matching on the round-intro P1/P2 history bands
[#33](https://github.com/SuperGoldenZ/fg_cv/pull/33)

- Round start layouts can now set their own `threshold` instead of the hardcoded value of 5
[#33](https://github.com/SuperGoldenZ/fg_cv/pull/33)

## 1.0.1
- SF6 match details round result extraction via template matching, including chip damage, critical art, overdrive, perfect, super art, timeout, and draw icons
[#29](https://github.com/SuperGoldenZ/fg_cv/pull/29)

- SF6 draw detection in match details and replay list
[#29](https://github.com/SuperGoldenZ/fg_cv/pull/29)

- SF6 replay list `is_bottom` detection (whether the selected row is the last in the list)
[#29](https://github.com/SuperGoldenZ/fg_cv/pull/29)

- Fixed SF6 match over screen false positive
[#29](https://github.com/SuperGoldenZ/fg_cv/pull/29)

- Detect VF5 delete-replay screens (delete selected in replay submenu, delete confirmation yes/no)
[#29](https://github.com/SuperGoldenZ/fg_cv/pull/29)

## 1.0.0
- SF6 replays list screen recognition, with CV/OCR to read the selected row: characters, ring names, MR, winner, date/time, and match type
[#26](https://github.com/SuperGoldenZ/fg_cv/pull/26)

- SF6 replay details screen recognition and Replay ID OCR
[#26](https://github.com/SuperGoldenZ/fg_cv/pull/26)

- Detect VF5 online replay download, download complete, and loading screens
[#26](https://github.com/SuperGoldenZ/fg_cv/pull/26)

## 0.0.7
- Now detects when no matches in playerlog
[#22](https://github.com/SuperGoldenZ/fg_cv/issues/22)

## 0.0.6
- Can now detect VF5 player data screen when Battle Log highlighted
[#19](https://github.com/SuperGoldenZ/fg_cv/issues/19)

- Fixed bug where VF5 player data screen sometimes not recognized
[#18](https://github.com/SuperGoldenZ/fg_cv/issues/18)

## 0.0.5
- Additional VF5 REVO World Stage screen recognition
[#16](https://github.com/SuperGoldenZ/fg_cv/issues/16)

## 0.0.4
- Aoi vs Lei Fei VS Screen detected properly
[#12](https://github.com/SuperGoldenZ/fg_cv/issues/12)

- Ranked / Replay Download CV
[#10](https://github.com/SuperGoldenZ/fg_cv/issues/10)

## 0.0.3
- Correctly recognize Lei Fei vs Wolf screen
[#6](https://github.com/SuperGoldenZ/fg_cv/issues/6)

## 0.0.2
- Detect VF5 REVO World Stage replay menu screens
[#2](https://github.com/SuperGoldenZ/fg_cv/issues/2)
