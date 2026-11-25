Installation
============

Requirements
------------

- **Python 3.10 or newer**
- A **contact PC/SC smart card reader** (for hardware operations)
- On Linux, the PC/SC daemon (``pcscd``) running:

  .. code-block:: bash

     sudo systemctl start pcscd
     sudo systemctl enable pcscd

Install
-------

The ``shamir-cli`` source package is supplied by Cryptnox with your card set.
Unpack it and install it from its directory. For hardware operations, include
the ``card`` extra (which pulls in ``pyscard``):

.. code-block:: bash

   cd shamir-cli    # the directory supplied by Cryptnox

   # With smart card support (physical cards)
   pip install -e ".[card]"

   # Or, for pure-software Shamir only (no reader)
   pip install -e .

After installation, the ``shamir-cli`` command is available on your ``PATH``.

.. note::

   This is an *editable* install (``-e``): the command runs the source in
   ``src/shamir_cli``, so any update to the source is picked up immediately.
   Do not move or delete that directory, or the command will break.

Verify the installation
------------------------

.. code-block:: bash

   shamir-cli --version
   shamir-cli reader list

``reader list`` should show your contact reader, for example:

.. code-block:: text

   ┌───┬──────────────────────────┐
   │ # │ Reader Name              │
   ├───┼──────────────────────────┤
   │ 0 │ <your contact reader>    │
   └───┴──────────────────────────┘

Insert an orchestrator card and confirm it responds:

.. code-block:: bash

   shamir-cli orchestrator info

.. code-block:: text

   ┌─────────┬──────────────────────────┐
   │ Type    │ O (Orchestrator)         │
   │ Version │ 0.9.2                    │
   │ State   │ 0x00 - Initial (reset)   │
   └─────────┴──────────────────────────┘

Global options
--------------

Every command accepts these global options:

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Option
     - Effect
   * - ``-r, --reader TEXT``
     - Select a reader by partial name match (a substring of its name).
   * - ``-S, --simulator``
     - Use the JCOP simulator on ``localhost:8050`` instead of hardware.
   * - ``--sim-port INT``
     - Simulator port (default ``8050``).
   * - ``-v, --verbose``
     - Print the raw APDU traffic (for debugging).
   * - ``-q, --quiet``
     - Suppress non-essential output.
   * - ``--json``
     - Emit machine-readable JSON (for scripting / integration).

Selecting a reader
~~~~~~~~~~~~~~~~~~~

When several readers are connected, target one explicitly by a substring of
its name (as shown by ``reader list``):

.. code-block:: bash

   shamir-cli -r "<reader-name>" orchestrator info

The match is a case-insensitive substring of the reader name.
