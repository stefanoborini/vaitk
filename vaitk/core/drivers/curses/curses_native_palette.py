import curses

from vaitk.core.color import rgb_distance
from vaitk.core.drivers.abc.abc_native_palette import ABCNativePalette
from vaitk.core.drivers.curses.curses_native_color import CursesNativeColor


class CursesNativePalette(ABCNativePalette):
    def __init__(self, driver):
        colors = {
            8: [
                (curses.COLOR_BLACK, None, (0x00, 0x00, 0x00)),
                (curses.COLOR_RED, None, (0x80, 0x00, 0x00)),
                (curses.COLOR_GREEN, None, (0x00, 0x80, 0x00)),
                (curses.COLOR_YELLOW, None, (0x80, 0x80, 0x00)),
                (curses.COLOR_BLUE, None, (0x00, 0x00, 0x80)),
                (curses.COLOR_MAGENTA, None, (0x80, 0x00, 0x80)),
                (curses.COLOR_CYAN, None, (0x00, 0x80, 0x80)),
                (curses.COLOR_WHITE, None, (0xc0, 0xc0, 0xc0)),
                (curses.COLOR_BLACK, curses.A_BOLD, (0x64, 0x64, 0x64)),
                (curses.COLOR_RED, curses.A_BOLD, (0xff, 0, 0)),
                (curses.COLOR_GREEN, curses.A_BOLD, (0, 0xff, 0)),
                (curses.COLOR_YELLOW, curses.A_BOLD, (0xff, 0xff, 0)),
                (curses.COLOR_BLUE, curses.A_BOLD, (0, 0, 0xff)),
                (curses.COLOR_MAGENTA, curses.A_BOLD, (0xff, 0, 0xff)),
                (curses.COLOR_CYAN, curses.A_BOLD, (0, 0xff, 0xff)),
                (curses.COLOR_WHITE, curses.A_BOLD, (0xff, 0xff, 0xff)),
            ],
            256: [
                (curses.COLOR_BLACK, None, (0x00, 0x00, 0x00)),
                (curses.COLOR_RED, None, (0x80, 0x00, 0x00)),
                (curses.COLOR_GREEN, None, (0x00, 0x80, 0x00)),
                (curses.COLOR_YELLOW, None, (0x80, 0x80, 0x00)),
                (curses.COLOR_BLUE, None, (0x00, 0x00, 0x80)),
                (curses.COLOR_MAGENTA, None, (0x80, 0x00, 0x80)),
                (curses.COLOR_CYAN, None, (0x00, 0x80, 0x80)),
                (curses.COLOR_WHITE, None, (0xc0, 0xc0, 0xc0)),
                (curses.COLOR_BLACK, curses.A_BOLD, (0x64, 0x64, 0x64)),
                (curses.COLOR_RED, curses.A_BOLD, (0xff, 0, 0)),
                (curses.COLOR_GREEN, curses.A_BOLD, (0, 0xff, 0)),
                (curses.COLOR_YELLOW, curses.A_BOLD, (0xff, 0xff, 0)),
                (curses.COLOR_BLUE, curses.A_BOLD, (0, 0, 0xff)),
                (curses.COLOR_MAGENTA, curses.A_BOLD, (0xff, 0, 0xff)),
                (curses.COLOR_CYAN, curses.A_BOLD, (0, 0xff, 0xff)),
                (curses.COLOR_WHITE, curses.A_BOLD, (0xff, 0xff, 0xff)),
                (9, None, (0xff, 0x00, 0x00)),
                (10, None, (0x00, 0xff, 0x00)),
                (11, None, (0xff, 0xff, 0x00)),
                (12, None, (0x00, 0x00, 0xff)),
                (13, None, (0xff, 0x00, 0xff)),
                (14, None, (0x00, 0xff, 0xff)),
                (15, None, (0xff, 0xff, 0xff)),
                (16, None, (0x00, 0x00, 0x00)),
                (17, None, (0x00, 0x00, 0x5f)),
                (18, None, (0x00, 0x00, 0x87)),
                (19, None, (0x00, 0x00, 0xaf)),
                (20, None, (0x00, 0x00, 0xd7)),
                (21, None, (0x00, 0x00, 0xff)),
                (22, None, (0x00, 0x5f, 0x00)),
                (23, None, (0x00, 0x5f, 0x5f)),
                (24, None, (0x00, 0x5f, 0x87)),
                (25, None, (0x00, 0x5f, 0xaf)),
                (26, None, (0x00, 0x5f, 0xd7)),
                (27, None, (0x00, 0x5f, 0xff)),
                (28, None, (0x00, 0x87, 0x00)),
                (29, None, (0x00, 0x87, 0x5f)),
                (30, None, (0x00, 0x87, 0x87)),
                (31, None, (0x00, 0x87, 0xaf)),
                (32, None, (0x00, 0x87, 0xd7)),
                (33, None, (0x00, 0x87, 0xff)),
                (34, None, (0x00, 0xaf, 0x00)),
                (35, None, (0x00, 0xaf, 0x5f)),
                (36, None, (0x00, 0xaf, 0x87)),
                (37, None, (0x00, 0xaf, 0xaf)),
                (38, None, (0x00, 0xaf, 0xd7)),
                (39, None, (0x00, 0xaf, 0xff)),
                (40, None, (0x00, 0xd7, 0x00)),
                (41, None, (0x00, 0xd7, 0x5f)),
                (42, None, (0x00, 0xd7, 0x87)),
                (43, None, (0x00, 0xd7, 0xaf)),
                (44, None, (0x00, 0xd7, 0xd7)),
                (45, None, (0x00, 0xd7, 0xff)),
                (46, None, (0x00, 0xff, 0x00)),
                (47, None, (0x00, 0xff, 0x5f)),
                (48, None, (0x00, 0xff, 0x87)),
                (49, None, (0x00, 0xff, 0xaf)),
                (50, None, (0x00, 0xff, 0xd7)),
                (51, None, (0x00, 0xff, 0xff)),
                (52, None, (0x5f, 0x00, 0x00)),
                (53, None, (0x5f, 0x00, 0x5f)),
                (54, None, (0x5f, 0x00, 0x87)),
                (55, None, (0x5f, 0x00, 0xaf)),
                (56, None, (0x5f, 0x00, 0xd7)),
                (57, None, (0x5f, 0x00, 0xff)),
                (58, None, (0x5f, 0x5f, 0x00)),
                (59, None, (0x5f, 0x5f, 0x5f)),
                (60, None, (0x5f, 0x5f, 0x87)),
                (61, None, (0x5f, 0x5f, 0xaf)),
                (62, None, (0x5f, 0x5f, 0xd7)),
                (63, None, (0x5f, 0x5f, 0xff)),
                (64, None, (0x5f, 0x87, 0x00)),
                (65, None, (0x5f, 0x87, 0x5f)),
                (66, None, (0x5f, 0x87, 0x87)),
                (67, None, (0x5f, 0x87, 0xaf)),
                (68, None, (0x5f, 0x87, 0xd7)),
                (69, None, (0x5f, 0x87, 0xff)),
                (70, None, (0x5f, 0xaf, 0x00)),
                (71, None, (0x5f, 0xaf, 0x5f)),
                (72, None, (0x5f, 0xaf, 0x87)),
                (73, None, (0x5f, 0xaf, 0xaf)),
                (74, None, (0x5f, 0xaf, 0xd7)),
                (75, None, (0x5f, 0xaf, 0xff)),
                (76, None, (0x5f, 0xd7, 0x00)),
                (77, None, (0x5f, 0xd7, 0x5f)),
                (78, None, (0x5f, 0xd7, 0x87)),
                (79, None, (0x5f, 0xd7, 0xaf)),
                (80, None, (0x5f, 0xd7, 0xd7)),
                (81, None, (0x5f, 0xd7, 0xff)),
                (82, None, (0x5f, 0xff, 0x00)),
                (83, None, (0x5f, 0xff, 0x5f)),
                (84, None, (0x5f, 0xff, 0x87)),
                (85, None, (0x5f, 0xff, 0xaf)),
                (86, None, (0x5f, 0xff, 0xd7)),
                (87, None, (0x5f, 0xff, 0xff)),
                (88, None, (0x87, 0x00, 0x00)),
                (89, None, (0x87, 0x00, 0x5f)),
                (90, None, (0x87, 0x00, 0x87)),
                (91, None, (0x87, 0x00, 0xaf)),
                (92, None, (0x87, 0x00, 0xd7)),
                (93, None, (0x87, 0x00, 0xff)),
                (94, None, (0x87, 0x5f, 0x00)),
                (95, None, (0x87, 0x5f, 0x5f)),
                (96, None, (0x87, 0x5f, 0x87)),
                (97, None, (0x87, 0x5f, 0xaf)),
                (98, None, (0x87, 0x5f, 0xd7)),
                (99, None, (0x87, 0x5f, 0xff)),
                (100, None, (0x87, 0x87, 0x00)),
                (101, None, (0x87, 0x87, 0x5f)),
                (102, None, (0x87, 0x87, 0x87)),
                (103, None, (0x87, 0x87, 0xaf)),
                (104, None, (0x87, 0x87, 0xd7)),
                (105, None, (0x87, 0x87, 0xff)),
                (106, None, (0x87, 0xaf, 0x00)),
                (107, None, (0x87, 0xaf, 0x5f)),
                (108, None, (0x87, 0xaf, 0x87)),
                (109, None, (0x87, 0xaf, 0xaf)),
                (110, None, (0x87, 0xaf, 0xd7)),
                (111, None, (0x87, 0xaf, 0xff)),
                (112, None, (0x87, 0xd7, 0x00)),
                (113, None, (0x87, 0xd7, 0x5f)),
                (114, None, (0x87, 0xd7, 0x87)),
                (115, None, (0x87, 0xd7, 0xaf)),
                (116, None, (0x87, 0xd7, 0xd7)),
                (117, None, (0x87, 0xd7, 0xff)),
                (118, None, (0x87, 0xff, 0x00)),
                (119, None, (0x87, 0xff, 0x5f)),
                (120, None, (0x87, 0xff, 0x87)),
                (121, None, (0x87, 0xff, 0xaf)),
                (122, None, (0x87, 0xff, 0xd7)),
                (123, None, (0x87, 0xff, 0xff)),
                (124, None, (0xaf, 0x00, 0x00)),
                (125, None, (0xaf, 0x00, 0x5f)),
                (126, None, (0xaf, 0x00, 0x87)),
                (127, None, (0xaf, 0x00, 0xaf)),
                (128, None, (0xaf, 0x00, 0xd7)),
                (129, None, (0xaf, 0x00, 0xff)),
                (130, None, (0xaf, 0x5f, 0x00)),
                (131, None, (0xaf, 0x5f, 0x5f)),
                (132, None, (0xaf, 0x5f, 0x87)),
                (133, None, (0xaf, 0x5f, 0xaf)),
                (134, None, (0xaf, 0x5f, 0xd7)),
                (135, None, (0xaf, 0x5f, 0xff)),
                (136, None, (0xaf, 0x87, 0x00)),
                (137, None, (0xaf, 0x87, 0x5f)),
                (138, None, (0xaf, 0x87, 0x87)),
                (139, None, (0xaf, 0x87, 0xaf)),
                (140, None, (0xaf, 0x87, 0xd7)),
                (141, None, (0xaf, 0x87, 0xff)),
                (142, None, (0xaf, 0xaf, 0x00)),
                (143, None, (0xaf, 0xaf, 0x5f)),
                (144, None, (0xaf, 0xaf, 0x87)),
                (145, None, (0xaf, 0xaf, 0xaf)),
                (146, None, (0xaf, 0xaf, 0xd7)),
                (147, None, (0xaf, 0xaf, 0xff)),
                (148, None, (0xaf, 0xd7, 0x00)),
                (149, None, (0xaf, 0xd7, 0x5f)),
                (150, None, (0xaf, 0xd7, 0x87)),
                (151, None, (0xaf, 0xd7, 0xaf)),
                (152, None, (0xaf, 0xd7, 0xd7)),
                (153, None, (0xaf, 0xd7, 0xff)),
                (154, None, (0xaf, 0xff, 0x00)),
                (155, None, (0xaf, 0xff, 0x5f)),
                (156, None, (0xaf, 0xff, 0x87)),
                (157, None, (0xaf, 0xff, 0xaf)),
                (158, None, (0xaf, 0xff, 0xd7)),
                (159, None, (0xaf, 0xff, 0xff)),
                (160, None, (0xd7, 0x00, 0x00)),
                (161, None, (0xd7, 0x00, 0x5f)),
                (162, None, (0xd7, 0x00, 0x87)),
                (163, None, (0xd7, 0x00, 0xaf)),
                (164, None, (0xd7, 0x00, 0xd7)),
                (165, None, (0xd7, 0x00, 0xff)),
                (166, None, (0xd7, 0x5f, 0x00)),
                (167, None, (0xd7, 0x5f, 0x5f)),
                (168, None, (0xd7, 0x5f, 0x87)),
                (169, None, (0xd7, 0x5f, 0xaf)),
                (170, None, (0xd7, 0x5f, 0xd7)),
                (171, None, (0xd7, 0x5f, 0xff)),
                (172, None, (0xd7, 0x87, 0x00)),
                (173, None, (0xd7, 0x87, 0x5f)),
                (174, None, (0xd7, 0x87, 0x87)),
                (175, None, (0xd7, 0x87, 0xaf)),
                (176, None, (0xd7, 0x87, 0xd7)),
                (177, None, (0xd7, 0x87, 0xff)),
                (178, None, (0xd7, 0xaf, 0x00)),
                (179, None, (0xd7, 0xaf, 0x5f)),
                (180, None, (0xd7, 0xaf, 0x87)),
                (181, None, (0xd7, 0xaf, 0xaf)),
                (182, None, (0xd7, 0xaf, 0xd7)),
                (183, None, (0xd7, 0xaf, 0xff)),
                (184, None, (0xd7, 0xd7, 0x00)),
                (185, None, (0xd7, 0xd7, 0x5f)),
                (186, None, (0xd7, 0xd7, 0x87)),
                (187, None, (0xd7, 0xd7, 0xaf)),
                (188, None, (0xd7, 0xd7, 0xd7)),
                (189, None, (0xd7, 0xd7, 0xff)),
                (190, None, (0xd7, 0xff, 0x00)),
                (191, None, (0xd7, 0xff, 0x5f)),
                (192, None, (0xd7, 0xff, 0x87)),
                (193, None, (0xd7, 0xff, 0xaf)),
                (194, None, (0xd7, 0xff, 0xd7)),
                (195, None, (0xd7, 0xff, 0xff)),
                (196, None, (0xff, 0x00, 0x00)),
                (197, None, (0xff, 0x00, 0x5f)),
                (198, None, (0xff, 0x00, 0x87)),
                (199, None, (0xff, 0x00, 0xaf)),
                (200, None, (0xff, 0x00, 0xd7)),
                (201, None, (0xff, 0x00, 0xff)),
                (202, None, (0xff, 0x5f, 0x00)),
                (203, None, (0xff, 0x5f, 0x5f)),
                (204, None, (0xff, 0x5f, 0x87)),
                (205, None, (0xff, 0x5f, 0xaf)),
                (206, None, (0xff, 0x5f, 0xd7)),
                (207, None, (0xff, 0x5f, 0xff)),
                (208, None, (0xff, 0x87, 0x00)),
                (209, None, (0xff, 0x87, 0x5f)),
                (210, None, (0xff, 0x87, 0x87)),
                (211, None, (0xff, 0x87, 0xaf)),
                (212, None, (0xff, 0x87, 0xd7)),
                (213, None, (0xff, 0x87, 0xff)),
                (214, None, (0xff, 0xaf, 0x00)),
                (215, None, (0xff, 0xaf, 0x5f)),
                (216, None, (0xff, 0xaf, 0x87)),
                (217, None, (0xff, 0xaf, 0xaf)),
                (218, None, (0xff, 0xaf, 0xd7)),
                (219, None, (0xff, 0xaf, 0xff)),
                (220, None, (0xff, 0xd7, 0x00)),
                (221, None, (0xff, 0xd7, 0x5f)),
                (222, None, (0xff, 0xd7, 0x87)),
                (223, None, (0xff, 0xd7, 0xaf)),
                (224, None, (0xff, 0xd7, 0xd7)),
                (225, None, (0xff, 0xd7, 0xff)),
                (226, None, (0xff, 0xff, 0x00)),
                (227, None, (0xff, 0xff, 0x5f)),
                (228, None, (0xff, 0xff, 0x87)),
                (229, None, (0xff, 0xff, 0xaf)),
                (230, None, (0xff, 0xff, 0xd7)),
                (231, None, (0xff, 0xff, 0xff)),
                (232, None, (0x08, 0x08, 0x08)),
                (233, None, (0x12, 0x12, 0x12)),
                (234, None, (0x1c, 0x1c, 0x1c)),
                (235, None, (0x26, 0x26, 0x26)),
                (236, None, (0x30, 0x30, 0x30)),
                (237, None, (0x3a, 0x3a, 0x3a)),
                (238, None, (0x44, 0x44, 0x44)),
                (239, None, (0x4e, 0x4e, 0x4e)),
                (240, None, (0x58, 0x58, 0x58)),
                (241, None, (0x60, 0x60, 0x60)),
                (242, None, (0x66, 0x66, 0x66)),
                (243, None, (0x76, 0x76, 0x76)),
                (244, None, (0x80, 0x80, 0x80)),
                (245, None, (0x8a, 0x8a, 0x8a)),
                (246, None, (0x94, 0x94, 0x94)),
                (247, None, (0x9e, 0x9e, 0x9e)),
                (248, None, (0xa8, 0xa8, 0xa8)),
                (249, None, (0xb2, 0xb2, 0xb2)),
                (250, None, (0xbc, 0xbc, 0xbc)),
                (251, None, (0xc6, 0xc6, 0xc6)),
                (252, None, (0xd0, 0xd0, 0xd0)),
                (253, None, (0xda, 0xda, 0xda)),
                (254, None, (0xe4, 0xe4, 0xe4)),
                (255, None, (0xee, 0xee, 0xee)),
            ]
        }

        # The first color pair is always defined with index 0 and contains
        # the default fg and bg colors
        self._color_pairs = [(-1, -1)]

        # Resolves the rgb color to the screen color
        self._color_lookup_cache = {}

        # Resolves fg, bg native index to the associated color pair index
        self._attr_lookup_cache = {}

        self._all_native_colors = [
            CursesNativeColor(idx, attr, rgb)
            for idx, attr, rgb in colors[driver.num_colors]
        ]

    def get_attr_for_colors(self, fg=None, bg=None):
        """Given fg and bg colors, find and return the correct attribute code
        to apply with chgat"""
        fg_screen = None if fg is None else self._find_closest_color(fg)
        bg_screen = None if bg is None else self._find_closest_color(bg)

        if (fg_screen, bg_screen) in self._attr_lookup_cache:
            return self._attr_lookup_cache[(fg_screen, bg_screen)]

        fg_index = -1 if fg_screen is None else fg_screen.color_idx()
        bg_index = -1 if bg_screen is None else bg_screen.color_idx()

        attr = self._get_pair_attr_from_index(fg_index, bg_index)

        if fg_screen and fg_screen.attr:
            attr |= fg_screen.attr()

        self._attr_lookup_cache[(fg_screen, bg_screen)] = attr
        return attr

    def _get_pair_attr_from_index(self, fg_index, bg_index):
        t = (fg_index, bg_index)

        if t in self._color_pairs:
            pair_index = self._color_pairs.index((fg_index, bg_index))
        else:
            pair_index = len(self._color_pairs)
            curses.init_pair(pair_index, fg_index, bg_index)
            self._color_pairs.append((fg_index, bg_index))

        attr = curses.color_pair(pair_index)

        return attr
        # Init color pairs

    def _find_closest_color(self, color):
        native_color = self._color_lookup_cache.get(color.rgb)
        if native_color is not None:
            return native_color

        closest = sorted(
            [
                (rgb_distance(color.rgb, native_color.rgb), native_color)
                for native_color in self._all_native_colors
            ])[0][1]

        self._color_lookup_cache[color.rgb] = closest

        return closest


