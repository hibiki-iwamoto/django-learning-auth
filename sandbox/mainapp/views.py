from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    """メインページ表示

    Args:
        request (HttpRequest): リクエスト情報

    Returns:
        HttpResponse: mainapp/index.htmlをベースにしたレスポンス情報
    """
    return render(request, "mainapp/index.html")
