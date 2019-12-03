.. _buildingTools:

Building Modules and Tools on OSC
=================================

There are several ways of using tools on OSC.

1. Directly

2. As modules

3. As singularity containers

Each has advantages/disadvantages (depends on if it's user *or* developer as well!), but, in general, these are ordered
according to universality.

We'll go through each method in some detail (enough to get you started/going), but we'll leave detailed descrption and
advanced use to their respective documentations.

For this section we'll use SPAdes, a common metagenomic assembler, as our example.

Let's download it first, so we all start at the same place:

.. code-block:: bash

    $ wget http://cab.spbu.ru/files/release3.13.2/SPAdes-3.13.2-Linux.tar.gz

And unpack it

.. code-block:: bash

    # Untar
    $ tar xf SPAdes-3.13.2-Linux.tar.gz
    # Check to see it decompressed
    $ ls
    SPAdes-3.13.2-Linux.tar.gz SPAdes-3.13.2-Linux

And check the files in our new SPAdes directory...

.. code-block:: bash

    $ ls SPAdes-3.13.2-Linux
    bin	share
    $ ls -l SPAdes-3.13.2-Linux/bin
    metaspades.py -> spades.py
    plasmidspades.py -> spades.py
    rnaspades.py -> spades.py
    spades-bwa
    spades-core
    spades-corrector-core
    spades-gbuilder
    spades-gmapper
    spades-hammer
    spades-ionhammer
    spades-kmercount
    spades-truseq-scfcorrection
    spades.py
    spades_init.py
    truspades.py

Now, for the 3 methods.

Directly
--------

The simplest way to load and/or run a tool.

.. code-block:: bash

    # Full path
    /fs/project/PAS1117/modules/spades/3.13.2/bin/spades.py --version
    SPAdes v3.13.2
    # Within the directory
    cd /fs/project/PAS1117/modules/spades/3.13.2/bin/
    ./spades.py --version
    SPAdes v3.13.2

SPAdes is a python program that can run on python 2+. Since python is already installed on OSC, there's no need to load
anything. You can simply put the *full path* to spades.py or use ./spades.py and you're good to go. If you wanted to
share this with a co-worker, you would need to send them the full path *and* ensure the folder SPAdes resides in
(/fs/project/PAS1117/...) is also readable for them. They'd need to use the full path and/or use ./ as we did earlier.
In this example, **only** people in PAS1117 can use this. Bummer.

Modules
-------

*However*, what if you didn't want to write the full path or change to the directory in order to use the tool? Normally,
you'd add this to your system's $PATH variable so when you typed "spades.py" it'd know *exactly* where to find your
tool.

.. code-block:: bash

    export PATH=$PWD/SPAdes-3.13.2-Linux/bin:$PATH

Now you can run SPAdes without worrying about where it's located!

.. code-block:: bash

    spades.py --version
    SPAdes v3.13.2

What OSC's module system does is let's you easily modify you paths and other variables, and provide a convenient way of
allowing others to do the same. All that's required is a single file with that information - a lua file.

.. code-block:: bash

    -- Local Variables
    local name = "spades"
    local version = "3.13.2"

    -- Locate Home Directory
    local projectDir = "/fs/project/PAS1117/"
    local root = pathJoin(projectDir, "modules", name, version)

    -- Set Paths
    prepend_path("PATH", pathJoin(root, "bin"))

What's happening? There's only 1 thing that's happening, "prepend_path" is adding a folder/directory path to your $PATH.
It's joining the "root" variable (we'll get there in a second) and "bin" directory together to form 1, complete path,
and then adding that path/folder to the system's $PATH variable, so it knows to look in that folder for your tools.

How is that "root" directory made? Look at "local root". It's joining the "projectDir" to "modules", and then adding the
"name" and "version" variables. Think of it like this:

root = projectDir + "modules" + name + version

root = "/fs/project/PAS1117/" + "modules" + "spades" + "3.13.2"

So that's root, now we need PATH.

PATH = root + "bin"

PATH = "/fs/project/PAS1117/" + "modules" + "spades" + "3.13.2" + "bin"

PATH = "/fs/project/PAS1117/modules/spades/3.13.2/bin"

and if you remember the SPAdes path earlier:

/fs/project/PAS1117/modules/spades/3.13.2/bin/spades.py

What a coincidence. PATH = the full path to the spades.py directory.

So that's great, how to I use this LUA file?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OSC has a great `howto site <https://www.osc.edu/resources/getting_started/howto/howto_locally_installing_software>`_,
and is more detailed than here. But let's summarize what they say.

Save your LUA files, also known as *modulefiles* in some directory, like "lmodfiles". Save all your tools and stuff in
"local". This example also uses your home directory ($HOME), and everything is assumed to be installed there. They
[OSC] recommends the following file structure:

.. code-block:: bash

    local
    |-- src
    |-- share
        `-- lmodfiles

In our example, above, it'd look like this for us:

.. code-block:: bash

    local
    |-- src
        | -- SPAdes-3.13.2-Linux.tar.gz
    |-- spades
        | -- SPAdes-3.13.2-Linux
    |-- share
        | -- lmodfiles
            | -- spades
                -- 3.13.2.lua

Notice how both tarfile and extracted folders/files are in different directories. Now, to load the module:

.. code-block:: bash

    module use local/share/lmodfiles/
    module load spades/3.13.2

You *must* **module use** and **module load** every time you log into OSC and in every job script (if you are loading
a module).

In the Sullivan lab, we use a nigh identical scheme, except that "lmodfiles" is "modulefiles" for greater clarity on
what the folder is storing vs what system it's actually running.

Singularity
-----------

Forthcoming!