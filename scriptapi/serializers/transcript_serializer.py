from rest_framework import serializers
from scriptapi.models import Transcript, ParsedFile, Keyword


class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ["id", "title", "content", "created_at"]
        # fields = ["id", "title", "content", "uploaded_at"]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "name"]


class ParsedFileSerializer(serializers.ModelSerializer):
    transcript_id = serializers.PrimaryKeyRelatedField(
        queryset=Transcript.objects.all(), source="transcript"
    )
    transcript_title = serializers.CharField(source="transcript.title", read_only=True)

    class Meta:
        model = ParsedFile
        fields = [
            "id",
            "transcript_id",
            "transcript_title",
            "keyword",
            "context_lines",
            "extracted_text",
            "created_at",
        ]


# class ParsedFileSerializer(serializers.ModelSerializer):
#     transcript_id = serializers.PrimaryKeyRelatedField(
#         queryset=Transcript.objects.all(), source="transcript"
#     )
#     transcript_title = serializers.CharField(source="transcript.title", read_only=True)

#     class Meta:
#         model = ParsedFile
#         fields = [
#             "id",
#             "transcript_id",
#             "transcript_title",
#             "keyword",
#             "context_lines",
#             "extracted_text",
#         ]
