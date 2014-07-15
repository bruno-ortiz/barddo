from hashlib import md5
import tempfile
import os
import codecs

from django.templatetags.i18n import register

from django.conf import settings
from django.utils import translation
import markdown

from accounts.models import BarddoUserProfile


@register.inclusion_tag('markdown.html', takes_context=True)
def localized_markdown(context, file):
    """
    Render a markdown document content as html, loading the correct version for the user current language
    """
    language = get_language_for_user(context['request'])
    content = get_document_content(file, language)
    return {'content': parse_markdown(content)}


def parse_markdown(content):
    """
    Parse markdown content as HTML, trying to use a simple cache strategy to avoid slow downs
    on reparsing the same file everytime
    """
    content_hash = md5(content.encode("utf-8")).hexdigest()
    cached_file = os.path.join(tempfile.gettempdir(), content_hash + ".cache")

    if not os.path.exists(cached_file):
        parsed_content = markdown.markdown(content, output_format="xhtml5", safe_mode="escape")
        with codecs.open(cached_file, "w", "utf-8") as cache:
            cache.write(parsed_content)
    else:
        with codecs.open(cached_file, "r", "utf-8") as cache:
            parsed_content = cache.read()

    return parsed_content


def get_document_content(document, language):
    """
    Get document content based on language provided, if the document is no in given
    language, then a fallback one will be used
    """
    file_path = os.path.join(settings.DOCUMENTS_ROOT, language, document + ".markdown")

    # Fallback to default language document (required to exist)
    if not os.path.exists(file_path):
        file_path = os.path.join(settings.DOCUMENTS_ROOT, settings.LANGUAGE_CODE, document + ".markdown")

    with codecs.open(file_path, "r", "utf-8") as file:
        return file.read()


def get_language_for_user(request):
    """
    Tries to determine user language to load correct document language
    """
    if request.user.is_authenticated():
        try:
            accountProfile = BarddoUserProfile.objects.get(user=request.user)
            return accountProfile.language
        except BarddoUserProfile.DoesNotExist:
            pass

    return translation.get_language_from_request(request)