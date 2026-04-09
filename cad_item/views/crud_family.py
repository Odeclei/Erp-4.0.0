# flake8: noqa
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from cad_item.forms import FamiliForm
from cad_item.models import FamilyProd

PER_PAGE = 25


class FamilyProdView(ListView):
    model = FamilyProd
    template_name = "cad_item/family/index.html"
    context_object_name = "form_family"
    paginate_by = PER_PAGE

    def get_queryset(self):
        # Otimização: ordenação feita diretamente na query principal
        return FamilyProd.objects.all().order_by("description")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lógica de range de páginas para o template
        if context.get('is_paginated'):
            page_obj = context['page_obj']
            num_pages = context['paginator'].num_pages
            current_page = page_obj.number
            
            start_index = max(1, current_page - 2)
            end_index = min(num_pages, start_index + 4) # Garante 5 páginas se possível
            if end_index == num_pages:
                start_index = max(1, num_pages - 4)
                
            context["page_range"] = range(start_index, end_index + 1)
        return context

class FamilySearchView(FamilyProdView): # Herda de FamilyProdView para manter paginação e contexto
    def get_queryset(self):
        search_value = self.request.GET.get("search", "").strip()
        if not search_value:
            return super().get_queryset()
            
        return super().get_queryset().filter(
            Q(refer__icontains=search_value) | 
            Q(description__icontains=search_value)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_value"] = self.request.GET.get("search", "").strip()
        return ctx


class FamilyCreateView(CreateView):
    model = FamilyProd
    template_name = "cad_item/family/create.html"
    form_class = FamiliForm
    context_object_name = "form_family"

    def get_success_url(self):
        return reverse_lazy("cad_item:family_list")  # type: ignore

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form_action = reverse("cad_item:family_create")
        ctx.update(
            {
                "form_action": form_action,
            }
        )
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "Família Criada com Sucesso.")
        return super().form_valid(form)


class FamilyUpdateView(UpdateView):
    model = FamilyProd
    template_name = "cad_item/family/create.html"
    form_class = FamiliForm
    context_object_name = "form_family"
    success_url = reverse_lazy("cad_item:family_list")

    def form_valid(self, form):
        messages.success(self.request, "Família Alterada com Sucesso.")
        return super().form_valid(form)


# class FamilySearchView(ListView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._search_value = ""

#     def setup(self, request, *args, **kwargs):
#         self._search_value = request.GET.get("search", "").strip()
#         return super().setup(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         search_value = self._search_value
#         ctx.update(
#             {
#                 "search_value": search_value,
#             }
#         )
#         return ctx

#     def get_queryset(self):
#         search_value = self._search_value
#         return (
#             super()
#             .get_queryset()
#             .filter(
#                 Q(refer__icontains=search_value)
#                 | Q(description__icontains=search_value)
#             )
#         )

#     model = FamilyProd
#     template_name = "cad_item/family/index.html"
#     context_object_name = "form_family"
