
class Model:

    def __init__(self, text, trigram_model, keras_model, chars, char_indices, indices_char):
        self.text = text
        self.trigram_model = trigram_model
        self.keras_model = keras_model
        self.chars = chars
        self.char_indices = char_indices
        self.indices_char = indices_char
