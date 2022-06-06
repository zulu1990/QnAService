def format_data(training_entries):
    template = ''
    for item in training_entries:
        template = template + ''.join(['- {}\n'.format(value) for value in item['luis'] ])
    return template
