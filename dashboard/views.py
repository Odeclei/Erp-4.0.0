from django.shortcuts import render


def initial(request):

    return render(
        request,
        'dashboard/index.html'
    )
