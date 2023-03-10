from django.contrib import admin
from interview.models import Candidate
from jobs.models import Resume
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from datetime import datetime
import logging
import csv

# Register your models here.
logger = logging.getLogger(__name__)

# 数据导出
exportable_fields = ('username', 'city', 'telephone', 'bachelor_school', 'master_school', 'degree',
                    'first_result', 'first_interviewer',
                    'second_result', 'second_interviewer',
                    'HR_result', 'HR_interviewer', 'HR_remark')

def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attchment; filename = recruitment-candidates-list-%s.csv' %(
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    # 写入表头
    response.charset = 'utf-8-sig'
    writer = csv.writer(response)
    writer. writerow(
        [ queryset.model._meta.get_field(f).verbose_name.title() for f in field_list ]
    )
    for obj in queryset:
        # 单行记录格式规定
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    logger.info("%s exported %s candidate records" % (request.user, len(queryset)))
    return response
export_model_as_csv.short_description = u'导出为csv文件'

# 候选人管理
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv,]

    list_display = (
        "username", "city", "bachelor_school","get_resume",
        "first_score", "first_result", "first_interviewer",
        "second_score", "second_result", "second_interviewer",
        "HR_score", "HR_result", "HR_interviewer",
        "last_editor"
    )

    # 查询字段
    search_fields = ("username", "telephone", "email", "bachelor_school")
    # 筛选字段
    list_filter = ("city", "first_score", "second_score", "HR_score", "first_interviewer", "second_interviewer", "HR_interviewer")
    # 排序字段
    ordering = ("HR_score", "second_score", "first_score")

    fieldsets = (
        ('基本信息', {'fields': ("userid", ("username", "city","telephone"), ("email", "born_address", "gender"), ("apply_position", "candidate_remark"), ("bachelor_school", "master_school", "doctor_school"), ("major", "degree"), ("test_score_of_general_ability", "paper_score"),"last_editor")}),
        ('初试', {'fields': (("first_score", "first_learning_ability", "first_profession_competency"), "first_advantage", "first_disadvantage", "first_result", ("first_recommend_position", "first_interviewer"), "first_remark",)}),
        ('复试', {'fields': (("second_score", "second_learning_ability", "second_profession_competency"), ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"), "second_advantage", "second_disadvantage", "second_result", "second_recommend_position", "second_interviewer", "second_remark",)}),
        ('终试', {'fields': ("HR_score", ("HR_responsibility", "HR_communication_ability", "HR_logic_ability"), ("HR_potential", "HR_stability"), "HR_advantage", "HR_disadvantage", "HR_result", "HR_interviewer", "HR_remark",)}),
    )

    def get_resume(self, obj):
        if not obj.telephone:
            return ""
        resumes = Resume.objects.filter(phone=obj.telephone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resumes[0].id, "查看简历"))
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True

admin.site.register(Candidate, CandidateAdmin)