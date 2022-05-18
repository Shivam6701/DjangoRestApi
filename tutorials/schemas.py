from typing import Optional
from django.db import models


class Token(models.Model):
    access_token: str
    token_type: str

class TokenData(models.Model):
    id: Optional[str]= None