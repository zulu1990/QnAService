import re

entity_regex = re.compile("\{[^=]*?=(.*?)\}")
def clean_entity_definition(utterance):
    return re.sub(entity_regex, r"\1", utterance)
    