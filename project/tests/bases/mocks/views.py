class UserMock:
    username = 'mock'
    email = 'mock@mock.mock'


class RequestMock:
    session = {}
    POST = {}
    GET = {}
    path = '/'
    user = UserMock()

    def is_secure(self): return False

    def get_host(self): return 'testserver'


class SelfViewMock:
    request = RequestMock()
