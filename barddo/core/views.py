# coding=utf-8
import json
import datetime
import os

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Collection, Work
from .exceptions import InvalidFileUploadError, ChangeOnObjectNotOwnedError
from accounts.views import ProfileAwareView, LoginRequiredMixin
from publishing.views import publisher_landpage
from rating.models import Rating, user_likes


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

        new_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(user).filter(publish_date__gte=limit). \
            order_by("-publish_date")
        return self.__filter_works_with_pages(new_works)

    def get_rising_works(self, user):
        # TODO: quando tivermos fluxo constante, limitar o que é exibido
        limit = self.get_relative_date(self.LAST_YEAR)

        # TODO: Rever o distinct
        rising_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(user).liked_after(limit).distinct(). \
            order_by("-total_likes")
        return self.__filter_works_with_pages(rising_works)

    def get_trending_works(self, user):
        # TODO: quando tivermos fluxo constante, limitar o que é exibido
        limit = self.get_relative_date(self.LAST_YEAR)

        # TODO: Rever o distinct
        trending_works = Work.objects.select_related("collection", "author", "author__profile").total_likes().liked_by(user).liked_after(limit).distinct(). \
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
    template_name = 'artist_dashboard.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(author_id=kwargs['user'].id)

        context = {
            'collections': collections
        }
        context.update(kwargs)
        return super(ArtistDashboardView, self).get_context_data(**context)

    def get(self, request, *args, **kwargs):
        if not request.user.is_publisher():
            return redirect(publisher_landpage)

        context = self.get_context_data(**{'user': request.user})
        context.update(kwargs)

        return super(ArtistDashboardView, self).render_to_response(context)


artist_dashboard = ArtistDashboardView.as_view()


class CollectionDetailView(LoginRequiredMixin, ProfileAwareView):
    template_name = 'modals/collection_detail.html'

    def get(self, request, collection_id, *args, **kwargs):
        collection = Collection.objects.get(id=collection_id)
        works = Work.objects.filter(collection_id=collection_id)

        context = {
            'collection': collection,
            'works': works
        }

        return super(CollectionDetailView, self).render_to_response(context)


collection_detail = CollectionDetailView.as_view()


# ##
# ## Work sorted upload
# ##


class UploadWorkPageView(LoginRequiredMixin, View):
    def post(self, request, work_id, *args, **kwargs):
        """
            This view will handle a work image upload, one per time, always.
            By convention, the file will be named by it's position on media folder.
        """
        file_name, file_extension = os.path.splitext(request.FILES['file'].name)

        # Black list sanity check
        if file_extension.lower()[1:] not in Work.ALLOWED_EXTENSIONS:
            raise InvalidFileUploadError()

        # Check if the user owns the work
        work = Work.objects.select_related("collection").get(id=work_id)
        if work.is_owner(request.user):
            raise ChangeOnObjectNotOwnedError()

        # Create the collection work folder if needed
        work_path = work.media_path()
        if not os.path.exists(work_path):
            os.makedirs(work_path)

        # Handle uploaded file to the server media folder
        work_content = work.image_files()
        file_name = ("%03d" % len(work_content)) + file_extension  # TODO: shadow file names?
        work.handle_uploaded_file(file_name, request.FILES['file'])

        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id,
            "work_page": len(work_content)
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


upload_work_page = UploadWorkPageView.as_view()


# TODO: thin views, fat models
class MoveWorkPageView(LoginRequiredMixin, View):
    def post(self, request, work_id, *args, **kwargs):
        """
            Handle sortable images widget. This work by convention, the image shown to the user is in the exact position
            as the file on the server folder.

            Then the user drag and sort the thumbnail, the files will be sorted exactly the same way.
        """
        # Check if the user owns the work
        work = Work.objects.select_related("collection").get(id=work_id)
        if work.is_owner(request.user):
            raise ChangeOnObjectNotOwnedError()

        work_path = work.media_path()
        work_content = work.image_files()

        pos_from = int(request.REQUEST['position_from'])
        pos_to = int(request.REQUEST['position_to'])

        start = min(pos_from, pos_to)

        # Rename affected files to avoid name collisions
        for x in xrange(start, len(work_content)):
            os.rename(os.path.join(work_path, work_content[x]), os.path.join(work_path, "MOVING_" + work_content[x]))

        # Switch given file position
        if pos_from > pos_to:
            work_content.insert(pos_to, work_content[pos_from])
            del work_content[pos_from + 1]
        else:
            work_content.insert(pos_to + 1, work_content[pos_from])
            del work_content[pos_from]

        # Adjust subsequent file names
        for x in xrange(start, len(work_content)):
            _, extension = os.path.splitext(work_content[x])
            os.rename(os.path.join(work_path, "MOVING_" + work_content[x]),
                      os.path.join(work_path, "%03d" % x + extension))

        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id
        }
        return HttpResponse(json.dumps(context), content_type="application/json")


move_work_page = MoveWorkPageView.as_view()


# TODO: thin views, fat models
class RemoveWorkPageView(LoginRequiredMixin, View):
    """
    Remove a page and rename subsequent ones
    """

    def post(self, request, work_id, page_index, *args, **kwargs):
        # Check if the user owns the work
        page_index = int(page_index)
        work = Work.objects.select_related("collection").get(id=work_id)
        if work.is_owner(request.user):
            raise ChangeOnObjectNotOwnedError()

        # Handle uploaded file to the server media folder
        work_content = work.image_files()
        work_path = work.media_path()

        # Rename affected files to avoid name collisions
        for x in xrange(page_index + 1, len(work_content)):
            os.rename(os.path.join(work_path, work_content[x]), os.path.join(work_path, "MOVING_" + work_content[x]))

        # Remove entry
        os.remove(os.path.join(work.media_path(), work_content[page_index]))
        del work_content[page_index]

        # Adjust subsequent file names
        for x in xrange(page_index, len(work_content)):
            _, extension = os.path.splitext(work_content[x])
            os.rename(os.path.join(work_path, "MOVING_" + work_content[x]),
                      os.path.join(work_path, "%03d" % x + extension))

        # TODO: create somekind of lock, to handle more than one user editing the same work?
        context = {
            "success": "true",
            "work_id": work.id,
            "work_page": len(work_content)
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

    def get(self, request, work_id, *args, **kwargs):
        work = Work.objects.get(id=work_id)
        voters = Rating.objects.filter(work__id=work_id).select_related("user")

        this_work_view_slug = "work_views_{}".format(work_id)

        context = self.get_context_data(**{'user': request.user})
        context["work"] = work
        context["voted"] = user_likes(request.user, work_id) if request.user.is_authenticated() else False
        context["voters"] = voters

        from redis_metrics.models import R

        r = R()
        context["views"] = r.get_metric(this_work_view_slug)['year']
        context.update(kwargs)

        return super(WorkPageView, self).render_to_response(context)