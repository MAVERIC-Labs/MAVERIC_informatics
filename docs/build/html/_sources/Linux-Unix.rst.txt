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

Check back for more content!


Advanced (or maybe "convenient"?) commands
------------------------------------------

Below is a list of commands Ben uses way too much and wants to keep around for posterity.

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

