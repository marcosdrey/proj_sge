from django.db import models


class AIResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.result if len(self.result) <= 10 else self.result[:10] + "..."
