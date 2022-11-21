# Generated by Django 4.1.2 on 2022-11-13 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_name_active_list_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='active_list',
            name='porpose_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='active_list',
            name='category',
            field=models.ManyToManyField(related_name='categorys', to='auctions.categorys'),
        ),
    ]