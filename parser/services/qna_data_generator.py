from azure.cognitiveservices.knowledge.qnamaker.authoring.models import UpdateKbOperationDTO, UpdateKbOperationDTOAdd, \
    UpdateKbOperationDTODelete, QnADTO, MetadataDTO

from models.cloud_local_pair import CloudLocalPair


def my_function(local_kb_data, service_data: [QnADTO]):
    cloud_data = service_data.qna_documents
    new_qna_pairs = []
    updated_qna_pairs = []
    for local_data in local_kb_data:
        id = local_data['meta']['id']
        from_cloud = [x for x in cloud_data if x.metadata[1].value == id]
        if len(from_cloud) == 0:
            new_qna_pairs.append(local_data)
        else:
            cloud_local_pair = CloudLocalPair(cloud_model=from_cloud[0], local_model=local_data)
            if cloud_local_pair.changes_made():
                updated_qna_pairs.append(cloud_local_pair)

    updated = qna_pair_updated(updated_qna_pairs, new_qna_pairs)
    return updated


def new_qna_pair_added(new_data):
    if len(new_data) == 0:
        return []

    new_qna_list = []

    for data in new_data:
        qna_metadata = []

        for key, value in data['meta'].items():
            qna_metadata.append(MetadataDTO(name=key, value=value))

        new_qna_list.append(QnADTO(
            answer=data['answer'],
            questions=data['qna_maker'],
            metadata=qna_metadata
        ))

    return new_qna_list


def generate_qna_update_model(updated: [QnADTO], ids: [int]):
    update_kb_operation_dto = UpdateKbOperationDTO(
        add=UpdateKbOperationDTOAdd(
            qna_list=updated
        ),
        delete=UpdateKbOperationDTODelete(ids=ids),
        update=None
    )
    return update_kb_operation_dto


def qna_pair_updated(updated_data: [CloudLocalPair], new_qna_pairs: []):
    ids = [x.CloudModel.id for x in updated_data]
    local_data = [l.LocalModel for l in updated_data]

    new_qna = new_qna_pair_added(new_qna_pairs)
    updated = new_qna_pair_added(local_data)
    updated.extend(new_qna)

    return generate_qna_update_model(updated, ids)

