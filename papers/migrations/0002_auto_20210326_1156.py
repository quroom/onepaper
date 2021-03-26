# Generated by Django 3.1.5 on 2021-03-26 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('addresses', '0001_initial'),
        ('papers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='verifyingexplanation',
            name='insurance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verifying_explanations', to='profiles.insurance'),
        ),
        migrations.AddField(
            model_name='verifyingexplanation',
            name='paper',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verifying_explanation', to='papers.paper'),
        ),
        migrations.AddField(
            model_name='signature',
            name='contractor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='signature', to='papers.contractor'),
        ),
        migrations.AddField(
            model_name='paper',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paper', to='addresses.address'),
        ),
        migrations.AddField(
            model_name='paper',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_papers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paper',
            name='status',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paper', to='papers.paperstatus'),
        ),
        migrations.AddField(
            model_name='explanationsignature',
            name='contractor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='explanation_signature', to='papers.contractor'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='paper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paper_contractors', related_query_name='paper_contractors', to='papers.paper'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_contractors', related_query_name='profile_contractors', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_answers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='contractor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor_answers', to='papers.contractor'),
        ),
        migrations.AddField(
            model_name='answer',
            name='voters',
            field=models.ManyToManyField(related_name='votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='contractor',
            constraint=models.UniqueConstraint(fields=('profile', 'paper'), name='unique_profile_paper'),
        ),
    ]
