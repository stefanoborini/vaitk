class VColor:
    def __init__(self, rgb):
        self._rgb = rgb

    @property
    def rgb(self):
        return self._rgb

    def hex_string(self):
        return "%0.2X%0.2X%0.2X" % self.rgb

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    @staticmethod
    def distance(color1, color2):
        return (color1.r - color2.r)**2 + (color1.g - color2.g)**2 + \
            (color1.b - color2.b)**2

    class tuple:
        @staticmethod
        def distance(color1, color2):
            return (color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + \
                (color1[2] - color2[2])**2


class VGlobalColor:
    """This class defines colors according to the rgb palette"""
    term_0 = VColor(rgb=(0x00, 0x00, 0x00))
    term_1 = VColor(rgb=(0x80, 0x00, 0x00))
    term_2 = VColor(rgb=(0x00, 0x80, 0x00))
    term_3 = VColor(rgb=(0x80, 0x80, 0x00))
    term_4 = VColor(rgb=(0x00, 0x00, 0x80))
    term_5 = VColor(rgb=(0x80, 0x00, 0x80))
    term_6 = VColor(rgb=(0x00, 0x80, 0x80))
    term_7 = VColor(rgb=(0xc0, 0xc0, 0xc0))
    term_8 = VColor(rgb=(0x80, 0x80, 0x80))
    term_9 = VColor(rgb=(0xff, 0x00, 0x00))
    term_10 = VColor(rgb=(0x00, 0xff, 0x00))
    term_11 = VColor(rgb=(0xff, 0xff, 0x00))
    term_12 = VColor(rgb=(0x00, 0x00, 0xff))
    term_13 = VColor(rgb=(0xff, 0x00, 0xff))
    term_14 = VColor(rgb=(0x00, 0xff, 0xff))
    term_15 = VColor(rgb=(0xff, 0xff, 0xff))
    term_16 = VColor(rgb=(0x00, 0x00, 0x00))
    term_17 = VColor(rgb=(0x00, 0x00, 0x5f))
    term_18 = VColor(rgb=(0x00, 0x00, 0x87))
    term_19 = VColor(rgb=(0x00, 0x00, 0xaf))
    term_20 = VColor(rgb=(0x00, 0x00, 0xd7))
    term_21 = VColor(rgb=(0x00, 0x00, 0xff))
    term_22 = VColor(rgb=(0x00, 0x5f, 0x00))
    term_23 = VColor(rgb=(0x00, 0x5f, 0x5f))
    term_24 = VColor(rgb=(0x00, 0x5f, 0x87))
    term_25 = VColor(rgb=(0x00, 0x5f, 0xaf))
    term_26 = VColor(rgb=(0x00, 0x5f, 0xd7))
    term_27 = VColor(rgb=(0x00, 0x5f, 0xff))
    term_28 = VColor(rgb=(0x00, 0x87, 0x00))
    term_29 = VColor(rgb=(0x00, 0x87, 0x5f))
    term_30 = VColor(rgb=(0x00, 0x87, 0x87))
    term_31 = VColor(rgb=(0x00, 0x87, 0xaf))
    term_32 = VColor(rgb=(0x00, 0x87, 0xd7))
    term_33 = VColor(rgb=(0x00, 0x87, 0xff))
    term_34 = VColor(rgb=(0x00, 0xaf, 0x00))
    term_35 = VColor(rgb=(0x00, 0xaf, 0x5f))
    term_36 = VColor(rgb=(0x00, 0xaf, 0x87))
    term_37 = VColor(rgb=(0x00, 0xaf, 0xaf))
    term_38 = VColor(rgb=(0x00, 0xaf, 0xd7))
    term_39 = VColor(rgb=(0x00, 0xaf, 0xff))
    term_40 = VColor(rgb=(0x00, 0xd7, 0x00))
    term_41 = VColor(rgb=(0x00, 0xd7, 0x5f))
    term_42 = VColor(rgb=(0x00, 0xd7, 0x87))
    term_43 = VColor(rgb=(0x00, 0xd7, 0xaf))
    term_44 = VColor(rgb=(0x00, 0xd7, 0xd7))
    term_45 = VColor(rgb=(0x00, 0xd7, 0xff))
    term_46 = VColor(rgb=(0x00, 0xff, 0x00))
    term_47 = VColor(rgb=(0x00, 0xff, 0x5f))
    term_48 = VColor(rgb=(0x00, 0xff, 0x87))
    term_49 = VColor(rgb=(0x00, 0xff, 0xaf))
    term_50 = VColor(rgb=(0x00, 0xff, 0xd7))
    term_51 = VColor(rgb=(0x00, 0xff, 0xff))
    term_52 = VColor(rgb=(0x5f, 0x00, 0x00))
    term_53 = VColor(rgb=(0x5f, 0x00, 0x5f))
    term_54 = VColor(rgb=(0x5f, 0x00, 0x87))
    term_55 = VColor(rgb=(0x5f, 0x00, 0xaf))
    term_56 = VColor(rgb=(0x5f, 0x00, 0xd7))
    term_57 = VColor(rgb=(0x5f, 0x00, 0xff))
    term_58 = VColor(rgb=(0x5f, 0x5f, 0x00))
    term_59 = VColor(rgb=(0x5f, 0x5f, 0x5f))
    term_60 = VColor(rgb=(0x5f, 0x5f, 0x87))
    term_61 = VColor(rgb=(0x5f, 0x5f, 0xaf))
    term_62 = VColor(rgb=(0x5f, 0x5f, 0xd7))
    term_63 = VColor(rgb=(0x5f, 0x5f, 0xff))
    term_64 = VColor(rgb=(0x5f, 0x87, 0x00))
    term_65 = VColor(rgb=(0x5f, 0x87, 0x5f))
    term_66 = VColor(rgb=(0x5f, 0x87, 0x87))
    term_67 = VColor(rgb=(0x5f, 0x87, 0xaf))
    term_68 = VColor(rgb=(0x5f, 0x87, 0xd7))
    term_69 = VColor(rgb=(0x5f, 0x87, 0xff))
    term_70 = VColor(rgb=(0x5f, 0xaf, 0x00))
    term_71 = VColor(rgb=(0x5f, 0xaf, 0x5f))
    term_72 = VColor(rgb=(0x5f, 0xaf, 0x87))
    term_73 = VColor(rgb=(0x5f, 0xaf, 0xaf))
    term_74 = VColor(rgb=(0x5f, 0xaf, 0xd7))
    term_75 = VColor(rgb=(0x5f, 0xaf, 0xff))
    term_76 = VColor(rgb=(0x5f, 0xd7, 0x00))
    term_77 = VColor(rgb=(0x5f, 0xd7, 0x5f))
    term_78 = VColor(rgb=(0x5f, 0xd7, 0x87))
    term_79 = VColor(rgb=(0x5f, 0xd7, 0xaf))
    term_80 = VColor(rgb=(0x5f, 0xd7, 0xd7))
    term_81 = VColor(rgb=(0x5f, 0xd7, 0xff))
    term_82 = VColor(rgb=(0x5f, 0xff, 0x00))
    term_83 = VColor(rgb=(0x5f, 0xff, 0x5f))
    term_84 = VColor(rgb=(0x5f, 0xff, 0x87))
    term_85 = VColor(rgb=(0x5f, 0xff, 0xaf))
    term_86 = VColor(rgb=(0x5f, 0xff, 0xd7))
    term_87 = VColor(rgb=(0x5f, 0xff, 0xff))
    term_88 = VColor(rgb=(0x87, 0x00, 0x00))
    term_89 = VColor(rgb=(0x87, 0x00, 0x5f))
    term_90 = VColor(rgb=(0x87, 0x00, 0x87))
    term_91 = VColor(rgb=(0x87, 0x00, 0xaf))
    term_92 = VColor(rgb=(0x87, 0x00, 0xd7))
    term_93 = VColor(rgb=(0x87, 0x00, 0xff))
    term_94 = VColor(rgb=(0x87, 0x5f, 0x00))
    term_95 = VColor(rgb=(0x87, 0x5f, 0x5f))
    term_96 = VColor(rgb=(0x87, 0x5f, 0x87))
    term_97 = VColor(rgb=(0x87, 0x5f, 0xaf))
    term_98 = VColor(rgb=(0x87, 0x5f, 0xd7))
    term_99 = VColor(rgb=(0x87, 0x5f, 0xff))
    term_100 = VColor(rgb=(0x87, 0x87, 0x00))
    term_101 = VColor(rgb=(0x87, 0x87, 0x5f))
    term_102 = VColor(rgb=(0x87, 0x87, 0x87))
    term_103 = VColor(rgb=(0x87, 0x87, 0xaf))
    term_104 = VColor(rgb=(0x87, 0x87, 0xd7))
    term_105 = VColor(rgb=(0x87, 0x87, 0xff))
    term_106 = VColor(rgb=(0x87, 0xaf, 0x00))
    term_107 = VColor(rgb=(0x87, 0xaf, 0x5f))
    term_108 = VColor(rgb=(0x87, 0xaf, 0x87))
    term_109 = VColor(rgb=(0x87, 0xaf, 0xaf))
    term_110 = VColor(rgb=(0x87, 0xaf, 0xd7))
    term_111 = VColor(rgb=(0x87, 0xaf, 0xff))
    term_112 = VColor(rgb=(0x87, 0xd7, 0x00))
    term_113 = VColor(rgb=(0x87, 0xd7, 0x5f))
    term_114 = VColor(rgb=(0x87, 0xd7, 0x87))
    term_115 = VColor(rgb=(0x87, 0xd7, 0xaf))
    term_116 = VColor(rgb=(0x87, 0xd7, 0xd7))
    term_117 = VColor(rgb=(0x87, 0xd7, 0xff))
    term_118 = VColor(rgb=(0x87, 0xff, 0x00))
    term_119 = VColor(rgb=(0x87, 0xff, 0x5f))
    term_120 = VColor(rgb=(0x87, 0xff, 0x87))
    term_121 = VColor(rgb=(0x87, 0xff, 0xaf))
    term_122 = VColor(rgb=(0x87, 0xff, 0xd7))
    term_123 = VColor(rgb=(0x87, 0xff, 0xff))
    term_124 = VColor(rgb=(0xaf, 0x00, 0x00))
    term_125 = VColor(rgb=(0xaf, 0x00, 0x5f))
    term_126 = VColor(rgb=(0xaf, 0x00, 0x87))
    term_127 = VColor(rgb=(0xaf, 0x00, 0xaf))
    term_128 = VColor(rgb=(0xaf, 0x00, 0xd7))
    term_129 = VColor(rgb=(0xaf, 0x00, 0xff))
    term_130 = VColor(rgb=(0xaf, 0x5f, 0x00))
    term_131 = VColor(rgb=(0xaf, 0x5f, 0x5f))
    term_132 = VColor(rgb=(0xaf, 0x5f, 0x87))
    term_133 = VColor(rgb=(0xaf, 0x5f, 0xaf))
    term_134 = VColor(rgb=(0xaf, 0x5f, 0xd7))
    term_135 = VColor(rgb=(0xaf, 0x5f, 0xff))
    term_136 = VColor(rgb=(0xaf, 0x87, 0x00))
    term_137 = VColor(rgb=(0xaf, 0x87, 0x5f))
    term_138 = VColor(rgb=(0xaf, 0x87, 0x87))
    term_139 = VColor(rgb=(0xaf, 0x87, 0xaf))
    term_140 = VColor(rgb=(0xaf, 0x87, 0xd7))
    term_141 = VColor(rgb=(0xaf, 0x87, 0xff))
    term_142 = VColor(rgb=(0xaf, 0xaf, 0x00))
    term_143 = VColor(rgb=(0xaf, 0xaf, 0x5f))
    term_144 = VColor(rgb=(0xaf, 0xaf, 0x87))
    term_145 = VColor(rgb=(0xaf, 0xaf, 0xaf))
    term_146 = VColor(rgb=(0xaf, 0xaf, 0xd7))
    term_147 = VColor(rgb=(0xaf, 0xaf, 0xff))
    term_148 = VColor(rgb=(0xaf, 0xd7, 0x00))
    term_149 = VColor(rgb=(0xaf, 0xd7, 0x5f))
    term_150 = VColor(rgb=(0xaf, 0xd7, 0x87))
    term_151 = VColor(rgb=(0xaf, 0xd7, 0xaf))
    term_152 = VColor(rgb=(0xaf, 0xd7, 0xd7))
    term_153 = VColor(rgb=(0xaf, 0xd7, 0xff))
    term_154 = VColor(rgb=(0xaf, 0xff, 0x00))
    term_155 = VColor(rgb=(0xaf, 0xff, 0x5f))
    term_156 = VColor(rgb=(0xaf, 0xff, 0x87))
    term_157 = VColor(rgb=(0xaf, 0xff, 0xaf))
    term_158 = VColor(rgb=(0xaf, 0xff, 0xd7))
    term_159 = VColor(rgb=(0xaf, 0xff, 0xff))
    term_160 = VColor(rgb=(0xd7, 0x00, 0x00))
    term_161 = VColor(rgb=(0xd7, 0x00, 0x5f))
    term_162 = VColor(rgb=(0xd7, 0x00, 0x87))
    term_163 = VColor(rgb=(0xd7, 0x00, 0xaf))
    term_164 = VColor(rgb=(0xd7, 0x00, 0xd7))
    term_165 = VColor(rgb=(0xd7, 0x00, 0xff))
    term_166 = VColor(rgb=(0xd7, 0x5f, 0x00))
    term_167 = VColor(rgb=(0xd7, 0x5f, 0x5f))
    term_168 = VColor(rgb=(0xd7, 0x5f, 0x87))
    term_169 = VColor(rgb=(0xd7, 0x5f, 0xaf))
    term_170 = VColor(rgb=(0xd7, 0x5f, 0xd7))
    term_171 = VColor(rgb=(0xd7, 0x5f, 0xff))
    term_172 = VColor(rgb=(0xd7, 0x87, 0x00))
    term_173 = VColor(rgb=(0xd7, 0x87, 0x5f))
    term_174 = VColor(rgb=(0xd7, 0x87, 0x87))
    term_175 = VColor(rgb=(0xd7, 0x87, 0xaf))
    term_176 = VColor(rgb=(0xd7, 0x87, 0xd7))
    term_177 = VColor(rgb=(0xd7, 0x87, 0xff))
    term_178 = VColor(rgb=(0xd7, 0xaf, 0x00))
    term_179 = VColor(rgb=(0xd7, 0xaf, 0x5f))
    term_180 = VColor(rgb=(0xd7, 0xaf, 0x87))
    term_181 = VColor(rgb=(0xd7, 0xaf, 0xaf))
    term_182 = VColor(rgb=(0xd7, 0xaf, 0xd7))
    term_183 = VColor(rgb=(0xd7, 0xaf, 0xff))
    term_184 = VColor(rgb=(0xd7, 0xd7, 0x00))
    term_185 = VColor(rgb=(0xd7, 0xd7, 0x5f))
    term_186 = VColor(rgb=(0xd7, 0xd7, 0x87))
    term_187 = VColor(rgb=(0xd7, 0xd7, 0xaf))
    term_188 = VColor(rgb=(0xd7, 0xd7, 0xd7))
    term_189 = VColor(rgb=(0xd7, 0xd7, 0xff))
    term_190 = VColor(rgb=(0xd7, 0xff, 0x00))
    term_191 = VColor(rgb=(0xd7, 0xff, 0x5f))
    term_192 = VColor(rgb=(0xd7, 0xff, 0x87))
    term_193 = VColor(rgb=(0xd7, 0xff, 0xaf))
    term_194 = VColor(rgb=(0xd7, 0xff, 0xd7))
    term_195 = VColor(rgb=(0xd7, 0xff, 0xff))
    term_196 = VColor(rgb=(0xff, 0x00, 0x00))
    term_197 = VColor(rgb=(0xff, 0x00, 0x5f))
    term_198 = VColor(rgb=(0xff, 0x00, 0x87))
    term_199 = VColor(rgb=(0xff, 0x00, 0xaf))
    term_200 = VColor(rgb=(0xff, 0x00, 0xd7))
    term_201 = VColor(rgb=(0xff, 0x00, 0xff))
    term_202 = VColor(rgb=(0xff, 0x5f, 0x00))
    term_203 = VColor(rgb=(0xff, 0x5f, 0x5f))
    term_204 = VColor(rgb=(0xff, 0x5f, 0x87))
    term_205 = VColor(rgb=(0xff, 0x5f, 0xaf))
    term_206 = VColor(rgb=(0xff, 0x5f, 0xd7))
    term_207 = VColor(rgb=(0xff, 0x5f, 0xff))
    term_208 = VColor(rgb=(0xff, 0x87, 0x00))
    term_209 = VColor(rgb=(0xff, 0x87, 0x5f))
    term_210 = VColor(rgb=(0xff, 0x87, 0x87))
    term_211 = VColor(rgb=(0xff, 0x87, 0xaf))
    term_212 = VColor(rgb=(0xff, 0x87, 0xd7))
    term_213 = VColor(rgb=(0xff, 0x87, 0xff))
    term_214 = VColor(rgb=(0xff, 0xaf, 0x00))
    term_215 = VColor(rgb=(0xff, 0xaf, 0x5f))
    term_216 = VColor(rgb=(0xff, 0xaf, 0x87))
    term_217 = VColor(rgb=(0xff, 0xaf, 0xaf))
    term_218 = VColor(rgb=(0xff, 0xaf, 0xd7))
    term_219 = VColor(rgb=(0xff, 0xaf, 0xff))
    term_220 = VColor(rgb=(0xff, 0xd7, 0x00))
    term_221 = VColor(rgb=(0xff, 0xd7, 0x5f))
    term_222 = VColor(rgb=(0xff, 0xd7, 0x87))
    term_223 = VColor(rgb=(0xff, 0xd7, 0xaf))
    term_224 = VColor(rgb=(0xff, 0xd7, 0xd7))
    term_225 = VColor(rgb=(0xff, 0xd7, 0xff))
    term_226 = VColor(rgb=(0xff, 0xff, 0x00))
    term_227 = VColor(rgb=(0xff, 0xff, 0x5f))
    term_228 = VColor(rgb=(0xff, 0xff, 0x87))
    term_229 = VColor(rgb=(0xff, 0xff, 0xaf))
    term_230 = VColor(rgb=(0xff, 0xff, 0xd7))
    term_231 = VColor(rgb=(0xff, 0xff, 0xff))
    term_232 = VColor(rgb=(0x08, 0x08, 0x08))
    term_233 = VColor(rgb=(0x12, 0x12, 0x12))
    term_234 = VColor(rgb=(0x1c, 0x1c, 0x1c))
    term_235 = VColor(rgb=(0x26, 0x26, 0x26))
    term_236 = VColor(rgb=(0x30, 0x30, 0x30))
    term_237 = VColor(rgb=(0x3a, 0x3a, 0x3a))
    term_238 = VColor(rgb=(0x44, 0x44, 0x44))
    term_239 = VColor(rgb=(0x4e, 0x4e, 0x4e))
    term_240 = VColor(rgb=(0x58, 0x58, 0x58))
    term_241 = VColor(rgb=(0x60, 0x60, 0x60))
    term_242 = VColor(rgb=(0x66, 0x66, 0x66))
    term_243 = VColor(rgb=(0x76, 0x76, 0x76))
    term_244 = VColor(rgb=(0x80, 0x80, 0x80))
    term_245 = VColor(rgb=(0x8a, 0x8a, 0x8a))
    term_246 = VColor(rgb=(0x94, 0x94, 0x94))
    term_247 = VColor(rgb=(0x9e, 0x9e, 0x9e))
    term_248 = VColor(rgb=(0xa8, 0xa8, 0xa8))
    term_249 = VColor(rgb=(0xb2, 0xb2, 0xb2))
    term_250 = VColor(rgb=(0xbc, 0xbc, 0xbc))
    term_251 = VColor(rgb=(0xc6, 0xc6, 0xc6))
    term_252 = VColor(rgb=(0xd0, 0xd0, 0xd0))
    term_253 = VColor(rgb=(0xda, 0xda, 0xda))
    term_254 = VColor(rgb=(0xe4, 0xe4, 0xe4))
    term_255 = VColor(rgb=(0xee, 0xee, 0xee))

    term_000000 = term_0
    term_800000 = term_1
    term_008000 = term_2
    term_808000 = term_3
    term_000080 = term_4
    term_800080 = term_5
    term_008080 = term_6
    term_c0c0c0 = term_7
    term_808080 = term_8
    term_ff0000 = term_9
    term_00ff00 = term_10
    term_ffff00 = term_11
    term_0000ff = term_12
    term_ff00ff = term_13
    term_00ffff = term_14
    term_ffffff = term_15
    term_000000 = term_16
    term_00005f = term_17
    term_000087 = term_18
    term_0000af = term_19
    term_0000d7 = term_20
    term_0000ff = term_21
    term_005f00 = term_22
    term_005f5f = term_23
    term_005f87 = term_24
    term_005faf = term_25
    term_005fd7 = term_26
    term_005fff = term_27
    term_008700 = term_28
    term_00875f = term_29
    term_008787 = term_30
    term_0087af = term_31
    term_0087d7 = term_32
    term_0087ff = term_33
    term_00af00 = term_34
    term_00af5f = term_35
    term_00af87 = term_36
    term_00afaf = term_37
    term_00afd7 = term_38
    term_00afff = term_39
    term_00d700 = term_40
    term_00d75f = term_41
    term_00d787 = term_42
    term_00d7af = term_43
    term_00d7d7 = term_44
    term_00d7ff = term_45
    term_00ff00 = term_46
    term_00ff5f = term_47
    term_00ff87 = term_48
    term_00ffaf = term_49
    term_00ffd7 = term_50
    term_00ffff = term_51
    term_5f0000 = term_52
    term_5f005f = term_53
    term_5f0087 = term_54
    term_5f00af = term_55
    term_5f00d7 = term_56
    term_5f00ff = term_57
    term_5f5f00 = term_58
    term_5f5f5f = term_59
    term_5f5f87 = term_60
    term_5f5faf = term_61
    term_5f5fd7 = term_62
    term_5f5fff = term_63
    term_5f8700 = term_64
    term_5f875f = term_65
    term_5f8787 = term_66
    term_5f87af = term_67
    term_5f87d7 = term_68
    term_5f87ff = term_69
    term_5faf00 = term_70
    term_5faf5f = term_71
    term_5faf87 = term_72
    term_5fafaf = term_73
    term_5fafd7 = term_74
    term_5fafff = term_75
    term_5fd700 = term_76
    term_5fd75f = term_77
    term_5fd787 = term_78
    term_5fd7af = term_79
    term_5fd7d7 = term_80
    term_5fd7ff = term_81
    term_5fff00 = term_82
    term_5fff5f = term_83
    term_5fff87 = term_84
    term_5fffaf = term_85
    term_5fffd7 = term_86
    term_5fffff = term_87
    term_870000 = term_88
    term_87005f = term_89
    term_870087 = term_90
    term_8700af = term_91
    term_8700d7 = term_92
    term_8700ff = term_93
    term_875f00 = term_94
    term_875f5f = term_95
    term_875f87 = term_96
    term_875faf = term_97
    term_875fd7 = term_98
    term_875fff = term_99
    term_878700 = term_100
    term_87875f = term_101
    term_878787 = term_102
    term_8787af = term_103
    term_8787d7 = term_104
    term_8787ff = term_105
    term_87af00 = term_106
    term_87af5f = term_107
    term_87af87 = term_108
    term_87afaf = term_109
    term_87afd7 = term_110
    term_87afff = term_111
    term_87d700 = term_112
    term_87d75f = term_113
    term_87d787 = term_114
    term_87d7af = term_115
    term_87d7d7 = term_116
    term_87d7ff = term_117
    term_87ff00 = term_118
    term_87ff5f = term_119
    term_87ff87 = term_120
    term_87ffaf = term_121
    term_87ffd7 = term_122
    term_87ffff = term_123
    term_af0000 = term_124
    term_af005f = term_125
    term_af0087 = term_126
    term_af00af = term_127
    term_af00d7 = term_128
    term_af00ff = term_129
    term_af5f00 = term_130
    term_af5f5f = term_131
    term_af5f87 = term_132
    term_af5faf = term_133
    term_af5fd7 = term_134
    term_af5fff = term_135
    term_af8700 = term_136
    term_af875f = term_137
    term_af8787 = term_138
    term_af87af = term_139
    term_af87d7 = term_140
    term_af87ff = term_141
    term_afaf00 = term_142
    term_afaf5f = term_143
    term_afaf87 = term_144
    term_afafaf = term_145
    term_afafd7 = term_146
    term_afafff = term_147
    term_afd700 = term_148
    term_afd75f = term_149
    term_afd787 = term_150
    term_afd7af = term_151
    term_afd7d7 = term_152
    term_afd7ff = term_153
    term_afff00 = term_154
    term_afff5f = term_155
    term_afff87 = term_156
    term_afffaf = term_157
    term_afffd7 = term_158
    term_afffff = term_159
    term_d70000 = term_160
    term_d7005f = term_161
    term_d70087 = term_162
    term_d700af = term_163
    term_d700d7 = term_164
    term_d700ff = term_165
    term_d75f00 = term_166
    term_d75f5f = term_167
    term_d75f87 = term_168
    term_d75faf = term_169
    term_d75fd7 = term_170
    term_d75fff = term_171
    term_d78700 = term_172
    term_d7875f = term_173
    term_d78787 = term_174
    term_d787af = term_175
    term_d787d7 = term_176
    term_d787ff = term_177
    term_d7af00 = term_178
    term_d7af5f = term_179
    term_d7af87 = term_180
    term_d7afaf = term_181
    term_d7afd7 = term_182
    term_d7afff = term_183
    term_d7d700 = term_184
    term_d7d75f = term_185
    term_d7d787 = term_186
    term_d7d7af = term_187
    term_d7d7d7 = term_188
    term_d7d7ff = term_189
    term_d7ff00 = term_190
    term_d7ff5f = term_191
    term_d7ff87 = term_192
    term_d7ffaf = term_193
    term_d7ffd7 = term_194
    term_d7ffff = term_195
    term_ff0000 = term_196
    term_ff005f = term_197
    term_ff0087 = term_198
    term_ff00af = term_199
    term_ff00d7 = term_200
    term_ff00ff = term_201
    term_ff5f00 = term_202
    term_ff5f5f = term_203
    term_ff5f87 = term_204
    term_ff5faf = term_205
    term_ff5fd7 = term_206
    term_ff5fff = term_207
    term_ff8700 = term_208
    term_ff875f = term_209
    term_ff8787 = term_210
    term_ff87af = term_211
    term_ff87d7 = term_212
    term_ff87ff = term_213
    term_ffaf00 = term_214
    term_ffaf5f = term_215
    term_ffaf87 = term_216
    term_ffafaf = term_217
    term_ffafd7 = term_218
    term_ffafff = term_219
    term_ffd700 = term_220
    term_ffd75f = term_221
    term_ffd787 = term_222
    term_ffd7af = term_223
    term_ffd7d7 = term_224
    term_ffd7ff = term_225
    term_ffff00 = term_226
    term_ffff5f = term_227
    term_ffff87 = term_228
    term_ffffaf = term_229
    term_ffffd7 = term_230
    term_ffffff = term_231
    term_080808 = term_232
    term_121212 = term_233
    term_1c1c1c = term_234
    term_262626 = term_235
    term_303030 = term_236
    term_3a3a3a = term_237
    term_444444 = term_238
    term_4e4e4e = term_239
    term_585858 = term_240
    term_606060 = term_241
    term_666666 = term_242
    term_767676 = term_243
    term_808080 = term_244
    term_8a8a8a = term_245
    term_949494 = term_246
    term_9e9e9e = term_247
    term_a8a8a8 = term_248
    term_b2b2b2 = term_249
    term_bcbcbc = term_250
    term_c6c6c6 = term_251
    term_d0d0d0 = term_252
    term_dadada = term_253
    term_e4e4e4 = term_254
    term_eeeeee = term_255

    transparent = None

    black = term_0
    red = term_1
    green = term_2
    brown = term_3
    blue = term_4
    magenta = term_5
    cyan = term_6
    white = term_7
    grey = term_8
    lightred = term_9
    lightgreen = term_10
    yellow = term_11
    lightblue = term_12
    lightmagenta = term_13
    lightcyan = term_14
    white = term_15

    pink = term_ff8787
    darkred = term_5f0000
    darkgreen = term_005f00
    darkblue = term_00005f
    darkmagenta = term_5f005f
    darkcyan = term_005f5f

    @staticmethod
    def name_to_color(name):
        """Perform lookup of the color by string. Returns None if the
        lookup fails."""
        return VGlobalColor.__dict__.get(name)
