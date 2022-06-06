ANSWER_TEMPLATE: str = '''```markdown
{}    
```'''

QNA_ENTRY_TEMPLATE: str = '''
> !# @qna.pair.source = Editorial

<a id = "{id}"></a>

{questions}

{meta}

{answer}

'''

META_TEMPLATE: str = '**Filters:**\n'

def format_questions_to_string(questions):
    first_question = '## ? {}\n'.format(questions[0])
    other_questions = questions[1:]

    other_questions_formatted = ['- {}\n'.format(question) for question in other_questions]    

    return first_question + ''.join(other_questions_formatted)

def format_answer_to_string(answer):
    return ANSWER_TEMPLATE.format(answer)

def format_qna_entry(id, questions, answer, meta):
    return QNA_ENTRY_TEMPLATE.format(id=id, questions=questions, answer=answer, meta=meta)

def format_meta(meta: dict):
    return META_TEMPLATE + ''.join(['- {key} = {value}\n'.format(key=key, value=meta[key]) for key in meta.keys()])

def format_data(training_entries):
    template = '> # QnA pairs\n\n'
    for index, entry in enumerate(training_entries, start = 1):
        questions = format_questions_to_string(entry['qna_maker'])
        answer = format_answer_to_string(entry['answer'])
        meta = format_meta(entry['meta'])
        template = template + format_qna_entry(id=index, questions=questions, answer=answer, meta=meta)

    return template