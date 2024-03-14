from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class GeraPDFMixin:
    def gerar_pdf(self, template_name: str, data: dict = {}):
        template = get_template(template_name)
        html = template.render(data)
        result = BytesIO()
        try:
            pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        except Exception as e:
            print(e)
            return None
