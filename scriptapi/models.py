from django.db import models
from django.contrib.auth.models import User


class Transcript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transcripts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name if isinstance(self.name, str) else str(self.name)


class ParsedFile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="parsed_files"
    )
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    context_lines = models.PositiveIntegerField(default=0)
    extracted_text = models.TextField()
    keywords = models.ManyToManyField("Keyword", related_name="parsed_files")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ParsedFile: {self.transcript.title} by {self.user.username}"


# class KeywordStat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     keyword = models.CharField(max_length=100)
#     usage_count = models.PositiveIntegerField(default=1)

#     class Meta:
#         unique_together = ("user", "keyword")

# from django.db import models
# from django.contrib.auth.models import User


# class Transcript(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transcripts")
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class ParsedFile(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="parsed_files"
#     )
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     format = models.CharField(max_length=10, default="txt")
#     created_at = models.DateTimeField(auto_now_add=True)
