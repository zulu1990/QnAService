import time

from azure.cognitiveservices.knowledge.qnamaker.authoring import QnAMakerClient
from msrest.authentication import CognitiveServicesCredentials

from config.config import QnaMakerConfig


def init_client(config: QnaMakerConfig):
    return QnAMakerClient(endpoint=config.AUTHORING_ENDPOINT, credentials=CognitiveServicesCredentials(config.SUBSCRIPTION_KEY))


class QnaMakerService:
    def __init__(self):
        self.client = init_client(QnaMakerConfig)
        print("init client")

    def download_kb(self, kb_id):
        print("Downloading knowledge base...")
        kb_data = self.client.knowledgebase.download(kb_id=kb_id, environment="Test")
        print("Downloaded knowledge base. It has {} QnAs.".format(len(kb_data.qna_documents)))
        return kb_data

    def update_knowledge_base(self, kb_id, update_kb_operation_dto):
        try:
            print("Update")
            return self.client.knowledgebase.update(kb_id=kb_id, update_kb=update_kb_operation_dto)
        except BaseException as bs:
            print(bs)
            raise bs



