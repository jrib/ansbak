======
ansbak
======

ansbak coalesces ``ansible -m shell`` output.  If two machines return identical output, you only see it once.  This is similar to ``dshbak`` for pdsh_ or ``clush --dshbak`` from clustershell_.

.. _pdsh: https://code.google.com/p/pdsh/
.. _clustershell: http://cea-hpc.github.io/clustershell/

Without ansbak:

.. code-block:: bash

    $ ansible host1:host2 -m shell -a 'echo foo\\nbar'
    host1 | success | rc=0 >>
    foo
    bar

    host2 | success | rc=0 >>
    foo
    bar

With ansbak:

.. code-block:: bash

    $ ansible host1:host2 -m shell -a 'echo foo\\nbar'  | ansbak.py
    host1,host2 | success | rc=0 >>
    foo
    bar

To allow ansible to colour code, you
can force_ it with the following, which ansbak can still parse:

.. _force: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-force-color

.. code-block:: bash

    $ export ANSIBLE_FORCE_COLOR=true
    $ ansible host1:host2 -m shell -a 'echo foo\\nbar'  | ansbak.py
    host1,host2 | success | rc=0 >>
    foo
    bar

Todo
----

* Group hostnames more intelligently, e.g., "host1-3" instead of "host1, host2, host3"
