class KeyEvent(Event):
    key_code = Int()

    def __init__(self, key_code):
        super().__init__(EventType.KeyPress)
        self.key_code = key_code

    @property
    def key(self):
        return self.key_code & Key.Mask

    @property
    def modifiers(self):
        return self.key_code & KeyModifier.Mask

    @property
    def text(self):
        return vai_key_code_to_text(self.key_code)

    @classmethod
    def from_native_key_code(cls, native_key_code):
        key_code = native_to_vai_key_code(native_key_code)
        if key_code is None:
            raise ValueError(f"Unknown native key code {native_key_code}")
        return cls(key_code)


