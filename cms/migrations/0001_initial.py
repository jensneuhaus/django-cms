# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.models import ACCESS_CHOICES, Page
from cms.utils.conf import get_cms_setting
from django.conf import settings
from django.db import models, migrations
import django.utils.timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

template_choices = [(x, _(y)) for x, y in get_cms_setting('TEMPLATES')]

User = get_user_model()

user_model_label = '%s.%s' % (User._meta.app_label, User._meta.model_name)
user_ptr_name = '%s_ptr' % User._meta.object_name.lower()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSPlugin',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name=_('ID'), auto_created=True, serialize=False)),
                ('position', models.PositiveSmallIntegerField(null=True, editable=False, blank=True, verbose_name=_('position'))),
                ('language', models.CharField(db_index=True, max_length=15, verbose_name=_("language"), editable=False)),
                ('plugin_type', models.CharField(db_index=True, max_length=50, verbose_name=_('plugin_name'), editable=False)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=_('creation date'), editable=False)),
                ('changed_date', models.DateTimeField(auto_now=True)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AliasPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, to='cms.CMSPlugin', auto_created=True, parent_link=True, serialize=False)),
                ('plugin', models.ForeignKey(null=True, to='cms.CMSPlugin', related_name='alias_reference', editable=False)),
            ],
            options={
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='cmsplugin',
            name='parent',
            field=models.ForeignKey(null=True, to='cms.CMSPlugin', blank=True, editable=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='GlobalPagePermission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name=_('ID'), auto_created=True, serialize=False)),
                ('can_change', models.BooleanField(default=True, verbose_name=_('can edit'))),
                ('can_add', models.BooleanField(default=True, verbose_name=_('can add'))),
                ('can_delete', models.BooleanField(default=True, verbose_name=_('can delete'))),
                ('can_change_advanced_settings', models.BooleanField(default=False, verbose_name=_('can change advanced settings'))),
                ('can_publish', models.BooleanField(default=True, verbose_name=_('can publish'))),
                ('can_change_permissions', models.BooleanField(default=False, help_text='on page level', verbose_name=_('can change permissions'))),
                ('can_move_page', models.BooleanField(default=True, verbose_name=_('can move'))),
                ('can_view', models.BooleanField(default=False, help_text='frontend view restriction', verbose_name=_('view restricted'))),
                ('can_recover_page', models.BooleanField(default=True, help_text='can recover any deleted page', verbose_name=_('can recover pages'))),
                ('group', models.ForeignKey(null=True, to='auth.Group', verbose_name=_('group'), blank=True)),
                ('sites', models.ManyToManyField(null=True, help_text='If none selected, user haves granted permissions to all sites.', blank=True, to='sites.Site', verbose_name=_('sites'))),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name=_('user'), blank=True)),
            ],
            options={
                'verbose_name': 'Page global permission',
                'verbose_name_plural': 'Pages global permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name=_('ID'), auto_created=True, serialize=False)),
                ('created_by', models.CharField(max_length=70, verbose_name=_('created by'), editable=False)),
                ('changed_by', models.CharField(max_length=70, verbose_name=_('changed by'), editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('changed_date', models.DateTimeField(auto_now=True)),
                ('publication_date', models.DateTimeField(db_index=True, null=True, help_text='When the page should go live. Status must be "Published" for page to go live.', blank=True, verbose_name=_('publication date'))),
                ('publication_end_date', models.DateTimeField(db_index=True, null=True, help_text='When to expire the page. Leave empty to never expire.', blank=True, verbose_name=_('publication end date'))),
                ('in_navigation', models.BooleanField(db_index=True, default=True, verbose_name=_('in navigation'))),
                ('soft_root', models.BooleanField(db_index=True, default=False, help_text='All ancestors will not be displayed in the navigation', verbose_name=_('soft root'))),
                ('reverse_id', models.CharField(db_index=True, max_length=40, verbose_name=_('id'), null=True, help_text='A unique identifier that is used with the page_url templatetag for linking to this page', blank=True)),
                ('navigation_extenders', models.CharField(db_index=True, max_length=80, blank=True, verbose_name=_('attached menu'), null=True)),
                ('template', models.CharField(max_length=100, default='INHERIT', help_text='The template used to render the content.', verbose_name=_('template'), choices=template_choices)),
                ('login_required', models.BooleanField(default=False, verbose_name=_('login required'))),
                ('limit_visibility_in_menu', models.SmallIntegerField(db_index=True, default=None, verbose_name=_('menu visibility'), null=True, choices=Page.LIMIT_VISIBILITY_IN_MENU_CHOICES, help_text='limit when this page is visible in the menu', blank=True)),
                ('is_home', models.BooleanField(db_index=True, default=False, editable=False)),
                ('application_urls', models.CharField(db_index=True, max_length=200, blank=True, verbose_name=_('application'), null=True)),
                ('application_namespace', models.CharField(max_length=200, null=True, blank=True, verbose_name=_('application instance name'))),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('publisher_is_draft', models.BooleanField(db_index=True, default=True, editable=False)),
                ('languages', models.CharField(max_length=255, null=True, blank=True, editable=False)),
                ('revision_id', models.PositiveIntegerField(default=0, editable=False)),
                ('xframe_options', models.IntegerField(default=0, choices=Page.X_FRAME_OPTIONS_CHOICES)),
                ('parent', models.ForeignKey(null=True, to='cms.Page', related_name='children', blank=True)),
                ('publisher_public', models.OneToOneField(null=True, to='cms.Page', related_name='publisher_draft', editable=False)),
                ('site', models.ForeignKey(to='sites.Site', verbose_name=_('site'), related_name='djangocms_pages', help_text='The site the page is accessible at.')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'permissions': (('view_page', 'Can view page'), ('publish_page', 'Can publish page'), ('edit_static_placeholder', 'Can edit static placeholders')),
                'verbose_name_plural': 'pages',
                'verbose_name': 'page',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PagePermission',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name=_('ID'), auto_created=True, serialize=False)),
                ('can_change', models.BooleanField(default=True, verbose_name=_('can edit'))),
                ('can_add', models.BooleanField(default=True, verbose_name=_('can add'))),
                ('can_delete', models.BooleanField(default=True, verbose_name=_('can delete'))),
                ('can_change_advanced_settings', models.BooleanField(default=False, verbose_name=_('can change advanced settings'))),
                ('can_publish', models.BooleanField(default=True, verbose_name=_('can publish'))),
                ('can_change_permissions', models.BooleanField(default=False, help_text='on page level', verbose_name=_('can change permissions'))),
                ('can_move_page', models.BooleanField(default=True, verbose_name=_('can move'))),
                ('can_view', models.BooleanField(default=False, help_text='frontend view restriction', verbose_name=_('view restricted'))),
                ('grant_on', models.IntegerField(default=5, verbose_name=_('Grant on'), choices=ACCESS_CHOICES)),
                ('group', models.ForeignKey(null=True, to='auth.Group', verbose_name=_('group'), blank=True)),
                ('page', models.ForeignKey(null=True, to='cms.Page', verbose_name=_('page'), blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, verbose_name=_('user'), blank=True)),
            ],
            options={
                'verbose_name': 'Page permission',
                'verbose_name_plural': 'Page permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageUser',
            fields=[
                (user_ptr_name, models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, auto_created=True, parent_link=True, serialize=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_users')),
            ],
            options={
                'verbose_name': 'User (page)',
                'verbose_name_plural': 'Users (page)',
            },
            bases=(user_model_label,),
        ),
        migrations.CreateModel(
            name='PageUserGroup',
            fields=[
                ('group_ptr', models.OneToOneField(primary_key=True, to='auth.Group', auto_created=True, parent_link=True, serialize=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_usergroups')),
            ],
            options={
                'verbose_name': 'User group (page)',
                'verbose_name_plural': 'User groups (page)',
            },
            bases=('auth.group',),
        ),
    ]
