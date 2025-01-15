from django.conf import settings
from django.views.generic.edit import FormView

from .forms import JsonRpcForm
from .jsonrpc_client import JsonRpcClient


class JsonRpcView(FormView):
    template_name = 'jsonrpc/jsonrpc_form.html'
    form_class = JsonRpcForm
    success_url = '/'

    def form_valid(self, form):
        client = JsonRpcClient('slb.medv.ru', 443, settings.CERTIFICATE, settings.PRIVATE_KEY)
        response = client.call_method(form.cleaned_data['method'], form.cleaned_data['params'])
        return self.render_to_response(self.get_context_data(form=form, response=response))
