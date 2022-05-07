
# Table of Contents

1.  [How to Run the Application](#orga8f0c1c)
2.  [How to Use](#orga1ee008)


<a id="orga8f0c1c"></a>

# How to Run the Application

The process of running the application must be done in a
command line interface, specifically, in the terminal
(powershell for windows and bash for linux).

First, we need to create a virtual environment. This is done
by running the following command on windows:

> \> py -3 -m venv venv

or on linux:

> $ python3 -m venv venv

After the creation of the environment, we activate it with
the following command on windows:

> \> venv/Scripts/activate

or on linux:

> $ source venv/bin/activate

The environment can be disabled on both systems (windows and
linux) with the command `deactivate`.

After activating the virtual environment we need to dowload
the dependencies. For that, we use the following command on window:

> \> pip install -e .

or on linux:

> $ pip3 install -e .

Finnaly, we run the script RunDev.ps1 on windows:

> \> .\RunDev.ps1

or rundev.sh on linux:

> $ chmod +x rundev.sh\
> $ ./rundev.sh


<a id="orga1ee008"></a>

# How to Use

Just put the resource (aluno or curso) in the url in
the format:

> <http://localhost:5000/aluno>

for aluno, or:

> <http://localhost:5000/curso>

for curso.

A Bearer token is needed to access all of this routes. This token
is retrieved with the url:

> <http://localhost:5000/login?user=admin&password=admin>

To use the methods `GET`, `PUT` and `DELETE` we need to
indicate the id in the url. For example, the `GET` method
with the url:

> <http://localhost:5000/aluno/5>

will return the resource aluno of id=5.

Also, to use `POST` and `PUT` methods is necessary to
pass a json with the parameters to create or change a
resource. For example, the `PUT` method with the url:

> <http://localhost:5000/curso/2>

and json:

> {\
>   "nome" : "medicina"\
> }

will change the name of the resource curso of id=2
to `"medicina"`.

For Swagger documentation access <http://localhost:5000/apidocs>.

