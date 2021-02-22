import yauploader


class TestAccounting:

    def setup_class(self):
        self.uploader = yauploader.YaUploader(yauploader.get_token(yauploader.TOKEN_PATH))

    def setup(self):
        self.folder_name = 'new folder'
        self.result = 201

    def test_add_create_folder_passes(self):
        assert self.uploader.create_folder(self.folder_name) == self.result

    def test_get_resource_info(self):
        assert self.folder_name == self.uploader.get_resource_info(self.folder_name)['name']
