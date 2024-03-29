import six

from mongoengine.queryset import QuerySet

from oncourse.libs.django_mongoengine.paginator import Paginator
from oncourse.libs.django_mongoengine.utils.wrappers import WrapDocument, copy_class
from oncourse.libs.django_mongoengine.utils.monkey import get_patched_django_module

__all__ = [
    "MultipleObjectMixin",
    "ListView",
]

djmod = get_patched_django_module(
    "django.views.generic.list",
    QuerySet=QuerySet,
)


@six.add_metaclass(WrapDocument)
class MultipleObjectMixin(djmod.MultipleObjectMixin):
    paginator_class = Paginator


@six.add_metaclass(WrapDocument)
class MultipleObjectTemplateResponseMixin(djmod.MultipleObjectTemplateResponseMixin):
    pass


@copy_class(djmod.ListView)
class ListView(MultipleObjectTemplateResponseMixin, djmod.BaseListView):
    __doc__ = djmod.ListView.__doc__
    paginator_class = Paginator
