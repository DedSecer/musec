cython_opt = -3 --embed

mainfile = musecui.py
cmainfile = $(patsubst %.py, %.c, $(mainfile))
outmainfile= $(patsubst %.c, %, $(cmainfile))

exclude = musecui.py cli.py demo.py
depenfiles = $(filter-out $(exclude), $(wildcard *.py))
cdepenfiles = $(patsubst %.py, %.c, $(depenfiles))
outdepenfiles = $(patsubst %.c, %.so, $(cdepenfiles))

cfiles = $(patsubst %.py, %.c , $(files))
outfiles = $(patsubst %.c, %, $(cfiles))

python = python3.8
python_include=/usr/include/$(python)


%.c: %.py
	cython $(cython_opt) $^ -o $@

%.so: %.c
	gcc `python-config --cflags --ldflags` -fPIC --shared $^ -o ./musecui/$@

all: dir depso musec-ui

dir:
	mkdir -p musecui

depso: $(outdepenfiles)

musec-ui:$(mainfile)
	cython $(cython_opt) $(mainfile) -o $(cmainfile)
	gcc -I$(python_include) -l$(python) $(cmainfile) -o ./musecui/$@
	rm musecui.c
