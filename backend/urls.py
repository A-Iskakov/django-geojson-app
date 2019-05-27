from django.urls import path

from .views import RegisterAccount

app_name = 'backend'
urlpatterns = [
    path('', RegisterAccount.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('employee/<int:object_id>/<str:action>/', EmployeeCompanyPage.as_view(company_or_employee=False)),
    # path('company/<int:object_id>/<str:action>/', EmployeeCompanyPage.as_view(company_or_employee=True)),
    # path('job/<int:object_id>/<str:action>/', JobsPage.as_view()),
    # path('common/<str:action>/', CommonCounters.as_view()),
    # path('reset/Hj9VmI7jIZ/', ResetCacheStats.as_view()),
    # path('', CheckPage.as_view()),
]