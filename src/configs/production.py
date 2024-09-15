from .base import Config


class ProductionConfig(Config):

    # @property
    # def SESSION_COOKIE_SECURE(self):
    #     return True
    def __init__(self):
        super().__init__()
        self.SESSION_COOKIE_SECURE = True
        self.JWT_COOKIE_CSRF_PROTECT=True
        self.JWT_COOKIE_SECURE=True

