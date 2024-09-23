from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView

from kitchen.forms import (
    DishForm,
    DishTypeForm,
    CookForm,
    UserRegistrationForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookSearchForm
)
from kitchen.models import Dish, DishType, Cook


class DishListView(generic.ListView):
    model = Dish
    template_name = "kitchen/list_of_dish.html"
    context_object_name = "dishes"
    paginate_by = 10

    def get_queryset(self):
        queryset = Dish.objects.all().order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DishSearchForm(self.request.GET)
        return context


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"
    context_object_name = "dish"


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'kitchen/form.html'
    extra_context = {'title': 'Add New Dish'}

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('kitchen:dish-list')


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'kitchen/form.html'
    extra_context = {'title': 'Update Dish'}

    def get_success_url(self):
        return reverse('kitchen:dish-detail', args=[self.object.id])


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy('kitchen:dish-list')
    template_name = "kitchen/dish_config_delete.html"


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/list_of_dishtypes.html"
    context_object_name = "dish_types"

    def get_queryset(self):
        queryset = DishType.objects.all().order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DishTypeSearchForm(self.request.GET)
        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = 'kitchen/form.html'
    extra_context = {'title': 'Add New Dish'}


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    form_class = DishTypeForm
    template_name = 'kitchen/form.html'


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy('kitchen:dish-type-list')
    template_name = "kitchen/dishtype_config_delete.html"


class CookListView(generic.ListView):
    model = Cook
    template_name = "kitchen/list_of_cooks.html"
    context_object_name = "cooks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Cook.objects.all().order_by('username')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(username__icontains=query) | Q(years_of_experience__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CookSearchForm(self.request.GET)
        return context


class CookDetailView(generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookForm
    template_name = 'kitchen/form.html'
    extra_context = {'title': 'Add New Cook'}


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookForm
    template_name = 'kitchen/form.html'


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = 'kitchen/cook_confirm_delete.html'
    success_url = reverse_lazy('kitchen:cook-list')


class HomeView(TemplateView):
    template_name = "kitchen/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = Dish.objects.all()[:5]
        context['cooks'] = Cook.objects.all()[:5]
        context['dishtypes'] = DishType.objects.all()
        return context


class UserRegistrationView(generic.View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})