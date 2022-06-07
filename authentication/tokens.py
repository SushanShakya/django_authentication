from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def create_hash(self, user):
        return (
            text_type(user.pk)
        )
    
    def check(self, user, token):
        hash = self.create_hash(user)
        return hash == token

token_generator = TokenGenerator()