# coding=utf-8
import json
import datetime

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect
from redis_metrics.models import R

from core.utils import validate_work_owner
from follow.models import Follow
from .models import Collection, Work
from accounts.views import ProfileAwareView, LoginRequiredMixin
from payments.forms import BankAccountForm
from publishing.views import publisher_landpage
from payments.models import FINISHED_PURCHASE_ID
from rating.models import Rating, user_likes
from payments.models import BankAccount, Item


class IndexView(ProfileAwareView):
    LAST_WEEK = -7

    LAST_MONTH = -30

    LAST_YEAR = -365

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next', '')

        barddo_user = self.get_barddo_user(request.user)

        new_works = self.get_new_works(barddo_user)
        rising_works = self.get_rising_works(barddo_user)
        trending_works = self.get_trending_works(barddo_user)
        context = {"next_url": next_url,
                   "new_works": new_works,
                   "rising_works": rising_works,
                   "trending_works": trending_works}
        if barddo_user:
            owned_works = self.get_owned_works(barddo_user)
            context['owned_works'] = owned_works
        return super(IndexView, self).get(request, **context)

    def get_new_works(self, user):
        # TODO: quando tivermos fluxo constante, limitar o que é exibido
        limit = self.get_relative_date(self.LAST_YEAR)

        new_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(
            user).filter(publish_date__gte=limit,
                         is_published=True). \
            order_by("-publish_date")
        return self.__filter_works_with_pages(new_works)

    def get_rising_works(self, user):
        # TODO: quando tivermos fluxo constante, limitar o que é exibido
        limit = self.get_relative_date(self.LAST_YEAR)

        # TODO: Rever o distinct
        rising_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(
            user).liked_after(limit).filter(
            is_published=True).distinct(). \
            order_by("-total_likes")
        return self.__filter_works_with_pages(rising_works)

    def get_trending_works(self, user):
        # TODO: quando tivermos fluxo constante, limitar o que é exibido
        limit = self.get_relative_date(self.LAST_YEAR)

        # TODO: Rever o distinct
        trending_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(
            user).liked_after(limit).filter(
            is_published=True).distinct(). \
            order_by("-total_likes")
        return self.__filter_works_with_pages(trending_works)

    def get_barddo_user(self, user):
        return user if user.is_authenticated() else None

    def get_relative_date(self, delta):
        return datetime.datetime.now() + datetime.timedelta(days=delta)

    def get_owned_works(self, barddo_user):
        return Work.objects.owned_by(barddo_user)

    def __filter_works_with_pages(self, works):
        # TODO: REMOVER quando tivermos controle de páginas pelo banco
        return filter(lambda work: work.has_pages(), works)


index = IndexView.as_view()

# ##
# ## Artist Dashboard
# ##


class ArtistDashboardView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'dashboard/artist_dashboard.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.select_related("works").filter(author_id=kwargs['user'].id)

        context = {
            'collections': collections
        }
        context.update(kwargs)
        return super(ArtistDashboardView, self).get_context_data(**context)

    def get(self, request, *args, **kwargs):
        if not request.user.is_publisher:
            return redirect(publisher_landpage)

        return super(ArtistDashboardView, self).get(request, *args, **kwargs)


artist_dashboard = ArtistDashboardView.as_view()


class ArtistStatisticsView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'dashboard/artist_statistics.html'

    def get_context_data(self, **kwargs):
        sold_works = Item.objects.select_related('work', "purchase").filter(
            work__author_id=kwargs['user'].id, purchase__status=FINISHED_PURCHASE_ID
        ).order_by("-purchase__date", "-purchase__id")

        total = sum([item.price - item.taxes for item in sold_works])

        start_date = datetime.date(2014, 01, 01)
        end_date = datetime.date.today()

        context = {
            'sold_works': sold_works,
            'total': total,
            "start_date": start_date,
            "end_date": end_date
        }

        context.update(kwargs)
        return super(ArtistStatisticsView, self).get_context_data(**context)

    def get(self, request, *args, **kwargs):
        if not request.user.is_publisher:
            return redirect(publisher_landpage)

        return super(ArtistStatisticsView, self).get(request, *args, **kwargs)


class BankAccountMixin(object):
    def get_bank_account_data(self):
        data = {}
        try:
            acc = BankAccount.objects.get(user=self.request.user)
            data['bank_account'] = acc
            data['has_account'] = True
        except BankAccount.DoesNotExist:
            data['has_account'] = False
        return data


class ArtistBankAccountView(LoginRequiredMixin, BankAccountMixin, ProfileAwareView):
    template_name = 'dashboard/bank_account.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_publisher:
            return redirect(publisher_landpage)

        bank_data = self.get_bank_account_data()
        if bank_data['has_account']:
            form = BankAccountForm(instance=bank_data['bank_account'])
        else:
            form = BankAccountForm()
        bank_data['form'] = form
        return super(ArtistBankAccountView, self).get(request, *args, **bank_data)

    def post(self, request):
        bank_data = self.get_bank_account_data()
        if bank_data['has_account']:
            form = BankAccountForm(request.POST, instance=bank_data['bank_account'])
        else:
            form = BankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.user = request.user
            bank_account.save()
        return super(ArtistBankAccountView, self).get(request, form=form, **bank_data)


# ##
# ## Work sorted upload
# ##
class UploadWorkPageView(LoginRequiredMixin, View):
    def post(self, request, work_id, *args, **kwargs):
        """
            This view will handle a work image upload, one per time, always.
            By convention, the file will be named by it's position on media folder.
        """

        # Check if the user owns the work
        work = Work.objects.select_related("collection").get(id=work_id)
        validate_work_owner(request.user, work)
        # Handle uploaded file to the server media folder
        _file = request.FILES['file']
        added_page = work.add_page(_file)
        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id,
            "work_page": added_page.sequence
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


upload_work_page = UploadWorkPageView.as_view()


class MoveWorkPageView(LoginRequiredMixin, View):
    def post(self, request, work_id, *args, **kwargs):
        """
            Handle sortable images widget. This work by convention, the image shown to the user is in the exact position
            as the file on the server folder.

            Then the user drag and sort the thumbnail, the files will be sorted exactly the same way.
        """
        # Check if the user owns the work
        work = Work.objects.select_related("collection", "work_pages").get(id=work_id)
        validate_work_owner(request.user, work)

        pos_from = int(request.REQUEST['position_from'])
        pos_to = int(request.REQUEST['position_to'])

        work.move_page(pos_from, pos_to)
        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


move_work_page = MoveWorkPageView.as_view()


class RemoveWorkPageView(LoginRequiredMixin, View):
    """
    Remove a page and rename subsequent ones
    """

    def post(self, request, work_id, page_index, *args, **kwargs):
        # Check if the user owns the work
        page_index = int(page_index)
        work = Work.objects.select_related('collection', 'work_pages').get(id=work_id)
        validate_work_owner(request.user, work)

        work.remove_page(page_index)

        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id,
            "work_page": len(work.pages)
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


remove_work_page = RemoveWorkPageView.as_view()


# ##
# ## Docs
# ##
class AboutUsView(ProfileAwareView):
    template_name = 'docs/about-us.html'


class TermsView(ProfileAwareView):
    template_name = 'docs/terms.html'


class HelpView(ProfileAwareView):
    template_name = 'docs/help.html'


class WorkPageView(ProfileAwareView):
    template_name = 'work_page/work_page.html'

    def get(self, request, *args, **kwargs):
        work = Work.objects.get(id=kwargs['work_id'])
        voters = Rating.objects.filter(work__id=kwargs['work_id']).select_related("user")

        this_work_view_slug = "work_views_{}".format(kwargs['work_id'])

        kwargs["work"] = work
        kwargs["voted"] = user_likes(request.user, kwargs['work_id']) if request.user.is_authenticated() else False
        kwargs["voters"] = voters

        r = R()
        kwargs["views"] = r.get_metric(this_work_view_slug)['year']

        return super(WorkPageView, self).get(request, *args, **kwargs)


class CollectionPageView(ProfileAwareView):
    template_name = 'collection_page/collection_page.html'

    def get(self, request, *args, **kwargs):
        collection = Collection.objects.get(slug=kwargs['collection_slug'])
        r = R()
        kwargs["views"] = 0
        works = collection.works.filter(is_published=True)
        for work in works:
            this_work_view_slug = "work_views_{}".format(work.id)
            kwargs["views"] += int(r.get_metric(this_work_view_slug)['year']) if r.get_metric(this_work_view_slug)['year'] is not None else 0
        kwargs['collection'] = collection
        kwargs['works'] = works
        kwargs['subscribers'] = Follow.objects.followers(collection)
        if request.user.is_authenticated():
            kwargs['subscribed'] = Follow.objects.follows(request.user, collection)
        return super(CollectionPageView, self).get(request, *args, **kwargs)