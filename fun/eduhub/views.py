import math
import os
import uuid
from datetime import datetime

import bleach
import magic
import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.exceptions import ValidationError
from django.core.paginator import InvalidPage, Paginator
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import (Http404, HttpResponseRedirect, redirect, render,
                              reverse)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from humanize import naturalsize

from fun import bleach_clean

from .apps import EduhubConfig
from .modelforms import (AppraisingModelForm, ASGMemberModelForm,
                         ASharingCModelForm, ASharingGroupModelForm,
                         EduhubhomestickerModelForm, FuncontentModelForm,
                         FuntestModelForm, LabelModelForm)
from .models import (Appraising, ASGMemberClassification, ASharingContent,
                     ASharingGroup, ASharingGroupMember, Classification,
                     Eduhubhomesticker, Funcontent, Funtest, Label,
                     content_name, eduhubhomesticker_name, funcontent_name,
                     funtest_name, label_name)

# Create your views here.

max_cover_size = 500 * 1024

label_create_template = f'eduhub/label_create.html'
label_detail_template = f'eduhub/label_detail.html'
label_delete_template = f'eduhub/label_delete.html'
label_update_template = f'eduhub/label_update.html'
label_list_template = f'eduhub/label_list.html'

content_create_template = f'eduhub/content_create.html'
content_detail_template = f'eduhub/content_detail.html'
content_delete_template = f'eduhub/content_delete.html'
content_update_template = f'eduhub/content_update.html'
content_list_template = f'eduhub/content_list.html'

funcontent_create_template = f'eduhub/funcontent_create.html'
funcontent_detail_template = f'eduhub/funcontent_detail.html'
funcontent_delete_template = f'eduhub/funcontent_delete.html'
funcontent_update_template = f'eduhub/funcontent_update.html'
funcontent_list_template = f'eduhub/funcontent_list.html'

eduhubhomesticker_list_template = f'eduhub/eduhubhomesticker_list.html'
eduhubhomesticker_detail_template = f'eduhub/eduhubhomesticker_detail.html'

eduhub_search_result_template = f'eduhub/eduhub_search_result.html'
eduhub_how_to_classification_template = f'eduhub/how_to_classification.html'


#  _____                            _             _
# |  ___|   _ _ __   ___ ___  _ __ | |_ ___ _ __ | |_
# | |_ | | | | '_ \ / __/ _ \| '_ \| __/ _ \ '_ \| __|
# |  _|| |_| | | | | (_| (_) | | | | ||  __/ | | | |_
# |_|   \__,_|_| |_|\___\___/|_| |_|\__\___|_| |_|\__|
# __     ___
# \ \   / (_) _____      __
#  \ \ / /| |/ _ \ \ /\ / /
#   \ V / | |  __/\ V  V /
#    \_/  |_|\___| \_/\_/


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelModelForm
    template_name = label_create_template
    success_url = reverse_lazy('eduhub:label_list')

    def form_valid(self, form):

        if not form.instance.cover.file:
            form.add_error('cover', _('Cover image is required'))
            return render(self.request, label_create_template,
                          context={'form': form})

        if not str(form.instance.cover.file.content_type).startswith('image/'):
            form.add_error('cover', _('Image allowed only'))
            return render(self.request, label_create_template,
                          context={'form': form})

        if form.instance.cover.file.size > max_cover_size:
            form.add_error(
                'cover',
                _('The length of cover should be less than') +
                ' ' +
                naturalsize(max_cover_size))
            return render(
                self.request, label_create_template,
                context={'form': form}
            )

        form.instance.author = self.request.user

        return super().form_valid(form)


class LabelListView(ListView):
    model = Label

    form_class = LabelModelForm
    template_name = label_list_template
    context_object_name = 'labels'
    ordering = ['-creating_date', ]
    paginate_by = 5
    paginate_orphans = 1

    def paginate_queryset(self, queryset, page_size):

        paginator = self.get_paginator(
            queryset, page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())

        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or \
            self.request.GET.get(page_kwarg) or 1

        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            page = paginator.page(1)
            return (paginator, page, page.object_list, page.has_other_pages())

    def get_queryset(self):

        if (not self.request.user.is_authenticated) or \
                self.request.COOKIES.get('is_my_label_list', False):
            return Label.objects\
                .filter(is_legal=True)\
                .order_by('-creating_date')

        else:
            return Label.objects\
                .filter(is_legal=True, author=self.request.user)\
                .order_by('-creating_date')

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('page', self.request.GET.get('page', 1))
        return response


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    form_class = LabelModelForm
    template_name = label_delete_template
    context_object_name = 'label'
    success_url = reverse_lazy('eduhub:label_list')

    def post(self, request, *args, **kwargs):
        if not Label.objects\
            .filter(pk=self.pk, author=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)


class LabelUpdateView(LoginRequiredMixin, UpdateView):

    model = Label
    form_class = LabelModelForm
    template_name = label_update_template
    context_object_name = 'label'

    def get_success_url(self):
        return '/eduhub/label_list?page=' + self.request.COOKIES.get('page', 1)

    def post(self, request, *args, **kwargs):
        if not Label.objects\
            .filter(pk=self.pk, author=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)


class FuncontentListView(ListView):
    model = Funcontent
    form_class = FuncontentModelForm
    template_name = funcontent_list_template
    context_object_name = 'funcontents'
    ordering = ['-uploading_date', ]
    paginate_by = 5
    paginate_orphans = 1
    pk_url_kwarg = 'label_id'

    def get_queryset(self):
        return Funcontent.objects.filter(
            label__id=self.kwargs['label_id'],
            is_legal=True)\
            .order_by('-uploading_date') \
            if len(str(self.kwargs.get('label_id', ''))) > 0 \
            else Funcontent.objects\
            .filter(is_legal=True)\
            .order_by('-uploading_date')

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.set_cookie('page', self.request.GET.get('page', 1))
        return response

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if len(str(self.kwargs.get('label_id', ''))) > 0:
            context_data['label'] = Label.objects.get(
                id=self.kwargs['label_id'])
            context_data['is_author'] = Label.objects.get(
                id=self.kwargs['label_id']).author == self.request.user
        return context_data


class FuncontentCreateView(LoginRequiredMixin, CreateView):
    model = Funcontent
    form_class = FuncontentModelForm
    template_name = funcontent_create_template
    pk_url_kwarg = 'label_id'

    def get_initial(self):
        initial = super().get_initial()
        classification_id = self.request.COOKIES.get(
            'classification', uuid.UUID(int=0))
        initial['classification'] = Classification.objects.get(
            pk=classification_id) if Classification.objects.filter(
            pk=classification_id).exists() else \
            Classification.objects.first()
        return initial

    def form_valid(self, form):
        form.instance.content = bleach_clean(form.instance.content)
        form.instance.author = self.request.user
        form.instance.label = Label.objects.get(pk=self.kwargs['label_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('eduhub:funcontent_list',
                       kwargs={'label_id': self.kwargs['label_id']})


class FuncontentDetailView(DetailView):
    model = Funcontent
    form_class = FuncontentModelForm
    template_name = funcontent_detail_template


class FuncontentDeleteView(LoginRequiredMixin, DeleteView):
    model = Funcontent
    form_class = FuncontentModelForm
    template_name = funcontent_delete_template

    def post(self, request, *args, **kwargs):

        if not Funcontent.objects\
            .filter(pk=self.pk, label__author=request.user)\
                .exists():
            raise Http404()

        self.label_id = Funcontent.objects.get(pk=self.pk).label.id
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('eduhub:funcontent_list',
                       kwargs={'label_id': self.label_id})


class FuncontentUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcontent
    form_class = FuncontentModelForm
    template_name = funcontent_update_template

    def post(self, request, *args, **kwargs):
        if not Funcontent.objects\
            .filter(pk=self.pk, label__author=request.user)\
                .exists():
            raise Http404()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.content = bleach_clean(form.instance.content)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'eduhub:funcontent_list',
            kwargs={'label_id': self.object.label.id})


funtest_create_template = f'eduhub/{funtest_name}_create.html'
funtest_content_preview = f'eduhub/funtest_content_preview.html'


class FuntestCreateView(CreateView):
    model = Funtest
    template_name = funtest_create_template
    form_class = FuntestModelForm

    def form_valid(self, form):
        form.instance.test_owner = self.request.user
        return super().form_valid(form)


class FuntestContentPreview(TemplateView):
    template_name = funtest_content_preview


def how_to_classification(request):
    if request.method == 'GET':
        return render(request, eduhub_how_to_classification_template)


#  _____    _       _           _     _                        __
# | ____|__| |_   _| |__  _   _| |__ | |__   ___  _ __ ___   __\ \
# |  _| / _` | | | | '_ \| | | | '_ \| '_ \ / _ \| '_ ` _ \ / _ \ \
# | |__| (_| | |_| | | | | |_| | |_) | | | | (_) | | | | | |  __/\ \
# |_____\__,_|\__,_|_| |_|\__,_|_.__/|_| |_|\___/|_| |_| |_|\___| \_\
#      _   _      _           __     ___
#  ___| |_(_) ___| | _____ _ _\ \   / (_) _____      __
# / __| __| |/ __| |/ / _ \ '__\ \ / /| |/ _ \ \ /\ / /
# \__ \ |_| | (__|   <  __/ |   \ V / | |  __/\ V  V /
# |___/\__|_|\___|_|\_\___|_|    \_/  |_|\___| \_/\_/


class EduhubhomestickerListView(ListView):
    model = Eduhubhomesticker
    template_name = eduhubhomesticker_list_template
    form_class = EduhubhomestickerModelForm
    context_object_name = 'eduhubhomestickers'
    ordering = ['-promulgating_date', ]
    paginate_by = 5
    paginate_orphans = 1


class EduhubhomestickerDetailView(DetailView):
    model = Eduhubhomesticker
    template_name = eduhubhomesticker_detail_template
    form_class = EduhubhomestickerModelForm


class EduhubSearch(TemplateView):
    model = Eduhubhomesticker
    template_name = eduhub_search_result_template

    def get_context_data(self, **kwargs):
        eduhub_top_filter = self.request.COOKIES.get('eduhub_top_filter', '')
        eduhub_top_filter = ''

        search_filter = self.request.GET.get('filter', '')
        context_data = super().get_context_data(**kwargs)

        if search_filter == 'labels' or search_filter == '':
            labels = Label.objects.filter(
                (Q(name__icontains=self.request.GET.get('q'))
                 | Q(comment__icontains=self.request.GET.get('q'))))\
                .order_by('-creating_date')

            paginator = Paginator(labels, 5 if search_filter == '' else 10)
            labels = paginator.get_page(self.request.GET.get('page'))
            context_data['labels'] = labels

        if search_filter == 'funcontents' or search_filter == '':
            funcontents = Funcontent.objects.filter(
                (Q(title__icontains=self.request.GET.get('q'))
                    | Q(classification__icontains=self.request.GET.get('q')))
                & Q(classification__icontains=eduhub_top_filter)

            ).order_by('-uploading_date') \
                if len(eduhub_top_filter) > 0 else\
                Funcontent.objects.filter(
                Q(title__icontains=self.request.GET.get('q'))
                | Q(classification__icontains=self.request.GET.get('q'))
            ).order_by('-uploading_date')

            paginator = Paginator(
                funcontents, 5 if search_filter == '' else 10)
            funcontents = paginator.get_page(self.request.GET.get('page'))
            context_data['funcontents'] = funcontents

        return context_data


appraising_create_template = 'eduhub/appraising_create.html'
appraising_list_template = 'eduhub/appraising_list.html'
appraising_update_template = 'eduhub/appraising_update.html'
appraising_detail_template = 'eduhub/appraising_detail.html'
appraising_delete_template = 'eduhub/appraising_delete.html'


#     _                          _     _           __     ___
#    / \   _ __  _ __  _ __ __ _(_)___(_)_ __   __ \ \   / (_) _____      __
#   / _ \ | '_ \| '_ \| '__/ _` | / __| | '_ \ / _` \ \ / /| |/ _ \ \ /\ / /
#  / ___ \| |_) | |_) | | | (_| | \__ \ | | | | (_| |\ V / | |  __/\ V  V /
# /_/   \_\ .__/| .__/|_|  \__,_|_|___/_|_| |_|\__, | \_/  |_|\___| \_/\_/
#         |_|   |_|                            |___/
class AppraisingListView(ListView):
    model = Appraising
    template_name = appraising_list_template
    form_class = AppraisingModelForm
    pass


class AppraisingCreateView(LoginRequiredMixin, CreateView):
    model = Appraising
    template_name = appraising_create_template
    form_class = AppraisingModelForm
    pk_url_kwarg = 'ac_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        asharingcontent = ASharingContent.objects\
            .get(id=self.kwargs['ac_id'])
        context['asharingcontent'] = asharingcontent
        return context

    def form_valid(self, form):
        if not ASharingGroupMember.objects\
            .filter(funuser=self.request.user, enable=True, isjudge=True)\
                .exists():
            return Http404()
        form.instance.acontent = ASharingContent.objects\
            .get(id=self.kwargs['ac_id'])
        form.instance.amember = ASharingGroupMember.objects\
            .get(funuser=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        asg_id = ASharingContent.objects\
            .get(id=self.kwargs['ac_id']).agroup.id
        return reverse(
            'eduhub:appraising_c_list',
            kwargs={'asg_id': asg_id})


class AppraisingUpdateView(LoginRequiredMixin, UpdateView):
    model = Appraising
    template_name = appraising_update_template
    form_class = AppraisingModelForm
    pass


class AppraisingDeleteView(LoginRequiredMixin, DeleteView):
    model = Appraising
    template_name = appraising_delete_template
    form_class = AppraisingModelForm
    pass


class AppraisingDetailView(DetailView):
    model = Appraising
    template_name = appraising_detail_template
    form_class = AppraisingModelForm
    pass

#     _    ____  _                _           __
#    / \  / ___|| |__   __ _ _ __(_)_ __   __ \ \
#   / _ \ \___ \| '_ \ / _` | '__| | '_ \ / _` \ \
#  / ___ \ ___) | | | | (_| | |  | | | | | (_| |\ \
# /_/   \_\____/|_| |_|\__,_|_|  |_|_| |_|\__, | \_\
#                                         |___/
#   ____            _             _ __     ___
#  / ___|___  _ __ | |_ ___ _ __ | |\ \   / (_) _____      __
# | |   / _ \| '_ \| __/ _ \ '_ \| __\ \ / /| |/ _ \ \ /\ / /
# | |__| (_) | | | | ||  __/ | | | |_ \ V / | |  __/\ V  V /
#  \____\___/|_| |_|\__\___|_| |_|\__| \_/  |_|\___| \_/\_/


appraising_c_create_template = 'eduhub/appraising_c_create.html'
appraising_c_list_template = 'eduhub/appraising_c_list.html'
appraising_c_update_template = 'eduhub/appraising_c_update.html'
appraising_c_detail_template = 'eduhub/appraising_c_detail.html'
appraising_c_delete_template = 'eduhub/appraising_c_delete.html'


class ASharingCListView(ListView):
    model = ASharingContent
    template_name = appraising_c_list_template
    form_class = AppraisingModelForm
    context_object_name = 'asharingcontents'
    pk_url_kwarg = 'asg_id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asg_id'] = self.kwargs['asg_id']
        return context

    def get_queryset(self):
        return ASharingContent.objects\
            .filter(is_legal=True, agroup__id=self.kwargs['asg_id'])\
            .order_by('-DOU')


class ASharingCCreateView(LoginRequiredMixin, CreateView):
    model = ASharingContent
    template_name = appraising_c_create_template
    form_class = ASharingCModelForm
    context_object_name = 'asharingcontent'
    pk_url_kwarg = 'asg_id'

    def get_initial(self):
        initial = super().get_initial()
        classification_id = self.request.COOKIES.get(
            'classification', None)
        initial['classification'] = Classification.objects.get(
            pk=classification_id) if classification_id \
            else Classification.objects.first()
        return initial

    def form_valid(self, form):
        form.instance.content = bleach_clean(form.instance.content)
        form.instance.cfrom = self.request.user
        form.instance.agroup = ASharingGroup.objects\
            .get(id=self.kwargs['asg_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'eduhub:appraising_c_list',
            kwargs={'asg_id': self.kwargs['asg_id']})


class ASharingCUpdateView(LoginRequiredMixin, UpdateView):
    model = ASharingContent
    template_name = appraising_c_update_template
    form_class = ASharingCModelForm
    context_object_name = 'asharingcontent'

    def post(self, request, *args, **kwargs):
        if not ASharingContent.objects\
            .filter(pk=self.pk, cfrom=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.acontent = bleach_clean(form.instance.acontent)
        form.instance.cfrom = self.request.user
        return super().form_valid(form)


class ASharingCDeleteView(LoginRequiredMixin, DeleteView):
    model = ASharingContent
    template_name = appraising_c_delete_template
    form_class = ASharingCModelForm
    context_object_name = 'asharingcontent'

    def post(self, request, *args, **kwargs):
        if not ASharingContent.objects\
            .filter(pk=self.pk, cfrom=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)


class ASharingCDetailView(DetailView):
    model = ASharingContent
    template_name = appraising_c_detail_template
    form_class = ASharingCModelForm
    context_object_name = 'asharingcontent'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_judge'] = ASharingGroupMember.objects\
            .filter(funuser=self.request.user, enable=True, isjudge=True)\
            .exists()

        return context


#     _    ____   ____ __  __                _
#    / \  / ___| / ___|  \/  | ___ _ __ ___ | |__   ___ _ __
#   / _ \ \___ \| |  _| |\/| |/ _ \ '_ ` _ \| '_ \ / _ \ '__|
#  / ___ \ ___) | |_| | |  | |  __/ | | | | | |_) |  __/ |
# /_/   \_\____/ \____|_|  |_|\___|_| |_| |_|_.__/ \___|_|
#
asgmember_create_template = 'eduhub/asgmember_create.html'
asgmember_list_template = 'eduhub/asgmember_list.html'
asgmember_update_template = 'eduhub/asgmember_update.html'
asgmember_detail_template = 'eduhub/asgmember_detail.html'
asgmember_delete_template = 'eduhub/asgmember_delete.html'


class ASGMemberListView(ListView):
    model = ASharingGroupMember
    template_name = asgmember_list_template
    form_class = AppraisingModelForm
    context_object_name = 'asgmembers'

    def get_queryset(self):
        return ASharingGroupMember.objects\
            .filter(is_legal=True)\
            .order_by('-DOU')


class ASGMemberCreateView(LoginRequiredMixin, CreateView):
    model = ASharingGroupMember
    template_name = asgmember_create_template
    form_class = ASGMemberModelForm
    context_object_name = 'asgmember'
    success_url = reverse_lazy('eduhub:asgmember_list')

    def get_initial(self):
        initial = super().get_initial()
        classification_id = self.request.COOKIES.get(
            'classification', uuid.UUID(int=0))
        initial['classification'] = Classification.objects.get(
            pk=classification_id)
        return initial

    def form_valid(self, form):
        form.instance.acontent = bleach_clean(form.instance.acontent)
        form.instance.cfrom = self.request.user
        return super().form_valid(form)


class ASGMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = ASharingGroupMember
    template_name = asgmember_update_template
    form_class = ASGMemberModelForm
    context_object_name = 'asgmember'

    def post(self, request, *args, **kwargs):
        if not ASharingGroupMember.objects\
            .filter(pk=self.pk, cfrom=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.acontent = bleach_clean(form.instance.acontent)
        form.instance.cfrom = self.request.user
        return super().form_valid(form)


class ASGMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = ASharingGroupMember
    template_name = asgmember_delete_template
    form_class = ASGMemberModelForm
    context_object_name = 'asgmember'

    def post(self, request, *args, **kwargs):
        if not ASharingGroupMember.objects\
            .filter(pk=self.pk, cfrom=request.user)\
                .exists():
            raise Http404()
        return super().post(request, *args, **kwargs)


class ASGMemberDetailView(DetailView):
    model = ASharingGroupMember
    template_name = asgmember_detail_template
    form_class = ASGMemberModelForm
    context_object_name = 'asgmember'
    pass

#     _    ____  _                _              ____
#    / \  / ___|| |__   __ _ _ __(_)_ __   __ _ / ___|_ __ ___  _   _ _ __
#   / _ \ \___ \| '_ \ / _` | '__| | '_ \ / _` | |  _| '__/ _ \| | | | '_ \
#  / ___ \ ___) | | | | (_| | |  | | | | | (_| | |_| | | | (_) | |_| | |_) |
# /_/   \_\____/|_| |_|\__,_|_|  |_|_| |_|\__, |\____|_|  \___/ \__,_| .__/
#                                         |___/                      |_|
# __     ___
# \ \   / (_) _____      __
#  \ \ / /| |/ _ \ \ /\ / /
#   \ V / | |  __/\ V  V /
#    \_/  |_|\___| \_/\_/


asgroup_list_template = 'eduhub/asharinggroup_list.html'
asgroup_update_template = 'eduhub/asharinggroup_update.html'
asgroup_delete_template = 'eduhub/asharinggroup_delete.html'


class ASGroupListView(ListView):
    model = ASharingGroup
    template_name = asgroup_list_template
    form_class = ASharingGroupModelForm
    context_object_name = 'asgroups'

    def get_queryset(self):
        gmembers = ASharingGroupMember.objects .filter(
            enable=True, funuser=self.request.user).select_related('agroup')
        return [m.agroup for m in gmembers]


class ASGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ASharingGroup
    template_name = asgroup_update_template
    form_class = ASharingGroupModelForm
    context_object_name = 'asgroup'

    def form_valid(self, form):
        if form.instance.founder != self.request.user:
            raise Http404()
        return super().form_valid(form)


class ASGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ASharingGroup
    template_name = asgroup_delete_template
    form_class = ASharingGroupModelForm
    context_object_name = 'asgroup'

    def post(self, request, *args, **kwargs):
        if form.instance.founder != self.request.user:
            raise Http404()
        return super().post(request, *args, **kwargs)
