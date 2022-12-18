from django.conf.urls import url
from django.urls import path
from django.conf import settings
from jobs import views

urlpatterns = [
    # 职位列表
    path("joblist/", views.joblist, name="joblist"),
    path('job/<int:job_id>/', views.detail, name='detail'),
    # 提交简历
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    # 首页自动跳转到 职位列表
    path("", views.joblist, name="name"),
]