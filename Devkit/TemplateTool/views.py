from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project_record
import yaml
import os

frontend = ['Bootstrap', 'Angular', 'HTML_CSS_JavaScript']
backend = ['Django', 'Flask', 'PHP']
database = ['Oracle', 'MySql', 'Postgre', 'Sqlite']


def read_params(config_path=os.path.join(settings.BASE_DIR, 'TemplateTool', 'params.yaml')):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def index(request):
    return render(request=request,
                  template_name="Index.html",
                  context={})

@login_required(login_url='/Login')
def logout_view(request):
    logout(request)
    return render(request=request,
                  template_name="index.html",
                  context={})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/Dashboard') #dashboard
        else:
            return HttpResponse("<p> The username or password is incorrect, <a href='/Login'>Return back</a> </p>")
    return render(request=request,
                  template_name="login.html",
                  context={})

def Registration(request, *args, **kwargs):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('secretcode')
        if User.objects.filter(username=email).exists():
            return HttpResponse("<p>User with same email id exists, try with different email id !  <a href='/Register'>Return back</a> </p>")
        else:
            user = User.objects.create_user(username=email,
                                            password=password,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name)
            user.save()

        if user:
            auth_login(request, user)
            return HttpResponseRedirect('/Dashboard') #dashboard
    return render(request, 'Registration.html', {})

@login_required(login_url='/Login')
def dashboard(request):
    Project_record_obj = Project_record.objects.filter(user=request.user)
    return render(request=request,
                  template_name="dashboard.html",
                  context={'Project_record_obj':Project_record_obj})

def webapptool(request):
    if request.method == 'POST':
        Project_name = request.POST.get('project_name')
        selected_frontend = frontend[int(request.POST.get('fd'))-1]
        selected_backend = backend[int(request.POST.get('bd')) - 1]
        selected_database = database[int(request.POST.get('db')) - 1]


        Project_record_obj = Project_record.objects.create(user=request.user,
                                                            project_name =Project_name,
                                                            selected_frontend =selected_frontend,
                                                            selected_backend =selected_backend,
                                                            selected_database =selected_database,)
        Project_record_obj.save()
        config = read_params()
        params_file_loc = os.path.join(config['user_project_records'], Project_name+'_'+str(Project_record_obj.id)+'.yaml')
        data={
            "project_name":Project_name,
            "selected_frontend":selected_frontend,
            "selected_backend": selected_backend,
            "selected_database": selected_database
        }
        with open(params_file_loc, 'w') as f:
            yaml.dump(data, f)
        Project_record_obj.yaml_file = params_file_loc
        Project_record_obj.save()
        print(selected_frontend, selected_backend, selected_database, Project_name)
        return HttpResponseRedirect('webapp/'+str(Project_record_obj.id))
    return render(request=request,
                  template_name="webapptool.html",
                  context={})

def record_nav_bar(request ,project_id):
    Project_record_obj = Project_record.objects.filter(user=request.user, pk=project_id)[0]
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']
    nav_bar_options = config_file['nav'][selected_frontend]
    print(nav_bar_options)
    if request.method == 'POST':
        selected_nav_bar = int(request.POST.get('nav_id'))
        if selected_nav_bar:
            project_config_file['selected_nav_bar']=selected_nav_bar
        else:
            project_config_file['selected_nav_bar']=False
        with open(yamlfile_address, 'w') as yaml_file:
            yaml_file.write(yaml.dump(project_config_file, default_flow_style=False))
        return HttpResponseRedirect(str(Project_record_obj.id)+'/footer')
    return render(request=request,
                  template_name="web_nav_bar_selection.html",
                  context={"nav_bar_options": nav_bar_options})

def record_footer(request ,project_id):
    Project_record_obj = Project_record.objects.filter(user=request.user, pk=project_id)[0]
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']
    footer_options = config_file['footer'][selected_frontend]
    print(footer_options)
    if request.method == 'POST':
        selected_footer = int(request.POST.get('footer_id'))
        if selected_footer:
            project_config_file['selected_footer']=selected_footer
        else:
            project_config_file['selected_footer']=False
        with open(yamlfile_address, 'w') as yaml_file:
            yaml_file.write(yaml.dump(project_config_file, default_flow_style=False))
        return HttpResponseRedirect('/webapp/'+str(Project_record_obj.id) + '/loginform')
    return render(request=request,
                  template_name="web_footer_selection.html",
                  context={"footer_options": footer_options})

def record_loginform(request ,project_id):
    Project_record_obj = Project_record.objects.filter(user=request.user, pk=project_id)[0]
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']
    loginform_options = config_file['Login'][selected_frontend]
    print(loginform_options)
    if request.method == 'POST':
        selected_loginform = int(request.POST.get('loginform_id'))
        if selected_loginform:
            project_config_file['selected_loginform']=selected_loginform
        else:
            project_config_file['selected_loginform']=False
        with open(yamlfile_address, 'w') as yaml_file:
            yaml_file.write(yaml.dump(project_config_file, default_flow_style=False))
        return HttpResponseRedirect('/webapp/'+str(Project_record_obj.id) + '/signupform')
    return render(request=request,
                  template_name="web_loginform_selection.html",
                  context={"loginform_options": loginform_options})

def record_signupform(request ,project_id):
    Project_record_obj = Project_record.objects.filter(user=request.user, pk=project_id)[0]
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']
    signupform_options = config_file['Signup'][selected_frontend]
    print(signupform_options)
    if request.method == 'POST':
        selected_signupform = int(request.POST.get('signupform_id'))
        if selected_signupform:
            project_config_file['selected_signupform']=selected_signupform
        else:
            project_config_file['selected_signupform']=False
        with open(yamlfile_address, 'w') as yaml_file:
            yaml_file.write(yaml.dump(project_config_file, default_flow_style=False))
        return HttpResponseRedirect('/webapp/'+str(Project_record_obj.id) + '/otherdetails')
    return render(request=request,
                  template_name="web_signupform_selection.html",
                  context={"signupform_options": signupform_options})

def other_details(request ,project_id):
    Project_record_obj = Project_record.objects.filter(user=request.user, pk=project_id)[0]
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    if request.method == 'POST':
        bg_color = request.POST.get('bg_color')
        Home_page_heading = request.POST.get('Home_page_heading')
        Home_page_text = request.POST.get('Home_page_text')
        print(bg_color, Home_page_heading, Home_page_text)
        project_config_file['bg_color'] = bg_color
        project_config_file['Home_page_heading'] = Home_page_heading
        project_config_file['Home_page_text'] = Home_page_text
        with open(yamlfile_address, 'w') as yaml_file:
            yaml_file.write(yaml.dump(project_config_file, default_flow_style=False))

        selected_backend = project_config_file['selected_backend']
        if selected_backend == "Django":
            Create_Django_APP(project_id)
        if selected_backend == "Flask":
            Create_Flask_APP(project_id)
        if selected_backend == "PHP":
            Create_PHP_APP(project_id)
        return HttpResponseRedirect('/download_template')

    return render(request=request,
                  template_name="web_other_details_selection.html",
                  context={})

import shutil
import bs4
from bs4 import BeautifulSoup
def write_html_files(nav_path, footer_path, other, custom_file_template_path, project_config_file):
    nav = open(os.path.join(settings.BASE_DIR, 'templates', nav_path))
    nav = nav.read()
    nav = bs4.BeautifulSoup(nav)
    nav.h4.string = project_config_file['project_name']
    footer = open(os.path.join(settings.BASE_DIR, 'templates', footer_path))
    footer = footer.read()
    footer = bs4.BeautifulSoup(footer)
    with open(custom_file_template_path) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)
    #changing template color accoring to user's input
    soup.body['style'] = "background-color: {};".format(project_config_file['bg_color'])
    #changing color end here
    soup.body.nav.append(nav)
    if other:
        soup.body.append(other)
        if project_config_file['selected_backend'] == "Django":
            soup.body.form.append('{% csrf_token %}')
    else:
        if project_config_file['selected_backend'] == "Django":
            content = """
                        {% if user.is_authenticated %}
                        Hi, {{request.user.first_name|title}}{{request.user.last_name|title}}
                        {% else %}
                        <br>
                        <a href="/Register" class="btn-get-started scrollto">Get Started</a> <br>
                        <a href="/Login" class="glightbox btn-watch-video"><i class="bi bi-play-circle"></i><span>Already have an account?</span></a>
                        {% endif %}<br><br>
                        """
            soup.body.h1.append(BeautifulSoup(content))
        if project_config_file['selected_backend'] == "Flask":
            content = """"""
            soup.body.h1.append(BeautifulSoup(content))

        if project_config_file['selected_backend'] == "PHP":
            content = """"""
            soup.body.h1.append(BeautifulSoup(content))

        soup.body.h1.append(project_config_file['Home_page_heading'])
        soup.body.p.append(project_config_file['Home_page_text'])
    soup.body.footer.append(footer)

    with open(custom_file_template_path, "w") as outf:
        outf.write(str(soup))

def generate_frontend_layout(custom_template_path, selected_frontend, project_config_file, config_file):
    custom_template_path = os.path.join(custom_template_path, 'application', 'templates')
    print("custom_template_path", custom_template_path)
    if selected_frontend == 'Bootstrap':
        basic_template = config_file['basic']['Bootstrap']
        custom_home_template_path = os.path.join(custom_template_path, 'index.html')
        custom_login_template_path = os.path.join(custom_template_path, 'login.html')
        custom_signup_template_path = os.path.join(custom_template_path, 'signup.html')
        shutil.copy(basic_template, custom_home_template_path)
        shutil.copy(basic_template, custom_login_template_path)
        shutil.copy(basic_template, custom_signup_template_path)

        nav_path = config_file['nav']['Bootstrap'][project_config_file['selected_nav_bar']]
        footer_path = config_file['footer']['Bootstrap'][project_config_file['selected_footer']]
        login_form_path = config_file['Login']['Bootstrap'][project_config_file['selected_loginform']]
        signup_form_path = config_file['Signup']['Bootstrap'][project_config_file['selected_signupform']]

        login_form = open(os.path.join(settings.BASE_DIR, 'templates', login_form_path))
        login_form = login_form.read()
        login_form = bs4.BeautifulSoup(login_form)
        signup_form = open(os.path.join(settings.BASE_DIR, 'templates', signup_form_path))
        signup_form = signup_form.read()
        signup_form = bs4.BeautifulSoup(signup_form)

        write_html_files(nav_path, footer_path, False, custom_home_template_path, project_config_file)
        write_html_files(nav_path, footer_path, login_form, custom_login_template_path, project_config_file)
        write_html_files(nav_path, footer_path, signup_form, custom_signup_template_path, project_config_file)

    if selected_frontend == 'Angular':
        basic_template = config_file['basic']['Angular']

    if selected_frontend == 'HTML_CSS_JavaScript':
        basic_template = config_file['basic']['HTML_CSS_JavaScript']
        custom_home_template_path = os.path.join(custom_template_path, 'index.html')
        custom_login_template_path = os.path.join(custom_template_path, 'login.html')
        custom_signup_template_path = os.path.join(custom_template_path, 'signup.html')
        shutil.copy(basic_template, custom_home_template_path)
        shutil.copy(basic_template, custom_login_template_path)
        shutil.copy(basic_template, custom_signup_template_path)

        nav_path = config_file['nav']['HTML_CSS_JavaScript'][project_config_file['selected_nav_bar']]
        footer_path = config_file['footer']['HTML_CSS_JavaScript'][project_config_file['selected_footer']]
        login_form_path = config_file['Login']['HTML_CSS_JavaScript'][project_config_file['selected_loginform']]
        signup_form_path = config_file['Signup']['HTML_CSS_JavaScript'][project_config_file['selected_signupform']]

        login_form = open(os.path.join(settings.BASE_DIR, 'templates', login_form_path))
        login_form = login_form.read()
        login_form = bs4.BeautifulSoup(login_form)
        signup_form = open(os.path.join(settings.BASE_DIR, 'templates', signup_form_path))
        signup_form = signup_form.read()
        signup_form = bs4.BeautifulSoup(signup_form)

        write_html_files(nav_path, footer_path, False, custom_home_template_path, project_config_file)
        write_html_files(nav_path, footer_path, login_form, custom_login_template_path, project_config_file)
        write_html_files(nav_path, footer_path, signup_form, custom_signup_template_path, project_config_file)
    return

def config_database_django(custom_template_path, project_config_file):
    custom_template_setting_file_path = os.path.join(custom_template_path,'application', 'application', 'settings.py')
    readme_file_path = os.path.join(custom_template_path,'application', 'Readme.md')
    readme_content = ""
    selected_database = project_config_file['selected_database']
    if selected_database == "Sqlite":
        database_engine = "DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3',}}"
    if selected_database == "MySql":
        database_engine = "DATABASES = {'default': { 'ENGINE': 'django.db.backends.mysql', 'OPTIONS': { 'read_default_file': BASE_DIR / 'my.cnf',},}}"
        db_confg_path = str(os.path.join(custom_template_path, 'application', 'my.cnf'))
        with open(db_confg_path, 'w') as f:
            data = "[client]\ndatabase = NAME\nuser = USER\npassword = PASSWORD\ndefault-character-set = utf8"
            f.write(data)
        readme_content = "Please Update My Sql Database Details in [my.cnf] file\n" \
                         + "Update: database, user, password in my.cnf file\n" + \
                         "my.cnf file path Main_folder > application > mycnf\n"
    if selected_database == "Postgre":
        database_engine = "DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2','NAME': 'dbname','USER': 'postgres','PASSWORD': '1234','HOST': '127.0.0.1','PORT': '5432',}}"
        readme_content = "Please Update postgreSQL Database Details in [settings.py] file\n" \
                        + "Update: Databasename, User, password, host, port\n" \
                        + "Main_folder>application>application>settings.py\n" \
                        + "At end of settings.py DATABASES Dictionary is present modify and save\n"
    if selected_database == "Oracle":
        database_engine = "DATABASES = {'default': {'ENGINE': 'django.db.backends.oracle','NAME': 'xe','USER': 'a_user','PASSWORD': 'a_password','HOST': '','PORT': '',}}"
        readme_content = "Please Update Oracle Database Details in [settings.py] file\n" \
                         + "Update: Databasename, User, password, host, port\n" \
                         + "Main_folder>application>application>settings.py\n" \
                         + "At end of settings.py DATABASES Dictionary is present modify and save\n"
    with open(custom_template_setting_file_path, "a") as f:
        f.write("\n"+database_engine)
    with open(readme_file_path, "a") as f:
        f.write(readme_content)


def write_html_files_php(nav_path, footer_path, other, custom_file_template_path, project_config_file):
    nav = open(os.path.join(settings.BASE_DIR, 'templates', nav_path))
    nav = nav.read()
    nav = bs4.BeautifulSoup(nav)
    nav.h4.string = project_config_file['project_name']
    footer = open(os.path.join(settings.BASE_DIR, 'templates', footer_path))
    footer = footer.read()
    footer = bs4.BeautifulSoup(footer)
    with open(custom_file_template_path) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt)
    #changing template color accoring to user's input
    soup.body['style'] = "background-color: {};".format(project_config_file['bg_color'])
    #changing color end here
    soup.body.nav.append(nav)
    if other:
        soup.body.append(other)
    else:
        soup.body.h1.append(project_config_file['Home_page_heading'])
        soup.body.p.append(project_config_file['Home_page_text'])
    soup.body.footer.append(footer)

    with open(custom_file_template_path, "w") as outf:
        outf.write(str(soup))

def generate_frontend_layout_php(custom_template_path, selected_frontend, project_config_file, config_file):
    custom_template_path = os.path.join(custom_template_path, 'application', 'templates')
    print("custom_template_path", custom_template_path)
    if selected_frontend == 'Bootstrap':
        basic_template = config_file['basic']['Bootstrap']
        custom_home_template_path = os.path.join(custom_template_path, 'index.html')
        custom_login_template_path = os.path.join(custom_template_path, 'login.html')
        custom_signup_template_path = os.path.join(custom_template_path, 'signup.html')
        shutil.copy(basic_template, custom_home_template_path)
        shutil.copy(basic_template, custom_login_template_path)
        shutil.copy(basic_template, custom_signup_template_path)

        nav_path = config_file['nav']['Bootstrap'][project_config_file['selected_nav_bar']]
        footer_path = config_file['footer']['Bootstrap'][project_config_file['selected_footer']]
        login_form_path = config_file['Login']['Bootstrap'][project_config_file['selected_loginform']]
        signup_form_path = config_file['Signup']['Bootstrap'][project_config_file['selected_signupform']]

        login_form = open(os.path.join(settings.BASE_DIR, 'templates', login_form_path))
        login_form = login_form.read()
        login_form = bs4.BeautifulSoup(login_form)
        signup_form = open(os.path.join(settings.BASE_DIR, 'templates', signup_form_path))
        signup_form = signup_form.read()
        signup_form = bs4.BeautifulSoup(signup_form)

        write_html_files_php(nav_path, footer_path, False, custom_home_template_path, project_config_file)
        write_html_files_php(nav_path, footer_path, login_form, custom_login_template_path, project_config_file)
        write_html_files_php(nav_path, footer_path, signup_form, custom_signup_template_path, project_config_file)

    if selected_frontend == 'Angular':
        basic_template = config_file['basic']['Angular']

    if selected_frontend == 'HTML_CSS_JavaScript':
        basic_template = config_file['basic']['HTML_CSS_JavaScript']
        custom_home_template_path = os.path.join(custom_template_path, 'index.html')
        custom_login_template_path = os.path.join(custom_template_path, 'login.html')
        custom_signup_template_path = os.path.join(custom_template_path, 'signup.html')
        shutil.copy(basic_template, custom_home_template_path)
        shutil.copy(basic_template, custom_login_template_path)
        shutil.copy(basic_template, custom_signup_template_path)

        nav_path = config_file['nav']['HTML_CSS_JavaScript'][project_config_file['selected_nav_bar']]
        footer_path = config_file['footer']['HTML_CSS_JavaScript'][project_config_file['selected_footer']]
        login_form_path = config_file['Login']['HTML_CSS_JavaScript'][project_config_file['selected_loginform']]
        signup_form_path = config_file['Signup']['HTML_CSS_JavaScript'][project_config_file['selected_signupform']]

        login_form = open(os.path.join(settings.BASE_DIR, 'templates', login_form_path))
        login_form = login_form.read()
        login_form = bs4.BeautifulSoup(login_form)
        signup_form = open(os.path.join(settings.BASE_DIR, 'templates', signup_form_path))
        signup_form = signup_form.read()
        signup_form = bs4.BeautifulSoup(signup_form)

        write_html_files_php(nav_path, footer_path, False, custom_home_template_path, project_config_file)
        write_html_files_php(nav_path, footer_path, login_form, custom_login_template_path, project_config_file)
        write_html_files_php(nav_path, footer_path, signup_form, custom_signup_template_path, project_config_file)
    return

def Create_Django_APP(project_id):
    Project_record_obj = Project_record.objects.get(pk=project_id)
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']


    #function to copy backend template structure into User_Custom_APP
    main_django_templete_path = os.path.join(settings.BASE_DIR, 'native_apps_templates', 'django')
    custom_template_path = os.path.join(settings.BASE_DIR, 'native_app_temp')
    shutil.rmtree(custom_template_path)
    shutil.copytree(main_django_templete_path, custom_template_path)

    #function to generate frontend pages according to user selection in User_Custom_APP's template folder
    generate_frontend_layout(custom_template_path, selected_frontend, project_config_file, config_file)

    #funtion to write specific database in User_Custom_APP's config.yaml file
    config_database_django(custom_template_path, project_config_file)
    return


def Create_Flask_APP(project_id):
    Project_record_obj = Project_record.objects.get(pk=project_id)
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']

    # function to copy backend template structure into User_Custom_APP
    main_flask_templete_path = os.path.join(settings.BASE_DIR, 'native_apps_templates', 'flask')
    custom_template_path = os.path.join(settings.BASE_DIR, 'native_app_temp')
    shutil.rmtree(custom_template_path)
    shutil.copytree(main_flask_templete_path, custom_template_path)

    # function to generate frontend pages according to user selection in User_Custom_APP's template folder
    generate_frontend_layout(custom_template_path, selected_frontend, project_config_file, config_file)

    # funtion to write specific database in User_Custom_APP's config.yaml file
    # config_database_django(custom_template_path, project_config_file)

def Create_PHP_APP(project_id):
    Project_record_obj = Project_record.objects.get(pk=project_id)
    yamlfile_address = Project_record_obj.yaml_file
    project_config_file = read_params(config_path=os.path.join(settings.BASE_DIR, yamlfile_address))
    config_file = read_params()
    selected_frontend = project_config_file['selected_frontend']

    # function to copy backend template structure into User_Custom_APP
    main_flask_templete_path = os.path.join(settings.BASE_DIR, 'native_apps_templates', 'PHP')
    custom_template_path = os.path.join(settings.BASE_DIR, 'native_app_temp')
    shutil.rmtree(custom_template_path)
    shutil.copytree(main_flask_templete_path, custom_template_path)
    generate_frontend_layout_php(custom_template_path, selected_frontend, project_config_file, config_file)


import shutil
from django.http import FileResponse
@login_required(login_url='/Login')
def download_template(response):
    dir_name = os.path.join(settings.BASE_DIR, 'native_app_temp')
    output_filename = os.path.join(settings.BASE_DIR, 'Application')
    if os.path.exists(output_filename):
        os.remove(output_filename)
    shutil.make_archive(output_filename, 'zip', dir_name)
    dataset = open(output_filename+'.zip', 'rb')
    response = FileResponse(dataset)
    return response
