from django.shortcuts import render_to_response, redirect
from core.models import Work


# Create your views here.
def embeddable_reader(request, work_id):
    # The user is accessing from outside, for now, disable unless authenticated
    if not request.user.is_authenticated():
        return redirect("core.work.detail", work_id=work_id)

    work = Work.objects.select_related("collection", "author", "author__profile").get(id=work_id)
    return render_to_response('embeddable_reader.html', {"work": work})