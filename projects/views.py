from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta

from projects.models import Project, Release, Item, ItemLog, ItemComments
from projects import forms


number_of_days_to_chart = 30


# usage: raise DebugMessage('asdf')
class DebugMessage(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


#
#   Projects
#


class ProjectIndex(ListView):
    model = Project
    template_name = 'project_index.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectIndex, self).get_context_data(**kwargs)
        total_projects = Project.objects.count()
        total_releases = Release.objects.all().count()
        total_items = Item.objects.all().count()
        context['total_projects'] = total_projects
        context['total_releases'] = total_releases
        context['total_items'] = total_items

        # get release totals for project view
        release_query = 'select projects_project.id as id, count(projects_release.id) as release_total from projects_project left join projects_release on projects_release.project_id_id = projects_project.id group by projects_project.id'
        release_rows = Project.objects.raw(release_query)
        release_totals = {}
        for row in release_rows:
            release_totals[row.id] = row.release_total
        context['release_totals'] = release_totals

        # get item totals for project view
        item_query = 'select projects_project.id as id, count(projects_item.id) as item_total from projects_project left join projects_release on projects_release.project_id_id = projects_project.id left join projects_item on projects_item.release_id_id = projects_release.id group by projects_project.id'
        item_rows = Project.objects.raw(item_query)
        item_totals = {}
        for row in item_rows:
            item_totals[row.id] = row.item_total
        context['item_totals'] = item_totals

        return context


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_view.html'
    slug_field = 'project_id'

    def get_context_data(self, **kwargs):

        context = super(ProjectDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs['pk']

        releases = Release.objects.filter(project_id=project_id).order_by('number')    # .order_by('-id')
        releases_return = []

        for release in releases:

            closed_items = Item.objects.filter(release_id=release.id)
            closed_items = closed_items.exclude(status=0)
            closed_items = closed_items.exclude(status=1)
            closed_items = closed_items.exclude(status=2)
            closed_items = closed_items.exclude(status=3)

            open_items = Item.objects.filter(release_id=release.id)
            open_items = open_items.exclude(status=4)
            open_items = open_items.exclude(status=5)

            release_return = release

            release_return.closed_items = closed_items.count()
            release_return.open_items = open_items.count()
            release_return.total_items = closed_items.count() + open_items.count()

            releases_return.append(release_return)

        context['releases'] = releases_return

        # provide total project items for charting
        project_total_items = Item.objects.filter(release__project__id=project_id).count()
        context['project_total_items'] = project_total_items

        # build any missing days in the reporting (for last N days, set number_of_days_in_chart at the top of this file)
        check_project_reporting(project_id)

        # get data for chart
        item_logs = get_item_logs(project_id)
        # ************************************************** need to add an order_by and limit the results to the last N

        if 'project_tab' in self.request.session:
            project_tab = self.request.session['project_tab']
            if project_tab == 'burn_down':
                raise DebugMessage('burn_down')
                # draw_burn_down_chart()
                pass
            else:   # project_tab == 'item_completion'
                '''
                returned_data = draw_item_completion_chart(project_id, item_logs)

                context['open_issues_data'] = returned_data['open_issues_data']
                context['closed_issues_data'] = returned_data['closed_issues_data']
                context['date_data'] = returned_data['date_data']
                '''

                data = draw_item_completion_chart(project_id, item_logs)
                data['project_id'] = project_id
                context['chart'] = get_ajax_chart('item_completion', data)

        else:
            # default tab

            self.request.session['project_tab'] = 'item_completion'

            returned_data = draw_item_completion_chart(project_id, item_logs)

            context['open_issues_data'] = returned_data['open_issues_data']
            context['closed_issues_data'] = returned_data['closed_issues_data']
            context['date_data'] = returned_data['date_data']

        return context


def get_item_logs(project_id):
    item_logs_query = 'SELECT * FROM (SELECT * FROM projects_itemlog WHERE project_id_id = "{project_id}" ORDER BY day DESC LIMIT {days}) ORDER BY day ASC'
    item_logs_query = item_logs_query.replace("{project_id}", project_id)
    item_logs_query = item_logs_query.replace("{days}", str(number_of_days_to_chart))
    return ItemLog.objects.raw(item_logs_query)


def draw_item_completion_chart(project_id, item_logs):
        # build data set for the main chart
        open_issues_data = ''
        closed_issues_data = ''
        date_data = ''
        for log in item_logs:
            open_issues_data += str(log.total_open) + ','
            closed_issues_data += str(log.total_closed) + ','
            date_data += "'" + str(log.day.strftime("%Y-%m-%d")) + "', "

        today_open_query = 'SELECT project_id_id as id, count(*) as total FROM projects_item as i ' \
                           'INNER JOIN projects_release as r ON r.id = i.release_id_id ' \
                           'WHERE project_id_id = "{project_id}" and i.status != 4 and i.status != 5 '
        today_open_query = today_open_query.replace("{project_id}", project_id)
        today_open = Item.objects.raw(today_open_query)[0]

        today_closed_query = 'SELECT project_id_id as id, count(*) as total FROM projects_item as i ' \
                             'INNER JOIN projects_release as r ON r.id = i.release_id_id ' \
                             'WHERE project_id_id = "{project_id}" and (i.status = 4 or i.status = 5) '
        today_closed_query = today_closed_query.replace("{project_id}", project_id)
        today_closed = Item.objects.raw(today_closed_query)[0]

        open_issues_data += str(today_open.total)
        closed_issues_data += str(today_closed.total)
        date_data += "'" + datetime.now().strftime("%Y-%m-%d") + "'"

        return_val = {}
        return_val['open_issues_data'] = open_issues_data
        return_val['closed_issues_data'] = closed_issues_data
        return_val['date_data'] = date_data

        return return_val


class ProjectCreate(CreateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'

    def form_valid(self, form):

        # create the project object and save it
        self.object = form.save()
        created_project_id = self.object.id
        created_project_title = self.object.title
        backlog_title = created_project_title + ' Backlog'

        # create a "backlog" release to start out with
        backlog = Release.objects.create(
            project_id=created_project_id,
            title=backlog_title,
            detail='The default backlog group',
        )
        backlog.save()

        return super(ModelFormMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        project_id = ''
        self.success_url = '/projects/project_id'.replace("project_id", project_id)
        return super(ProjectCreate, self).post(request, *args, **kwargs)


class ProjectCreateQuick(ProjectCreate):

    template_name = 'project_quick.html'

    def form_valid(self, form):

        # create the project object and save it
        self.object = form.save()
        created_project_id = self.object.id
        created_project_title = self.object.title
        backlog_title = created_project_title + ' Backlog'

        # create a "backlog" release to start out with
        backlog = Release.objects.create(
            project_id=created_project_id,
            title=backlog_title,
            detail='The default backlog group',
        )
        backlog.save()
        backlog_object_id = backlog.pk

        # backlog_object_id = backlog_object.id

        # create sub items under the backlog
        quick_items = self.request.POST['quick_items']

        for line in iter(quick_items.splitlines()):
            value_result = ''
            if "," in line:
                values = line.split(',')
                for value in values[1:]:
                    value_result += value + ','
            else:
                values[0] = line

            value_result = value_result[0:-1]

            new_item = Item.objects.create(
                release_id=backlog_object_id,
                title=values[0],
                detail=value_result,
                date_started=None,
                date_completed=None,
            )
            new_item.save()

        '''
        # old version, replaced with newer version with some bug fixes above
        for lines in iter(quick_items.splitlines()):
            values = lines.split(',')
            new_item = Item.objects.create(
                release_id=backlog_object_id,
                title=values[0],
                detail=values[1],
                date_started=None,
                date_completed=None,
            )
            new_item.save()
        '''

        return super(ModelFormMixin, self).form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'
    slug_field = 'project_id'


'''
def project_delete(request, pk):
    Project.objects.filter(pk=pk).delete()
    slug_field = 'project_id'
    return http.HttpResponseRedirect('/projects/')
'''


class ProjectDelete(DeleteView):

    model = Project
    template_name = 'project_delete.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'


#
#   Releases
#


class ReleaseIndex(ListView):
    model = Release
    template_name = 'release_index.html'

    def get_queryset(self):
        object_list = Release.objects.all()     # (project__id=self.kwargs['project_id'])
        return object_list


class ReleaseDetail(DetailView):

    model = Release
    template_name = 'release_view.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')
        context['project_id'] = project_id

        # ***********************
        # Need to modify "items" query to only return open objects (non 4, 5 status objects)

        items = Item.objects.filter(release=release_id).order_by('-priority')
        # context['items'] = items

        # ***********************
        # Additional set of closed items
        # closed_items = Item.objects.filter(release=release_id, status=Item.CLOSED_ACTION)

        closed_items = []
        open_items = []
        closed_items_total = 0
        open_items_total = 0

        total_count = 0
        for item in items:
            total_count += 1
            if item.status == 4 or item.status == 5:
                closed_items_total += 1
                closed_items.append(item)
            else:
                open_items.append(item)

        context['open_items'] = open_items
        context['closed_items'] = closed_items

        percent_complete = 0.0
        if total_count == 0:
            percent_complete = 0.0
        else:
            percent_complete = float(closed_items_total) / float(total_count)

        context['percent_complete'] = percent_complete
        # context['closed_items_total'] = closed_items_total
        # context['total_items'] = total_count

        # set backlog_flag true if backlog is in the title of the release
        title = context['release'].title
        title = title.lower()
        if title.find('backlog') == -1:
            backlog_flag = False
        else:
            backlog_flag = True
        context['backlog_flag'] = backlog_flag

        return context


class ReleaseBacklogAdd(DetailView):

    model = Release
    template_name = 'release_backlog.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseBacklogAdd, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')
        context['project_id'] = project_id
        items = Item.objects.filter(release=release_id).order_by('-priority')
        context['items'] = items

        # set backlog_flag true if backlog is in the title of the release
        title = context['release'].title
        title = title.lower()
        if title.find('backlog') == -1:
            backlog_flag = False
        else:
            backlog_flag = True
        context['backlog_flag'] = backlog_flag

        # todo:

        # pull backlog id
        backlog = Release.objects.filter(title__contains='Backlog', project__id=project_id)
        backlog_id = backlog[0].id
        context['backlog_id'] = backlog_id

        # pull "left" - the backlog data
        # left = Item.objects.filter(release__title__contains='Backlog', release__project__id=project_id).order_by('-priority')
        left = Item.objects.filter(release__title__contains='Backlog', release__project__id=project_id)
        left = left.exclude(status=4)
        left = left.exclude(status=5)
        left = left.order_by('-priority')
        context['left'] = left

        # pull "right" - the current projects items
        # right = Item.objects.filter(release_id=context['release'].id).order_by('-priority')
        right = Item.objects.filter(release_id=context['release'].id)
        right = right.exclude(status=4)
        right = right.exclude(status=5)
        right = right.order_by('-priority')
        context['right'] = right

        return context


class ReleaseQuickAdd(CreateView):

    form_class = forms.ReleaseQuickForm
    template_name = 'release_quick.html'
    # success_url = '/projects/'

    def get_context_data(self, **kwargs):
        context = super(ReleaseQuickAdd, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')

        release = Release.objects.get(pk=release_id)

        context['project_id'] = project_id
        context['release_id'] = release_id
        context['release'] = release

        self.success_url = '/projects/{{project_id}}/releases/{{release_id}}'.replace('{{project_id}}', project_id).replace('{{release_id}}', release_id)

        return context

    def post(self, request, *args, **kwargs):

        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')

        # get field value
        quick_items = self.request.POST['quick_items']

        for line in iter(quick_items.splitlines()):
            value_result = ''
            if "," in line:
                values = line.split(',')
                for value in values[1:]:
                    value_result += value + ','
            else:
                values[0] = line

            value_result = value_result[0:-1]

            new_item = Item.objects.create(
                release_id=release_id,
                title=values[0],
                detail=value_result,
                date_started=None,
                date_completed=None,
            )
            new_item.save()

        self.success_url = '/projects/' + project_id + '/releases/' + release_id

        # parse field value creating an item for each (may not have a description, may only be a title
        return HttpResponseRedirect(self.success_url)


class ReleaseCreate(CreateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'
    template_name='release_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseCreate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_id'] = project_id
        self.success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return context

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        self.success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return super(ReleaseCreate, self).post(self, request, *args, **kwargs)


class ReleaseUpdate(UpdateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'
    template_name = 'release_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseUpdate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_id'] = project_id
        return context

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')
        self.success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
        return super(ReleaseUpdate, self).post(self, request, *args, **kwargs)


class ReleaseDelete(DeleteView):

    model = Release
    form_class = forms.ReleaseForm
    template_name='release_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseDelete, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_id'] = project_id

        if 'backlog' in context['release'].title.lower():
            context['error'] = True
        else:
            context['error'] = False

        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return success_url


#
#   Items
#


class ItemIndex(ListView):
    model = Item
    template_name = 'item_index.html'


class ItemDetail(DetailView):

    model = Item
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        item_id = self.kwargs.get('pk')
        context['project_id'] = project_id
        context['release_id'] = release_id

        comments = ItemComments.objects.filter(item_id=item_id)

        context['comments'] = comments

        return context


class ItemCreate(CreateView):

    model = Item
    template_name = 'item_edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    def get_context_data(self, **kwargs):
        context = super(ItemCreate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        context['project_id'] = project_id
        context['release_id'] = release_id
        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')

        if 'submit_and_add' in self.get_form_kwargs().get('data'):
            self.success_url = '/projects/project_id/releases/release_id/items/create/'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url
        else:
            self.success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url


class ItemUpdate(UpdateView):

    model = Item
    template_name = 'item_edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')

        if 'submit_and_add' in self.get_form_kwargs().get('data'):
            self.success_url = '/projects/project_id/releases/release_id/items/create/'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url
        else:
            self.success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        context['project_id'] = project_id
        context['release_id'] = release_id
        return context



'''
def item_delete(request, pk):
    Item.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')
'''


class ItemDelete(DeleteView):

    model = Item
    form_class = forms.ItemForm
    template_name = 'item_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDelete, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        item_id = self.kwargs.get('pk')
        context['project_id'] = project_id
        context['release_id'] = release_id
        context['item_id'] = item_id
        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
        return success_url


# ajax "views"
#
def release_quick_add_ajax(request, release_id, item_id):

    # perform update
    curr_item = Item.objects.get(id=item_id)
    curr_item.release_id = release_id
    curr_item.save()

    # get item title and release title
    item_title = Item.objects.get(id=item_id).title
    release_title = Release.objects.get(id=release_id).title

    return_val = 'Moved Item: [<b>item_title</b>] to Release: [<b>release_title</b>]'.replace('item_title', item_title).replace('release_title', release_title)

    return HttpResponse(content=return_val)


def item_start(request, item_id):

    # perform update
    curr_item = Item.objects.get(id=item_id)
    d = datetime.now()
    curr_item.date_started, date_started = d, d.strftime('%b DAY, %Y, HOUR:%M%p')
    curr_item.save()

    # item_title = curr_item.title
    day = d.strftime('%d')
    if day[0] == '0':
        day = day[1:]

    hour = d.strftime('%I')
    if hour[0] == '0':
        hour = hour[1:]

    date_started = date_started.replace('DAY', day)
    date_started = date_started.replace('HOUR', hour)
    return_val = date_started.replace('AM', ' a.m.').replace('PM', ' p.m.')

    return HttpResponse(content=return_val)


from models import Item


def item_complete_action(request, item_id, action=True):

    # perform update
    curr_item = Item.objects.get(id=item_id)
    d = datetime.now()
    curr_item.date_completed = d
    if action:
        curr_item.status = Item.CLOSED_ACTION
    else:
        curr_item.status = Item.CLOSED_NO_ACTION
    curr_item.status
    curr_item.save()

    # item_title = curr_item.title
    day = d.strftime('%d')
    if day[0] == '0':
        day = day[1:]

    hour = d.strftime('%I')
    if hour[0] == '0':
        hour = hour[1:]

    date_completed = d.strftime('%b DAY, %Y, HOUR:%M%p')
    date_completed = date_completed.replace('DAY', day)
    date_completed = date_completed.replace('HOUR', hour)
    return_val = date_completed.replace('AM', ' a.m.').replace('PM', ' p.m.')

    return HttpResponse(content=return_val)


def item_complete_no_action(request, item_id, action=False):
    return item_complete_action(request, item_id, action)


def item_add_comment(request, item_id):

    # add comment

    # raise DebugMessage(request.POST)

    comment_text = request.POST['comment_text']
    new_comment = ItemComments(item_id=item_id, comment=comment_text)
    new_comment.save()

    # templates for return value
    comments_template = '''
    <div class="panel-heading font-size-18">Comments</div>
        {{comments}}
    <div class="list-group-item">
        <textarea id="comment_text" class="textarea-full-width" rows="6"></textarea><br><br>
        <button class="btn btn-success margin-btm-5" onclick="trigger_add_comment('{{item_id}}')">Add Comment</button>
    </div>
    '''
    comments_template = comments_template.replace('{{item_id}}', item_id)
    comment_template = '''
        <div class="list-group-item">
            <span class="subtitle">{{comment_time}}</span><br>
            {{comment}}
        </div>
    '''

    # build return value
    comments = ItemComments.objects.filter(item_id=item_id)
    comments_return = ''
    for row in comments:
        comment_tmp = comment_template.replace('{{comment}}', row.comment)
        comment_tmp = comment_tmp.replace('{{comment_time}}', get_formatted_date_time(row.date_created))
        comments_return += comment_tmp

    return_val = comments_template.replace('{{comments}}', comments_return)

    return HttpResponse(content=return_val)


# details


def check_project_reporting(project_id):

    days = number_of_days_to_chart

    z = ''
    # go through last N days
    for i in range(days, 0, -1):

        d = datetime.now().date()
        d = d - timedelta(days=i)

        data = ItemLog.objects.filter(day=d, project_id=project_id)

        if not data:
            # no data for this day, generate data for the day
            ed = d + timedelta(days=1)

            # total_items = Item.objects.filter(release__project__id=project_id).count()
            total_open_query = 'SELECT project_id_id as id, count(*) as total FROM projects_item as i ' \
                               'INNER JOIN projects_release as r ON r.id = i.release_id_id ' \
                               'WHERE project_id_id = "{project_id}" and i.date_created < "{ED}" and (i.date_completed > "{D}" or i.date_completed is null)'
            total_open_query = total_open_query.replace('{ED}', ed.strftime("%Y-%m-%d %H:%M:%S"))
            total_open_query = total_open_query.replace('{D}', d.strftime("%Y-%m-%d %H:%M:%S"))
            total_open_query = total_open_query.replace('{project_id}', project_id)

            total_open = Item.objects.raw(total_open_query)[0]

            total_closed_query = 'SELECT project_id_id as id, count(*) as total FROM projects_item as i ' \
                                 'INNER JOIN projects_release as r ON r.id = i.release_id_id ' \
                                 'WHERE project_id_id = "{project_id}" and i.date_created < "{ED}" and i.date_completed < "{D}"'
            total_closed_query = total_closed_query.replace('{ED}', ed.strftime("%Y-%m-%d %H:%M:%S"))
            total_closed_query = total_closed_query.replace('{D}', d.strftime("%Y-%m-%d %H:%M:%S"))
            total_closed_query = total_closed_query.replace('{project_id}', project_id)

            total_closed = Item.objects.raw(total_closed_query)[0]

            new_log_entry = ItemLog(
                project_id=project_id,
                day=d,
                total_open=total_open.total,
                total_closed=total_closed.total,
            )

            new_log_entry.save()


def get_formatted_date_time(d):

    day = d.strftime('%d')
    if day[0] == '0':
        day = day[1:]

    hour = d.strftime('%I')
    if hour[0] == '0':
        hour = hour[1:]

    return_val = d.strftime('%b DAY, %Y, HOUR:%M%p')
    return_val = return_val.replace('DAY', day)
    return_val = return_val.replace('HOUR', hour)
    return_val = return_val.replace('AM', ' a.m.').replace('PM', ' p.m.')

    return return_val


def get_chart(request, project_id, chart_id):

    data = {}
    data['project_id'] = project_id
    return_val = get_ajax_chart(chart_id, data)
    return HttpResponse(content=return_val)


# get_ajax_chart('item_completion', data)
#
def get_ajax_chart(chart, data):

    if chart == 'item_completion':

        template = '''
        <div id="chart" class="chart"></div>
        <script type="text/javascript">
            $(function () {
                $('#chart').highcharts({
                    chart: {
                        type: 'area',
                        showAxes: false,
                    },
                    title: { text: '' },
                    plotOptions: {
                        area: {
                            stacking: 'normal',
                            lineColor: '#fff',
                            lineWidth: 0,
                            marker: { enabled: false, },
                            dataLabels: { enabled: false, },
                        }
                    },
                    yAxis: {
                        title: { text: '' },
                        labels: { enabled: false, },
                        gridLineWidth: 0,
                    },
                    xAxis: {
                        title: { text: '' },
                        labels: { enabled: true, },
                        tickColor: '#fff',
                        categories: [{{date_data}}],
                    },
                    series: [{
                        name: 'Pending Issues',
                        data: [{{open_issues_data}}],
                        color: '#E75F54',
                        showInLegend: false,
                    }, {
                        name: 'Fixed Issues',
                        data: [{{closed_issues_data}}],
                        color: '#336C48',
                        showInLegend: false,
                    }]
                });
            });
        </script>
        '''

        returned_data = draw_item_completion_chart(data['project_id'], get_item_logs(data['project_id']))

        template = template.replace('{{open_issues_data}}', returned_data['open_issues_data'])
        template = template.replace('{{closed_issues_data}}', returned_data['closed_issues_data'])
        template = template.replace('{{date_data}}', returned_data['date_data'])

        return template

    elif chart == 'burndown':

        template = '''
        <div id="chart" class="chart"></div>
        <script type="text/javascript">
            $(function () {
                $('#chart').highcharts({
                    chart: {
                        type: 'line',
                        // showAxes: false,
                    },
                    title: { text: '' },
                    plotOptions: {
                        line: {
                            dataLabels: { enabled: false },
                            enableMouseTracking: false,
                        }
                    },
                    yAxis: {
                        title: { text: '' },
                        labels: { enabled: false, },
                        floor: 0,
                        gridLineWidth: 0,
                    },
                    xAxis: {
                        title: { text: '' },
                        labels: { enabled: true, },
                        tickColor: '#fff',
                        floor: 0,
                        // categories: [{{date_data|safe}}],
                    },
                    series: [{
                        name: 'Open Issues',
                        data: [987, 610, 377, 233, 144, 89, 55, 34, 21, 13, 8, 5, 3, 2, 1, 1, 0],
                        // data: [{{open_issues_data}}],
                        color: '#336C48',
                        showInLegend: false,
                    }, {
                        type: 'line',
                        name: ' ',
                        showInLegend: false,
                        data: [[0, 987], [16, 0]],
                        // data: [[{{trend_line_start}}], [{{trend_line_end}}]]
                        marker: {
                            enabled: false
                        },
                        states: {
                            hover: {
                                lineWidth: 0
                            }
                        },
                        enableMouseTracking: false
                    }]
                });
            });
        </script>
        '''


        # return template
        return '<b>[burndown chart here]</b>'

    return '<b>Nothing yet, may have new charts coming later.</b>'


def item_complete_action(request, item_id, action=True):

    # perform update
    curr_item = Item.objects.get(id=item_id)
    d = datetime.now()
    curr_item.date_completed = d
    if action:
        curr_item.status = Item.CLOSED_ACTION
    else:
        curr_item.status = Item.CLOSED_NO_ACTION
    curr_item.status
    curr_item.save()

    # item_title = curr_item.title
    day = d.strftime('%d')
    if day[0] == '0':
        day = day[1:]

    hour = d.strftime('%I')
    if hour[0] == '0':
        hour = hour[1:]

    date_completed = d.strftime('%b DAY, %Y, HOUR:%M%p')
    date_completed = date_completed.replace('DAY', day)
    date_completed = date_completed.replace('HOUR', hour)
    return_val = date_completed.replace('AM', ' a.m.').replace('PM', ' p.m.')

    return HttpResponse(content=return_val)

