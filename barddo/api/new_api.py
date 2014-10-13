from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, IntegerField
from rest_framework.pagination import PaginationSerializer
import dateutil.parser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import RemotePage, Collection, Work


class MangaSerializer(ModelSerializer):
    """
    Knows how to serialize as JSON a manga item with it's chapters
    """
    id = IntegerField(source="id", read_only=True)
    name = CharField(source="name", read_only=True)
    summary = CharField(source="summary", read_only=True)
    author = CharField(source="author.get_full_name", read_only=True)
    chapters = SerializerMethodField('get_chapters')

    def get_chapters(self, collection):
        """
        Helper method to render all manga chapters as a list
        """
        return [{'id': w.id, 'pos': w.unit_count} for w in collection.works.all()]

    class Meta:
        model = Collection
        fields = ('id', 'name', 'author', 'cover_url', 'chapters', 'summary')


class PaginatedMangaSerializer(PaginationSerializer):
    """
    Handle pagination logic on serialization process
    """

    class Meta:
        object_serializer_class = MangaSerializer


class MangaListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Expose manga list with timestamp and pagination parameters
    """
    model = Collection
    serializer_class = MangaSerializer
    permission_classes = [AllowAny]

    default_timestamp = "2014-01-01 00:00:00.876305+00:00"
    page_size = 100

    def list(self, request, *args, **kwargs):
        last_date_string = request.GET.get("last", self.default_timestamp)
        last_date = dateutil.parser.parse(last_date_string)

        queryset = Collection.objects.select_related("author").prefetch_related('works').filter(
            last_updated__gte=last_date).order_by('name')
        paginator = Paginator(queryset, self.page_size)

        page = request.QUERY_PARAMS.get('page')
        try:
            mangas = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            mangas = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            mangas = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedMangaSerializer(mangas, context=serializer_context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


class ChapterSerializer(ModelSerializer):
    """
    Knows how to serialize as JSON a manga item with it's chapters
    """
    id = IntegerField(source="id", read_only=True)
    manga_id = CharField(source="collection.id", read_only=True)
    pos = IntegerField(source="unit_count", read_only=True)

    class Meta:
        model = Work
        fields = ("id", "manga_id", "pos")


class PaginatedChapterSerializer(PaginationSerializer):
    """
    Handle pagination logic on serialization process
    """

    class Meta:
        object_serializer_class = ChapterSerializer


class ChapterListViewSet(viewsets.ReadOnlyModelViewSet):
    model = Work
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]

    default_timestamp = "2014-01-01 00:00:00.876305+00:00"
    page_size = 100

    def list(self, request, *args, **kwargs):
        last_date_string = request.GET.get("last", self.default_timestamp)
        last_date = dateutil.parser.parse(last_date_string)

        queryset = Work.objects.filter(
            publish_date__gte=last_date).order_by('collection')
        paginator = Paginator(queryset, self.page_size)

        page = request.QUERY_PARAMS.get('page')
        try:
            chapters = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            chapters = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            chapters = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedChapterSerializer(chapters, context=serializer_context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)


class RemotePageSerializer(ModelSerializer):
    """
    Knows how to serialize do JSON a RemotePage object
    """

    def to_native(self, obj):
        return obj.url

    class Meta:
        model = RemotePage


class RemotePagesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all pages for given chapter
    """
    model = RemotePage
    serializer_class = RemotePageSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """
        List every favorite work
        """
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Disable single item retrieve
        """
        queryset = RemotePage.objects.filter(work_id=pk).order_by("sequence")
        serializer = RemotePageSerializer(queryset, many=True)
        return Response(serializer.data)