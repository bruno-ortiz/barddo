from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, IntegerField
from rest_framework.pagination import PaginationSerializer
import dateutil.parser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import RemotePage, Collection, CollectionAvailability, CollectionSource


class MangaSerializer(ModelSerializer):
    """
    Knows how to serialize as JSON a manga item with it's chapters
    """
    id = IntegerField(source="id", read_only=True)
    name = CharField(source="name", read_only=True)
    summary = CharField(source="summary", read_only=True)
    source_id = CharField(source="source_id", read_only=True)
    author = CharField(source="author.get_full_name", read_only=True)
    chapters = SerializerMethodField('get_chapters')

    def get_chapters(self, collection):
        """
        Helper method to render all manga chapters as a list
        """
        only_new = self.context.get('only_new', False)
        if only_new:
            last_date = self.context['last_date']
            queryset = collection.works.filter(publish_date__gte=last_date)
        else:
            queryset = collection.works
        return [{'id': w.id, 'pos': w.unit_count} for w in queryset.all()]

    class Meta:
        model = Collection
        fields = ('id', 'name', 'author', 'cover_url', 'chapters', 'summary', 'source_id')


class PaginatedMangaSerializer(PaginationSerializer):
    """
    Handle pagination logic on serialization process
    """

    class Meta:
        object_serializer_class = MangaSerializer


_is_true = lambda value: bool(value) and value.lower() not in ('false', '0')


def _api_version(val):
    try:
        return int(val)
    except:
        return 1


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
        only_new = _is_true(request.GET.get("new", "false"))
        last_date = dateutil.parser.parse(last_date_string)

        api_version = _api_version(request.GET.get("version", "1"))

        if api_version == 1:
            queryset = Collection.objects.select_related("author").prefetch_related('works').filter(last_updated__gte=last_date, enabled=True, source=CollectionSource.CENTRAL_DE_MANGAS_ID).order_by('name')
        else:
            queryset = Collection.objects.select_related("author").prefetch_related('works').filter(last_updated__gte=last_date, enabled=True).order_by('name')

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

        serializer_context = {'request': request, 'only_new': only_new, 'last_date': last_date}
        serializer = PaginatedMangaSerializer(mangas, context=serializer_context)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Collection.objects.filter(pk=pk)
        serializer = MangaSerializer(queryset)
        return Response(serializer.data)


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


class CollectionAvailabilitySerializer(ModelSerializer):
    manga_id = IntegerField(source="collection.id", read_only=True)
    status = IntegerField(source="status", read_only=True)

    class Meta:
        model = Collection
        fields = ('manga_id', 'status')


class PaginatedMangaStatusSerializer(PaginationSerializer):
    """
    Handle pagination logic on serialization process
    """

    class Meta:
        object_serializer_class = CollectionAvailabilitySerializer


class MangaStatusListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Expose manga list with timestamp and pagination parameters
    """
    model = CollectionAvailability
    serializer_class = CollectionAvailabilitySerializer
    permission_classes = [AllowAny]

    default_timestamp = "2014-01-01 00:00:00.876305+00:00"
    page_size = 100

    def list(self, request, *args, **kwargs):
        last_date_string = request.GET.get("last", self.default_timestamp)
        last_date = dateutil.parser.parse(last_date_string)

        queryset = CollectionAvailability.objects.filter(modify_date__gte=last_date).order_by('id')
        serializer = CollectionAvailabilitySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response("Call not allowed", status=status.HTTP_404_NOT_FOUND)