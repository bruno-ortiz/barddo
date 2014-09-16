# -*- coding: utf-8 -*-
from PIL import Image

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils.html import escape
from dajaxice.utils import deserialize_form
from django.contrib.auth.decorators import login_required
from pilkit.processors import Crop
from django.forms.models import model_to_dict
from easy_thumbnails.files import get_thumbnailer
from django.utils.translation import ugettext as _
from django.core.mail import mail_admins

from core.models import Collection, Work
from core.tasks import notify_collection_updated
from follow.models import Follow
from .forms import CollectionForm, WorkForm, CoverOnlyWorkForm


@login_required
@dajaxice_register
def validate_unique_collection(request, collection_name):
    """
    Used to validate when collection name is unique
    """
    ajax = Dajax()

    try:
        Collection.objects.get(name__iexact=escape(collection_name.lower().strip()))
        ajax.script("callback_collection_name_is_not_avaliable()")

    except Collection.DoesNotExist:
        ajax.script("callback_collection_name_is_avaliable()")

    return ajax.json()


@login_required
@dajaxice_register
def register_a_collection(request, form):
    """
    Called asynchronously to validate/save a new collection.
    Right now we only do a simple model validation.
    """
    ajax = Dajax()
    form = CollectionForm(deserialize_form(form))

    if form.is_valid():
        collection = form.save(commit=False)
        collection.author = request.user
        collection.save()

        ajax.script('callback_validate_collection_ok()')
    else:
        ajax.script('callback_validate_collection_error()')
        ajax.remove_css_class("#collection-form div.form-group", "has-error")

        for field, errors in form.errors.items():
            ajax.script("error_tooltip('#collection-form #id_%s', '%s');" % (field, "<br />".join(errors)))
            ajax.script('$("#collection-form #id_%s").closest("div.form-group").addClass("has-error")' % field)

    return ajax.json()


@login_required
@dajaxice_register
def validate_work_information(request, form):
    """
    Partially validates a new artist work. Basically, we ignore cover validation, that will only be
    considered on a later step
    """
    ajax = Dajax()
    form = WorkForm(deserialize_form(form))

    if not form.is_valid():
        ajax.script('callback_validate_work_error()')
        ajax.remove_css_class("#work-form div.form-group", "has-error")

        for field, errors in form.errors.items():
            print field, errors
            ajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
            ajax.script('$("#work-form #id_%s").closest("div.form-group").addClass("has-error")' % field)
    else:
        ajax.script('callback_validate_work_ok()')

    return ajax.json()


@login_required
@dajaxice_register
def register_a_work(request):
    """
    Create a new artist work. The most important part here, is the cover parsing. We need to save the cover before
    cropping it.

    Note that we also set the collection cover to the new one.
    """
    ajax = Dajax()
    form = WorkForm(request.POST, request.FILES)

    # TODO: validate minimal image size
    if form.is_valid():
        new_work = form.save(commit=False)
        new_work.total_pages = 0
        new_work.save()

        x_ratio = new_work.cover.width / float(request.POST["width"])
        y_ratio = new_work.cover.height / float(request.POST["height"])

        print x_ratio, y_ratio

        cx, cy = -float(request.POST["crop_x"]) * x_ratio, -float(request.POST["crop_y"]) * y_ratio
        cw, ch = float(request.POST["crop_w"]) * x_ratio, float(request.POST["crop_h"]) * y_ratio

        print cx, cy, cw, ch, request.POST["crop_w"], request.POST["crop_h"]

        crop_image(new_work, int(cx), int(cy), int(cw), int(ch))

        # TODO: only set as collection cover when user opted for it
        new_work.collection.cover = new_work.cover
        new_work.collection.save()

        ajax.script('callback_create_work_ok(' + str(new_work.id) + ')')

        mail_admins(u"[Barddo] Nova obra criada: " + new_work.title,
                    u"A obra '{}' acaba de ser criada no Barddo por '{}".format(new_work.title, request.user.username))
    else:
        ajax.script('callback_create_work_error()')
        for field, errors in form.errors.items():
            print field, errors

    return ajax.json()


@login_required
@dajaxice_register
def change_work_cover(request):
    """
    Create a new artist work. The most important part here, is the cover parsing. We need to save the cover before
    cropping it.

    Note that we also set the collection cover to the new one.
    """
    ajax = Dajax()

    id = escape(request.POST["id"])
    work = Work.objects.get(pk=id)

    if work.author != request.user:
        ajax.script(u'gritter_error("{}")'.format(_("You are not the owner of this work!")))
        return ajax.json()

    form = CoverOnlyWorkForm(request.POST, request.FILES, instance=work)

    # TODO: validate minimal image size
    if form.is_valid():
        changed_work = form.save()

        x_ratio = changed_work.cover.width / float(request.POST["width"])
        y_ratio = changed_work.cover.height / float(request.POST["height"])

        print x_ratio, y_ratio

        cx, cy = -float(request.POST["crop_x"]) * x_ratio, -float(request.POST["crop_y"]) * y_ratio
        cw, ch = float(request.POST["crop_w"]) * x_ratio, float(request.POST["crop_h"]) * y_ratio

        print cx, cy, cw, ch, request.POST["crop_w"], request.POST["crop_h"]

        crop_image(changed_work, int(cx), int(cy), int(cw), int(ch))

        # TODO: only set as collection cover when user opted for it
        changed_work.collection.cover = changed_work.cover
        changed_work.collection.save()

        thumb = get_thumbnailer(changed_work.cover)["big_cover"]

        ajax.script('callback_edit_cover_ok(' + str(changed_work.id) + ', "' + thumb.url + '")')
    else:
        ajax.script('callback_edit_cover_error()')

    return ajax.json()


def crop_image(work, x, y, width, height):
    """
    Crop given image with given coords and size
    """
    image = Image.open(work.cover.path)
    crop = Crop(width=width, height=height, x=x, y=y)
    crop.process(image).save(work.cover.path, 'JPEG', quality=90)


@login_required
@dajaxice_register
def edit_work_field(request, _id, field, value):
    dajax = Dajax()

    instance = Work.objects.get(id=_id)
    data = model_to_dict(instance)
    data[field] = value

    form = WorkForm(instance=instance, data=data)
    if form.is_valid():
        form.save()
        dajax.remove_css_class('#id_{0}'.format(field), 'field-error')
        dajax.add_css_class('#id_{0}'.format(field), 'field-success')
        dajax.script("gritter_feedback('{}');".format(_("Value successfuly changed!")))
    else:
        dajax.remove_css_class('#id_{0}'.format(field), 'field-success')
        dajax.add_css_class('#id_{0}'.format(field), 'field-error')
        errors = form.errors[field]
        dajax.script("error_tooltip('#id_%s', '%s');" % (field, "<br />".join(errors)))
        dajax.script("gritter_error('{}');".format(_("Error changing value...")))
    return dajax.json()


@login_required
@dajaxice_register
def publish_work(request, work_id):
    """
    Change work status to published
    """
    ajax = Dajax()

    work = Work.objects.get(id=work_id)

    request_user = request.user
    if request_user.is_staff or work.author_id == request_user.id:
        work.is_published = True
        work.save()

        notify_collection_updated(request_user, work)

        ajax.script("publish_work_callback({});".format(work_id))

        mail_admins(u"[Barddo] Nova obra publicada: " + work.title,
                    u"A obra '{}' acaba de ser publicada no Barddo por '{}".format(work.title, request_user.username))
    else:
        ajax.script("alert('Unable to publish work. You are not the onwer.');")

    return ajax.json()


@login_required
@dajaxice_register
def toggle_subscription(request, collection_id):
    """
    Toggle given user following on request user
    """
    ajax = Dajax()
    current_user = request.user
    collection = Collection.objects.get(id=collection_id)
    follows = Follow.objects.follows(current_user, collection)

    if follows:
        Follow.objects.remove_follower(current_user, collection)
        ajax.script('collection_unsubscribed_callback()')

    else:
        Follow.objects.add_follower(current_user, collection)
        ajax.script('collection_subscribed_callback()')

    return ajax.json()
