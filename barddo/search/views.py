# coding=utf-8
from django.utils.html import escape
from django.utils.translation import ugettext as _

from accounts.models import BarddoUser

from accounts.views import ProfileAwareView
from core.models import Collection, Work


__author__ = 'jovial'


class SearchResultView(ProfileAwareView):
    template_name = 'page_template.html'

    def get(self, request, *args, **kwargs):
        text = escape(request.GET.get('t', ''))

        text = self.remove_small_words(text)

        if len(text) > 0:
            collections = self.search_in_collections(text)
            works = self.search_in_works(text)
            people = self.search_in_users(text)

            if len(collections) != 0 and len(works) != 0 and len(people) != 0:
                context = self.get_context_data(**{'user': request.user, "error": _(u"Não foi encontrado nenhum resultado para sua busca."), "success": False})
            else:
                context = self.get_context_data(**{'user': request.user, "collections": collections, "works": works, "people": people, "success": True})
        else:
            context = self.get_context_data(**{'user': request.user, "error": _(u"Pesquisa inválida."), "success": False})

        return super(SearchResultView, self).render_to_response(context)

    def remove_small_words(self, text):
        return ' '.join(word for word in text.split() if len(word) > 3)

    def search_in_collections(self, text):
        return Collection.objects.filter(name__icontains=text)[:30]

    def search_in_works(self, text):
        return Work.objects.filter(title__icontains=text)[:30]

    def search_in_users(self, text):
        return BarddoUser.objects.filter(username__icontains=text)[:30]


search_result = SearchResultView.as_view()