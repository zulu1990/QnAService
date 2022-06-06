import itertools
import os
import time
from operator import itemgetter

from azure.cognitiveservices.knowledge.qnamaker.authoring.models import OperationStateType
from azure.cognitiveservices.knowledge.qnamaker.runtime.models import QnADTO

from config.config import QnaMakerConfig
from exporters.qna_maker_exporter import format_data as format_data_qna
from exporters.luis_exporter import format_data as format_data_luis
from exporters.botium_luis_exporter import format_data as format_data_luis_botium
from exporters.botium_qna_exporter import format_single_data as format_single_data_qna_botium
from exporters.botium_qna_exporter import format_template as format_botium_qna_template
from data_parser import parse_excel_training
from services.QnaMakerService import QnaMakerService
from services.qna_data_generator import my_function


def group_data(data):
    grouped = dict()
    for key, values in itertools.groupby(data, key=itemgetter('type')):
        if key not in grouped: grouped[key] = list()
        for value in values:
            grouped[key].append(value)
    
    return grouped

def write_file(data, subpath, name, format):
    filename ="../output/{subpath}/{name}.{format}".format(name=name, subpath=subpath, format=format) 
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    f = open(filename, "w", encoding="utf-8")
    f.write(data)
    f.close()


def parsing_and_stuff(grouped_data):
    for key in grouped_data.keys():
        qna_data = format_data_qna(grouped_data[key])
        write_file(qna_data, 'qnamaker-training', key, 'qna')

        luis_data = format_data_luis(grouped_data[key])
        write_file(luis_data, 'luis-training', key, 'lu')

        luis_data = format_data_luis_botium(grouped_data[key], 'luis')
        write_file(luis_data, 'luis-at', key, 'training.utterances.txt')

        luis_data = format_data_luis_botium(grouped_data[key], 'verification')
        write_file(luis_data, 'luis-at', key, 'verification.utterances.txt')

        for data in grouped_data[key]:
            botium_qna_data = format_single_data_qna_botium(data, 'luis')
            write_file(botium_qna_data, 'kb-at/{scope}/training/utterances'.format(scope=key), data['name'],
                       'training.utterances.txt')
            botium_convo_data = format_botium_qna_template(data, 'luis')
            write_file(botium_convo_data, 'kb-at/{scope}/training'.format(scope=key), data['name'],
                       'training.convo.txt')

            botium_qna_data = format_single_data_qna_botium(data, 'verification')
            write_file(botium_qna_data, 'kb-at/{scope}/verification/utterances'.format(scope=key), data['name'],
                       'verification.utterances.txt')
            botium_convo_data = format_botium_qna_template(data, 'verification')
            write_file(botium_convo_data, 'kb-at/{scope}/verification'.format(scope=key), data['name'],
                       'verification.convo.txt')



    print("Finish")


def _monitor_operation(self, operation):
    for i in range(100):
        if operation.operation_state in [OperationStateType.not_started, OperationStateType.running]:
            print(f"{i} -> Waiting for operation: {operation.operation_id} to complete. status: {operation.operation_state}")
            time.sleep(5)
            operation = self.operations.get_details(operation_id=operation.operation_id)
        else:
            break
    if operation.operation_state != OperationStateType.succeeded:
        raise Exception(f"Operation {operation.operation_id} failed to complete. status {operation.operation_state}")

    return operation


if __name__ == '__main__':
    print("Start")
    qna_service = QnaMakerService()
    qna_maker_data = qna_service.download_kb(QnaMakerConfig.CONCUR_ID)

    path: str = '../data/training-data.xlsx'
    sheet_name: str = "QnA"
    all_data = parse_excel_training(path, sheet_name=sheet_name)

    data_grouped = group_data(all_data)['concur']

    update_data = my_function(data_grouped, qna_maker_data)

    operation = qna_service.update_knowledge_base(QnaMakerConfig.CONCUR_ID, update_data)
    _monitor_operation(qna_service.client, operation)
