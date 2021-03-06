from waterbutler.core import metadata


class BaseDataverseMetadata(metadata.BaseMetadata):

    @property
    def provider(self):
        return 'dataverse'


class DataverseFileMetadata(BaseDataverseMetadata, metadata.BaseFileMetadata):

    def __init__(self, raw, dataset_version):
        super().__init__(raw)
        self.dataset_version = dataset_version

    @property
    def file_id(self):
        return str(self.raw['id'])

    @property
    def name(self):
        return self.raw['name']

    @property
    def path(self):
        return self.build_path(self.file_id)

    @property
    def size(self):
        return None

    @property
    def content_type(self):
        return self.raw['contentType']

    @property
    def modified(self):
        return None

    @property
    def can_delete(self):
        """Files can be deleted if they are part of the draft dataset"""
        return self.dataset_version == 'latest' or self.dataset_version == 'draft'

    @property
    def extra(self):
        return {
            'fileId': self.file_id,
            'canDelete': self.can_delete,
        }


class DataverseDatasetMetadata(BaseDataverseMetadata, metadata.BaseFolderMetadata):

    def __init__(self, raw, name, doi, version):
        super().__init__(raw)
        self._name = name
        self.doi = doi

        files = self.raw['files']
        self._entries = [DataverseFileMetadata(f['datafile'], version) for f in files]

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self.build_path(self.doi)

    @property
    def entries(self):
        return self._entries

    def serialized(self):
        if self._entries:
            return [e.serialized() for e in self._entries]
        return super(DataverseDatasetMetadata, self).serialized()
