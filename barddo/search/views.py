# coding=utf-8
from django.db.models import Count
from django.utils.html import escape
from django.utils.translation import ugettext as _

from accounts.models import BarddoUser
from accounts.views import ProfileAwareView
from core.models import Collection, Work
from rating.models import Rating


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

            if len(collections) == 0 and len(works) == 0 and len(people) == 0:
                context = self.get_context_data(**{
                    "user": request.user,
                    "error": _(u"Não foi encontrado nenhum resultado para sua busca."),
                    "success": False
                })
            else:
                context = self.get_context_data(**{
                    "user": request.user,
                    "collections": collections,
                    "works": works,
                    "people": people,
                    "success": True
                })
        else:
            context = self.get_context_data(**{
                "user": request.user,
                "error": _(u"Pesquisa inválida."),
                "success": False
            })

        return super(SearchResultView, self).render_to_response(context)

    def remove_small_words(self, text):
        return ' & '.join(word for word in text.split() if len(word) > 3)

    def search_in_collections(self, text):
        return Collection.search_manager.search(text). \
            annotate(work_count=Count("work"))[:30]

    def search_in_works(self, text):
        sub_query = Rating.objects.annotate(Count('id')).values('id__count') \
            .extra(where=["core_work.id = rating_rating.work_id"]).filter(like=True).query

        return Work.search_manager.search(text).extra(select={"like_count": sub_query})[:30]

    def search_in_users(self, text):
        return BarddoUser.search_manager.search(text)[:30]


search_result = SearchResultView.as_view()