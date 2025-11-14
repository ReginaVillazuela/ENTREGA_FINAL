from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse 
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count 
from django.http import HttpResponseRedirect 
from .models import Page, Comment, CATEGORY_CHOICES
from .forms import PageForm, CommentForm 

CATEGORY_CHOICES = [
    ('BIO', 'Biología'),
    ('CAL', 'Cálculo'),
    ('CIE', 'Ciencias'),
    ('NOV', 'Novedades'),
    ('OTR', 'Otros'),
]


def welcome_view(request):
    return render(request, 'pages/landing.html')

@login_required
def home_view(request):
    return render(request, 'pages/home.html')

@login_required
def about_view(request):
    return render(request, 'pages/about.html')

@login_required
def list_pages(request):
    """
    Vista de listado que utiliza CATEGORY_CHOICES para la lógica de filtrado.
    """
    query = request.GET.get('q') 
    category_code = request.GET.get('category') 
    
    pages = Page.objects.all().order_by('-created_at')
    category_name = "Todos los Papers" 

    if category_code:
        pages = pages.filter(category=category_code)
        category_name = dict(CATEGORY_CHOICES).get(category_code, "Categoría") 

    if query:
        pages = pages.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        category_name = f"Resultados de '{query}' en {category_name}"

    context = {
        'pages': pages,
        'query': query, 
        'category_name': category_name, 
        'category_code': category_code, 
    }
    return render(request, 'pages/pages_list.html', context)

@login_required
def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk)
    comments = page.comments.all().order_by('-created_at')
    return render(request, 'pages/page_detail.html', {'page': page, 'comments': comments, 'comment_form': CommentForm()}) 

@login_required
def add_comment(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST) 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.page = page
            comment.user = request.user
            comment.save()
    return redirect('page_detail', pk=pk)

@login_required
def page_rate(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == "POST":
        rating = int(request.POST.get('rating', 0))
        if 1 <= rating <= 5:
            page.rating_total += rating
            page.rating_count += 1
            page.save()
    return redirect('page_detail', pk=pk)



class CategorySelectionView(LoginRequiredMixin, View):
    """Vista para seleccionar la categoría (grupos) usando CATEGORY_CHOICES."""
    template_name = 'pages/category_selection.html'

    def get(self, request):
        categories_data = []
        for code, name in CATEGORY_CHOICES:
            count = Page.objects.filter(category=code).count()
            categories_data.append({
                'code': code,
                'name': name,
                'page_count': count,
            })

        context = {
            'categories': categories_data
        }
        return render(request, self.template_name, context)


class PageCreateView(LoginRequiredMixin, CreateView):
    """
    CORREGIDO: Asigna autor y usa redirección dinámica.
    """
    model = Page
    form_class = PageForm 
    template_name = 'pages/page_form.html'

    def get_success_url(self):
        return reverse('page_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """Asigna el usuario actual como el autor antes de guardar."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/page_form.html'
    
    def get_success_url(self):
        return reverse('page_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = 'pages/page_confirm_delete.html'
    success_url = reverse_lazy('pages_list')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)