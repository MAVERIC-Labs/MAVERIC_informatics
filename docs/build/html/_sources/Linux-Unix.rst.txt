.. _UNIX_LINUX:

UNIX/LINUX Introduction and Guide
=================================

There are anthologies to using Unix operating systems. Unix is a family of many different OS's, including Apple's macOS
and Linux distributions (derivatives of unix). We won't cover **any** of the histories or flavors of them here. There's
a lot of "spirited" discussions, and we'd like to avoid all of that.

For the purposes of this guide, we'll be using macOS's Terminal (Finder -> Applications -> Utilities -> Terminal),
`OSC's onDemand <https://ondemand.osc.edu/>`_ shell (Clusters -> Pitzer Shell Access), or a terminal in a flavor of
Linux.

**Final note**: This won't cover every command (not even 1%) available. TThe overall "jist" of this is to quickly get a
new user oriented to OSC and right into doing basic bioinformatics. Sure, there might be some really useful administrator
commands for managing systems, but those aren't really *useful* for beginners who aren't sysadmins. If you're looking for
that here, you've come to the wrong place.

Basic Navigation and Universally Common Commands
------------------------------------------------

When you first login to OSC (via any means), you'll be greeted by a bunch of OSC-related messages, ending with:

.. code-block:: bash

    [userid@pitzer-login01 ~]$

First of all, you've entered into your "home" directory. The **~** is a shortcut for your home (and notice how on the command
line it ends in ~), as is the **$HOME** variable (more on variables later). The rest of the line is basically:

1) who you are (userid)
2) what system you've connected to (pitzer-login01)
3) where you are (~ *or* $HOME)

Now that you know where you are, check out what other files might be in your home directory:

.. code-block:: bash

    $ ls

Before we go any further - I've used the **$** to represent the command line. This is the line that commands are typed on.
It's a quick and easy way to identify which lines were typed and which lines were written back by the system. So for the
above command, "$ ls" means that I've typed "ls". I'm don't 100% conform to this, but for most of the documentation on this
site, I try to keep it as consistent as possible. By the time you get to those points in the guides/documentation, it should
be more or less clear the intention of the instruction.

So type the above, and you should get the following:

.. code-block:: bash

    $ ls
    test_file.txt

There isn't much to look at. Earlier I created a single file, called "test_file.txt". And that's all that's in my home
directory.

The Profile (aliases, environmental variables, $PATH)
-----------------------------------------------------

When you want to run a tool and you don't want to write the full path to that tool every time, i.e.

.. code-block:: bash

    $ /fs/project/PAS1573/bin/bowtie2

the system needs to know where that tool can be found. It doesn't magically know where every tool is located.
**This is where the $PATH variable comes in**. The PATH tells the system where to find its tools. In fact, whenever
you type "ls" or "cat" or "grep" or any *standard* linux tool, the system knows where it is because there are
default directories already present on the system.

You can see where a tool is found by typing:

.. code-block:: bash

    $ which ls
    /usr/bin/ls

The system's PATH variable was set up with several directories, usually /usr/bin, /usr/local/bin, /opt/usr/bin, etc...

What we want to do is ADD to that PATH, so in addition to all the useful, standard linux tools, we can also have our own.

If you try to run the tool without having added it to your $PATH variable...

.. code-block:: bash

    $ bowtie2 --version
    -bash: bowtie2: command not found

But this will work

.. code-block:: bash

    $ /fs/project/PAS1573/bin/bowtie2 --version

What you *can do* is add that PATH to your system:

.. code-block:: bash

    $ export PATH=/fs/project/PAS1573/bin/:$PATH

In this example, you're **extending** your PATH variable, NOT replacing it (more below). You're adding
/fs/project/PAS1573/bin/ to all the other directories in $PATH.

Now you can type:

.. code-block:: bash

    $ bowtie2 --version
    /fs/project/PAS1573/bin/bowtie2-align-s version 2.3.5.1
    ...
    ...

Keeping the $PATH at the end is pretty important...

HOWEVER, if you do this:

.. code-block:: bash

    $ export PATH=/fs/project/PAS1573/bin/

**No programs will work.** You will create a VERY annoying issue on your machine where the system can't find ANYTHING.
No "ls", no "cat", and you won't even be able to edit the file. Every command will end up as "command not found."
*So what happened?* You **replaced** the PATH and basically said, "system, I only want you to look at this directory
for **every** program."

To fix this, you'll need to specify the full path to any tool... or restart your login session.

There are a couple files on OSC (and generally, all linux systems) that control system variables like $PATH where users
can add to or edit. On OSC, these are .bashrc and .bash_profile. They're located in your HOME directory

They might be empty, or might have a few lines of code in them. What we want to do is add to one of them.

.. code-block:: bash

    $ nano .bash_profile

and then add the following:

.. code-block:: bash

    $ export PATH=/fs/project/PAS1573/bin/:$PATH

Look familiar? Now, instead of having to write "export PATH=" every time you log into OSC, it'll be there because the
system will load up .bash_profile when you log in.

Alternatively, instead of using nano:

.. code-block:: bash

    $ echo "export PATH=/fs/project/PAS1573/bin/:$PATH" >> .bash_profile



File and Folder Permissions
---------------------------

The dreaded "Permission Denied" error.

Since our class/project comprises multiple members who may/may not be a part of different OSC projects, that means each
person is potentially a member of different system "groups." If you're only a member of one project - one group - then
you might not notice a difference. However, if you are, it's possible for you to create a file in a "shared" directory
(i.e. our class project directory) that others cannot read or write to.

By default, each user has a specific group that they will assign to a file or folder when they create it.

Given our class project is PAS1573, we want all members in our class *group* to be able to write to all directories and
read all files.

For example, lets say you want to share data with your classmates...

.. code-block:: bash

    # Create the directory
    $ mkdir data_to_share
    # Change the group of the directory to the class/project group
    $ chgrp PAS1573 data_to_share
    # Make sure everything within that directory will have the same group as the class/group
    $ chmod g+s data_to_share
    # Set permissions for the owner (4+2+1) and group (4+2+1) to read, write, and execute
    $ chmod 770 data_to_share


Advanced (or maybe "convenient"?) commands
------------------------------------------

Below is a list of commands Ben uses way too much and wants to keep around for posterity.

**Count the number of sequences in a fasta file**

.. code-block:: bash

    $ grep -c ">" sequences.fasta

**Count the number of sequences in a gzip-compressed fastq file (.fastq.gz)**

.. code-block:: bash

    $ zcat seqs.fastq.gz | echo $((`wc -l`/4))

For non-compressed files, use :code:`cat` instead.

**Submit an interactive job on OSC**

.. code-block:: bash

    $ srun --pty -N $NODES -n $CPU_THREADS -t $TIME -A $PROJECT /bin/bash -l

Keep in mind that nodes, cpu_threads, time and project must be specified. And, while you *can* specify any length of time,
you will need to wait for those resouces to become available. So if you request 120 hours, you might have to wait a while.

**Get some stats on a job**

.. code-block:: bash

    $ sacct -j $JOBID --format "CPUTime,MaxRSS,Elapsed"

Note: There are A LOT of options within the format field.

**Get the size of the current directory and its subdirectories**, aggregating results to one folder "depth" (i.e. --max-depth=1)

.. code-block:: bash

    $ du -h --max-depth=1 .


Checking for non-ASCII characters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you ever run a command and somewhere along the line there's an error that includes "Non-ACSII character at X line"
it's probably due to using (often) Windows or software that auto-formats characters into something else. One great example
is the `em dash <https://www.thepunctuationguide.com/em-dash.html>`_. While great for punctuation (I use it often!), it
makes a **terrible** character to put into a bash script. Frequently, text writing software will auto-format a double
dash ("--") for an em-dash. (It's called "em" because it's like the length of an "M"... I think). Why is it a bad
character? It's not part of the ASCII character set. It's part of Unicode's set (U+2014). We won't go into details here,
but long story short, if you want to emulate it, use double dashes instead.

So if you have this error, you need to 1) identify the non-ASCII characters and 2) eliminate them. Below are two ways to
identify such characters using grep. For the 2nd option on a Mac, you must install pcre via Homebrew or MacPorts.

.. code-block:: bash

    # https://stackoverflow.com/a/13702856
    $ grep --color='auto' -P -n '[^\x00-\x7F]' filename
    # OR on Mac
    $ pcregrep --color='auto' -n '[^\x00-\x7F]' filename


... more to be added at a later time!

