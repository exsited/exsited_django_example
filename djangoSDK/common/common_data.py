from exsited.exsited.auth.dto.token_dto import RequestTokenDTO

class CommonData:

    @staticmethod
    def get_request_token_dto():
        return RequestTokenDTO(
            grantType="[GRANT_TYPE]",
            clientId = 	"[YOUR_CLIENT_ID]",
            clientSecret = "[YOUR_CLIENT_SECRET]",
            redirectUri = "[YOUR_REDIRECT_URI]",
            exsitedUrl = "[YOUR_EXSITED_SERVER_URL]"
        )