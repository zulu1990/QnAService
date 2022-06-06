from parser_lib.utterances_cleanup import clean_entity_definition

def format_data(training_entries, key = 'luis'):
    template = '{name}-{key}-UTT\n'.format(name=training_entries[0]['type'].upper(), key=key.upper())
    for item in training_entries:
        for line in item[key]:
            if line.strip():
                template = template + '{}\n'.format(clean_entity_definition(line))
    return template
