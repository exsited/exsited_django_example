from exsited.exsited.exsited_sdk import ExsitedSDK
from common.common_data import CommonData


class ExsitedService:
    def __init__(self):
        self.sdk = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    def get_sdk(self):
        return ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
