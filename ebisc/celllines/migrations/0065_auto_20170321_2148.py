# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ebisc.celllines.models


class Migration(migrations.Migration):

    dependencies = [
        ('celllines', '0064_auto_20170321_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='CelllineGenomeAnalysisFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vcf_file', models.FileField(upload_to=ebisc.celllines.models.upload_to, null=True, verbose_name='VCF File', blank=True)),
            ],
            options={
                'ordering': [],
                'verbose_name': 'Cell line genome analysis file',
                'verbose_name_plural': 'Cell line genome analysis files',
            },
        ),
        migrations.RemoveField(
            model_name='celllinegenomeanalysis',
            name='data',
        ),
        migrations.AddField(
            model_name='celllinegenomeanalysis',
            name='analysis_method',
            field=models.CharField(max_length=300, null=True, verbose_name='Analysis method', blank=True),
        ),
        migrations.AddField(
            model_name='celllinekaryotype',
            name='karyotype_file',
            field=models.FileField(upload_to=ebisc.celllines.models.upload_to, null=True, verbose_name='File', blank=True),
        ),
        migrations.AlterField(
            model_name='celllinegenomeanalysis',
            name='cell_line',
            field=models.ForeignKey(related_name='genome_analysis', verbose_name='Cell line', to='celllines.Cellline'),
        ),
        migrations.AddField(
            model_name='celllinegenomeanalysisfile',
            name='genome_analysis',
            field=models.ForeignKey(related_name='genome_analysis_files', verbose_name='Cell line genome analysis', to='celllines.CelllineGenomeAnalysis'),
        ),
    ]
