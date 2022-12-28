# Generated by Django 4.1.1 on 2022-12-28 08:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtensionService_Collaborators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ExtensionService_OfferedPrograms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_title', models.CharField(max_length=100)),
                ('research_progress', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Presented', 'Presented'), ('Published', 'Published')], default=None, max_length=100)),
                ('research_area', models.CharField(blank=True, choices=[('Algorithms and Theory', 'Algorithms and Theory'), ('Data Management', 'Data Management'), ('Data Mining and Modeling', 'Data Mining and Modeling'), ('Distributed Systems and Parallel Computing', 'Distributed Systems and Parallel Computing'), ('Economics and Electronic Commerce', 'Economics and Electronic Commerce'), ('Education Innovation', 'Education Innovation'), ('General Science', 'General Science'), ('Health & Bioscience', 'Health & Bioscience'), ('Hardware and Architecture', 'Hardware and Architecture'), ('Human-Computer Interaction and Visualization', 'Human-Computer Interaction and Visualization'), ('Information Retrieval and the Web', 'Information Retrieval and the Web'), ('Machine Intelligence', 'Machine Intelligence'), ('Machine Perception', 'Machine Perception'), ('Machine Translation', 'Machine Translation'), ('Mobile Systems', 'Mobile Systems'), ('Natural Language Processing', 'Natural Language Processing'), ('Networking', 'Networking'), ('Quantum Computing', 'Quantum Computing'), ('Robotics', 'Robotics'), ('Security, Privacy and Abuse Prevention', 'Security, Privacy and Abuse Prevention'), ('Software Engineering', 'Software Engineering'), ('Software Systems', 'Software Systems'), ('Speech Processing', 'Speech Processing'), ('Others', 'Others')], default=None, max_length=100, null=True)),
                ('degree_level', models.CharField(blank=True, choices=[('Associate Degree', 'Associate Degree'), ('Bachelor Degree', 'Bachelor Degree'), ('Masters Degree', 'Masters Degree'), ('Doctorate Degree', 'Doctorate Degree'), ('Independent', 'Independent')], default=None, max_length=100, null=True)),
                ('researcher_school', models.CharField(max_length=100)),
                ('faculty_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(default='NSTP10', max_length=20)),
                ('course_title', models.CharField(default='National Service Training Program 1', max_length=100)),
                ('course_credits', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('semester', models.CharField(choices=[('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester')], default='1st Semester', max_length=50)),
                ('year', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default=1, max_length=50)),
                ('course_lec_units', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('course_lab_units', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('course_hours_per_week', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('specialization', models.CharField(blank=True, choices=[('Service Management Specialization Track', 'Service Management Specialization Track'), ('Business Analytics Specialization Track', 'Business Analytics Specialization Track'), ('Web and Mobile Application Specialization Track', 'Web and Mobile Application Specialization Track'), ('None', 'None')], default='None', max_length=50, null=True)),
                ('course_type', models.CharField(choices=[('General Education Courses', 'General Education Courses'), ('Common Courses', 'Common Courses'), ('Professional Courses', 'Professional Courses'), ('Professional Electives', 'Professional Electives'), ('Physical Education', 'Physical Education'), ('National Service Training Program', 'National Service Training Program'), ('None', 'None')], default='None', max_length=50)),
                ('pre_requisite', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_member.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('Faculty', 'Faculty'), ('Department Head', 'Department Head'), ('Research Coordinator', 'Research Coordinator'), ('Extension Coordinator', 'Extension Coordinator')], default='Faculty', max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(choices=[('Faculty', 'Faculty'), ('Department Head', 'Department Head'), ('Research Coordinator', 'Research Coordinator'), ('Extension Coordinator', 'Extension Coordinator')], default='Faculty', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects_Taught',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('handled_subjects', models.ManyToManyField(to='faculty_member.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Research_Published',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateField()),
                ('publication', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('research_license', models.CharField(choices=[('Creative Commons Licenses', 'Creative Commons Licenses'), ('Alternatives Publishing Licenses', 'Alternatives Publishing Licenses'), ('Research Repository Licences', 'Research Repository Licences'), ('Open Access', 'Open Access'), ('None', 'None')], default='None', max_length=200, null=True)),
                ('abstract', models.TextField(max_length=1200)),
                ('presented_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_member.research')),
            ],
        ),
        migrations.CreateModel(
            name='Research_Presented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=200)),
                ('event_venue', models.CharField(max_length=200)),
                ('event_start_date', models.DateField()),
                ('event_end_date', models.DateField()),
                ('presentation_type', models.CharField(choices=[('Physical', 'Physical'), ('Virtual', 'Virtual'), ('Hyrbrid', 'Hyrbrid')], default='Conference', max_length=200, null=True)),
                ('event_type', models.CharField(choices=[('Conference', 'Conference'), ('Seminars', 'Seminars'), ('Product Launch', 'Product Launch'), ('Corporate / Executive Meetings', 'Corporate / Executive Meetings'), ('Summits', 'Summits'), ('Symposium', 'Symposium'), ('Trade Shows', 'Trade Shows'), ('Others', 'Others')], default='Physical', max_length=200, null=True)),
                ('org_name', models.CharField(max_length=200)),
                ('org_website_url', models.CharField(max_length=200)),
                ('org_support', models.CharField(max_length=200)),
                ('org_description', models.TextField(max_length=500)),
                ('date_presented', models.DateField()),
                ('published_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_member.research')),
            ],
        ),
        migrations.CreateModel(
            name='ExtensionService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='extension_service_profilepic/')),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('contact_no', models.CharField(blank=True, max_length=15, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('background', models.TextField(max_length=500)),
                ('extension_head', models.CharField(blank=True, max_length=200, null=True)),
                ('ext_collaborator_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_member.extensionservice_collaborators')),
                ('ext_offeredprograms_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty_member.extensionservice_offeredprograms')),
                ('faculty_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
