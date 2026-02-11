from django.db.models import TextChoices


class ChannelTypeChoices(TextChoices):
    FI = 'Físico', 'Físico'
    Di = 'Digital', 'Digital'