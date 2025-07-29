from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from scriptapi.models import Transcript, ParsedFile, Keyword
from .serializers.transcript_serializer import (
    TranscriptSerializer,
    ParsedFileSerializer,
)
from collections import Counter


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_transcript(request):
    serializer = TranscriptSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_transcripts(request):
    transcripts = Transcript.objects.filter(user=request.user)
    serializer = TranscriptSerializer(transcripts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_parsed_file(request):
    transcript_id = request.data.get("transcript_id")
    keyword = request.data.get("keyword")
    context = int(request.data.get("context", 0))

    try:
        transcript = Transcript.objects.get(id=transcript_id, user=request.user)
    except Transcript.DoesNotExist:
        return Response({"error": "Transcript not found"}, status=404)

    lines = transcript.content.split("\n")
    results = []

    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            start = max(i - context, 0)
            end = min(i + context + 1, len(lines))
            results.extend(lines[start:end])
            results.append("-" * 50)

    extracted_text = "\n".join(results)

    parsed = ParsedFile.objects.create(
        user=request.user,
        transcript=transcript,
        keyword=keyword,
        context_lines=context,
        extracted_text=extracted_text,
    )
    serializer = ParsedFileSerializer(parsed)
    return Response(serializer.data, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_files(request):
    files = ParsedFile.objects.filter(user=request.user)
    serializer = ParsedFileSerializer(files, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.user
    return Response(
        {"message": f"Welcome, {user.first_name}! This is a protected endpoint."}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_parsed_file(request):
    serializer = ParsedFileSerializer(data=request.data)
    if serializer.is_valid():
        parsed_file = serializer.save(user=request.user)

        keyword_text = request.data.get("keyword", "").strip()
        if keyword_text:
            keyword_obj, _ = Keyword.objects.get_or_create(name=keyword_text)
            parsed_file.keywords.add(keyword_obj)

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_parsed_file(request, pk):
    try:
        parsed = ParsedFile.objects.get(pk=pk, user=request.user)
        serializer = ParsedFileSerializer(parsed)
        return Response(serializer.data)
    except ParsedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def save_parsed_file(request):
#     serializer = ParsedFileSerializer(data=request.data)
#     if serializer.is_valid():
#         parsed_file = serializer.save(user=request.user)

#         keyword_text = request.data.get("keyword", "").strip()
#         if keyword_text:
#             keyword, _ = Keyword.objects.get_or_create(name=keyword_text)
#             keyword.files.add(parsed_file)

#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_transcript(request, pk):
    try:
        transcript = Transcript.objects.get(pk=pk, user=request.user)
        transcript.delete()
        return Response(status=204)
    except Transcript.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_parsed_file(request, pk):
    try:
        file = ParsedFile.objects.get(pk=pk, user=request.user)
        file.delete()
        return Response(status=204)
    except ParsedFile.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def rename_transcript(request, pk):
    try:
        transcript = Transcript.objects.get(id=pk, user=request.user)
    except Transcript.DoesNotExist:
        return Response({"error": "Transcript not found"}, status=404)

    new_title = request.data.get("title")
    if not new_title:
        return Response({"error": "Title required"}, status=400)

    transcript.title = new_title
    transcript.save()
    return Response({"message": "Title updated", "title": new_title})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_keyword_stats(request):
    files = ParsedFile.objects.filter(user=request.user)
    keywords = [pf.keyword.lower() for pf in files]
    keyword_counts = Counter(keywords)
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: -x[1])
    return Response({"keywords": sorted_keywords})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def rename_parsed_file(request, file_id):
    try:
        parsed_file = ParsedFile.objects.get(id=file_id, user=request.user)
        parsed_file.transcript.title = request.data.get(
            "title", parsed_file.transcript.title
        )
        parsed_file.transcript.save()
        return Response({"message": "Renamed successfully"})
    except ParsedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_files_by_keyword(request, keyword):
    try:
        keyword_obj = Keyword.objects.get(name__iexact=keyword)
        files = keyword_obj.parsed_files.filter(user=request.user)
        serializer = ParsedFileSerializer(files, many=True)
        return Response(serializer.data)
    except Keyword.DoesNotExist:
        return Response([], status=200)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def save_parsed_file(request):
#     try:
#         transcript_id = request.data.get("transcript_id")
#         keyword = request.data.get("keyword")
#         context = int(request.data.get("context_lines", 0))
#         extracted_text = request.data.get("extracted_text")

#         transcript = Transcript.objects.get(id=transcript_id, user=request.user)

#         parsed = ParsedFile.objects.create(
#             user=request.user,
#             transcript=transcript,
#             keyword=keyword,
#             context_lines=context,
#             extracted_text=extracted_text,
#         )

#         serializer = ParsedFileSerializer(parsed)
#         return Response(serializer.data, status=201)

#     except Transcript.DoesNotExist:
#         return Response({"error": "Transcript not found."}, status=404)
#     except Exception as e:
#         return Response({"error": str(e)}, status=400)
