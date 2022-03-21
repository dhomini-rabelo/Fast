<h1>Fast Project</h1>

<h2>About</h2>

<p>Python package for better development process with Django using command line. The commands folder is a django app with commands of project, Fast folder have utils functions for fast development with Django</p>

<h2>How to start Django project with Fast Project</h2>

<ol>

<li>
<h3>Start virtual environment and Django project</h3>

```
python -m venv venv
```

```
venv/Scripts/Activate.ps1 # if PowerShell
```

```
pip install django
```

```
mkdir project
```

```
cd project
```

```
django-admin startproject MY_PROJECT_NAME .
```

</li><br>

<li>
<h3>Copy folders and files of project folder from this project and paste in your project folder, download <a href="./project.rar" type="application/rar" download="project.rar">here</a></h3>
</li><br>

<li>
<h3>Download requirements.txt and update requirements.txt</h3>

```
pip install -r requirements.txt
```

```
pip freeze > requirements.txt
```

</li><br>

<li>
<h3>Add project name and commands app in settings.py</h3>

```
# settings.py

PROJECT_NAME = 'MY_PROJECT_NAME'

INSTALLED_APPS = [
    ...,
    'commands.CommandsConfig',
]
```

</li><br>

<li>
<h3>Create project structure</h3>

```
python manage.py fast-init --del
```

</li><br>

</li><br>

<li>
<h3>Create custom user</h3>

```
python manage.py create-accounts-app
```

</li><br>

<li>
<h3>Edit user model and user admin</h3>
</li><br>

<li>
<h3>Do the migrations</h3>

```
python manage.py makemigrations
```

```
python manage.py migrate
```

</li><br>


</ol>


<h2>Commands</h2>

<ul>

<li>
<h3>fast-init [--del, -d]</h3>
<p>--del, -d  -> For delete default commentaries</p>
<p>Command for create project structure and configure project</p>
</li><br>

<li>
<h3>create-fast-app [app_name]</h3>
<p>Command for create fast app in backend folder</p>
</li><br>

<li>
<h3>create-accounts-app</h3>
<p>Command for create fast app with custom user</p>
</li><br>


<li>
<h3>register admin [model_address]</h3>
<p>model_address -> app_name.model_name</p>
<p>Command for create base for register admin model</p>
</li><br>

<li>
<h3>minificate-css</h3>
</li><br>

<li>
<h3>minificate-html</h3>
</li><br>

<li>
<h3>minificate-js</h3>
</li><br>


</ul>