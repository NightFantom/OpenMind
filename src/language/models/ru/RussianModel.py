from pycorenlp import StanfordCoreNLP
from configs.config_constants import CoreNLPServerAddress
from language.models.named_entity_recognition import NERType
from language.models.part_of_speech import POS
from language.models.token import Token
from language.models.language_model import LanguageModel
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class RussianLanguageModel(LanguageModel):
    __name = "Russian"
    __code = "ru"

    def __init__(self):
        self.pos_map = {"VERB": POS.VERB,
                        "INFN": POS.VERB,
                        "NOUN": POS.NOUN,
                        "NPRO": POS.NOUN,
                        "ADJF": POS.ADJ,
                        "ADJS": POS.ADJ,
                        "NUMR": POS.CARDINAL_NUMBER,
                        "PRTF": POS.PARTICLE,
                        "PRTS": POS.PARTICLE,
                        }

        self.pymorph_to_w2v_map = {"VERB": "VERB",
                                   "INFN": "VERB",
                                   "ADJF": "ADJ",
                                   "ADJS": "ADJ",
                                   "NOUN": "NOUN",
                                   "ADVB": "ADV",
                                   "NUMR": "NUM",
                                   "PRTF": "PART",
                                   "PRTS": "PART",
                                   "NPRO": "NOUN"
                                   }

    def get_language_name(self):
        return RussianLanguageModel.__name

    @property
    def language_code(self):
        return RussianLanguageModel.__code

    def convert_pos(self, pos_str):
        return self.pos_map.get(pos_str, POS.UNKOWN)

    def pos_from_pymorph_to_w2v(self, str):
        return self.pymorph_to_w2v_map.get(str, "unkown")

    def convert_ner(self, ner):
        raise NotImplementedError()

    def tokenize(self, string):
        splited = string.split(' ')
        result = []
        for word in splited:
            description = morph.parse(word)[0]
            lemma = description.normal_form
            pos_tag = self.convert_pos(description.tag.POS)
            if description.tag.POS != None:
                lemma += '_' + self.pos_from_pymorph_to_w2v(description.tag.POS)
            token = Token(word, lemma, pos_tag)
            result.append(token)
        return result