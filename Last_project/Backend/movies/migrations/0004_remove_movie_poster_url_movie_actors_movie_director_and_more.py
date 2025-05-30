# Generated by Django 4.2.21 on 2025-05-23 02:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_place_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster_url',
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='', upload_to='posters/'),
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserPrefer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=20)),
                ('mood', models.CharField(choices=[('happy', '행복'), ('sad', '슬픔'), ('angry', '분노'), ('fear', '두려움'), ('disgust', '혐오'), ('surprise', '놀람')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
