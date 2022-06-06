from parser_lib.utterances_cleanup import clean_entity_definition

BOTIUM_KB_TEST_TEMPLATE: str = '''
{name}-{group}

#include PCONVO_GREETING_FIRST_TIME
#include PCONVO_SET_COUNTRY_{country}

#me
{name}-{group}-UTT

#bot
{answer}

PAUSE 2000
'''

def format_template(training_entry, group = 'luis'):
    country = training_entry['meta']['country']
    if not country.strip():
        country = 'other'
    return BOTIUM_KB_TEST_TEMPLATE.format(
        name=training_entry['name'].upper(), 
        group=group.upper(), 
        answer=training_entry['answer'],
        country=training_entry['meta']['country'].upper()
    )

def format_single_data(training_entry, group = 'luis'):
    template = '{name}-{group}-UTT\n'.format(name=training_entry['name'].upper(), group=group.upper())
    for line in training_entry[group]:
        if line.strip():
            template = template + '{}\n'.format(clean_entity_definition(line))
    return template
