class CloudLocalPair:
    def __init__(self, cloud_model, local_model):
        self.CloudModel = cloud_model
        self.LocalModel = local_model

    def changes_made(self):
        cm = self.CloudModel
        lm = self.LocalModel
        if cm.answer != lm['answer'] or cm.questions != lm['qna_maker']:
            return True

        return False
