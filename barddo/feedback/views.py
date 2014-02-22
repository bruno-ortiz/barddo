from django.views.generic.edit import FormView
from feedback.forms import FeedbackForm

__author__ = 'jose'


class FeedbackView(FormView):
    template_name = "feedback-modal.html"
    form_class = FeedbackForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        initials = {}

        if request.user.is_authenticated():
            initials['name'] = request.user.get_full_name()
            initials['email'] = request.user.email

        form = self.form_class(initial=initials)
        context['form'] = form

        return self.render_to_response(context)