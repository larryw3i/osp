#!/usr/bin/bash

# tree -L 2 # my tree
# .
# ├── fun
# │   ├── db.sqlite3
# │   ├── eduhub
# │   ├── fun
# │   ├── funauth
# │   ├── fundeveloper
# │   ├── funfile
# │   ├── funhome
# │   ├── funlog
# │   ├── funmiddleware
# │   ├── funuser
# │   ├── locale
# │   └── manage.py
# ├── fun.sh
# ├── LICENSE
# ├── README.md
# ├── requirements
# │   ├── dev.txt
# │   └── produc.txt
# ├── setup.py
# └── venv
#     ├── bin
#     ├── lib
#     └── pyvenv.cfg
#


_args=("$@") # all parameters from terminal.

activate_source(){
    if [[ -x "$(which virtualenv)" ]]; then
        [[ -f "./venv/bin/activate" ]] || virtualenv venv
        source ./venv/bin/activate
    else
        echo "virtualenv doesn't exist, please install it" && exit
    fi
}

p8(){
    activate_source
    isort -v ./fun/
    autopep8 -i -a -a -r -v ./fun/
}

pi(){
    activate_source
    pip3 install $( cat requirements/*.txt | grep -v "#" )
}


init(){
    activate_source;    pi;
    [[ -x "$(which yarn)" ]] && cd ./fun/funhome/static && \
    yarn install && cd ../../..

    [[ -d "./fun/funlog" ]] || mkdir ./fun/funlog
    [[ -f "./fun/funlog/django_fun.log" ]] || touch ./fun/funlog/django_fun.log

    [[ -d "./funfile/files" ]] || mkdir -p ./fun/funfile/files
    
    [[ -f "./fun/fun/settings.py" ]] || \
    cp ./fun/fun/settings_.py ./fun/fun/settings.py
    
    python3 ./fun/manage.py makemigrations
    python3 ./fun/manage.py migrate    
    python3 ./fun/manage.py compilemessages

    read -p "Create superuser?(y/N)" _createsuperuser
    [[  "Yy" == *"${_createsuperuser}"* ]] && \
    python3 ./fun/manage.py createsuperuser

    python3 ./fun/manage.py runserver
    echo "Done."
}

update_gitignore(){
    git rm -r --cached . && git add .
    read -p "commit now?(y/N)" commit_now
    [[ "Yy" == *"$commit_now"* ]] && git commit -m 'update .gitignore'
    echo "gitignore updated!"
}

_msgfmt(){
    for _po in $(find ./fun/locale -name "*.po"); do
        echo -e "$_po ${_po/.po/.mo}"
        msgfmt -v -o ${_po/.po/.mo}  $_po
    done
}

_start(){
    activate_source
    cd ./fun
    cd ./funstatic/static

    if [[ -x "$(which yarn)" ]]; then
        yarn
        cd ../..
    else
        echo "yarn doesn't exist, please install it"
        cd ../../..
        exit
    fi

    python3 ./manage.py migrate
    python3 ./manage.py runserver
    cd ..
}

ug(){       update_gitignore;   }
_s(){       _start;             }
gita(){     p8; git add . ;     }

as(){       activate_source;    }
_msg(){     _msgfmt;            }


${_args[0]}