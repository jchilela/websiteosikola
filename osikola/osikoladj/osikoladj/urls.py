from django.conf.urls import patterns
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('osikolaapp.views',
    # Examples:
    url(r'^$', 'loginProfessores', name='loginProfessores'),
    url(r'^professores/', 'iniciop', name='iniciop'),
    url(r'^editar/dadospessoais/', 'EditarDadosPessoais', name='EditarDadosPessoais'),
    url(r'^editar/dadosdeacesso/', 'editarDadosAcesso', name='editarDadosAcesso'),
    url(r'^editar/notas/', 'editarNotas', name='editarNotas'),


    url(r'^show_image/$', 'show_image', name='show_image'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
