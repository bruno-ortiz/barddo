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
    """
    Handle the search result page
    TODO: handle searches and return as JSON
    """
    template_name = 'page_template.html'

    def get(self, request, *args, **kwargs):
        """
        Searches over works, collections and users and render the resulta page with found results
        The query parameter is the GET "t", if not found, nothing will be returned
        """
        query_text = escape(request.GET.get('t', ''))

        if len(query_text) > 0:
            query_text = self.parse_search_criteria(query_text)

            collections = self.search_in_collections(query_text)
            works = self.search_in_works(query_text)
            people = self.search_in_users(query_text)

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

    def parse_search_criteria(self, text):
        """
        Transform user query in a valid and relevant fulltext seach.

        For now the model used is the Boolean FTS mode, so:
            - '*' are used to enable partial matching
            - words > 3 characters receive a '+' preffix, so they become required to the result
            - words <= 3 characters aren't required to the result, bu should be considered
        """
        criteria = ""
        for word in text.split(' '):
            # obligatory word and partial match
            if len(word) > 3:
                criteria += "+" + word + "* "

            # optional word, and partial match, if found, higher relevance returned
            else:
                criteria += word + "* "

        return criteria

    def search_in_collections(self, query_text):
        """
        Just search relevant collections with given query
        """
        return Collection.search_manager.search_ordered(query_text, ("name", "summary")).annotate(
            work_count=Count("work"))

    def search_in_works(self, query_text):
        """
        Just search relevant works with given query, other information are required on result,
        like if the user liked a work or not
        """
        sub_query = Rating.objects.annotate(Count('id')).values('id__count') \
            .extra(where=["core_work.id = rating_rating.work_id"]).filter(like=True).query

        return Work.search_manager.search_ordered(query_text, ("title", "summary")).extra(
            select={"like_count": sub_query})

    def search_in_users(self, query_text):
        """
        Just search relevant users with given query
        """
        return BarddoUser.search_manager.search(query_text)


search_result = SearchResultView.as_view()