Command Reference
=================

The ``shamir-cli`` command drives the whole system. This page lists every
command. For guided procedures, see :doc:`ceremony`, :doc:`recovery` and
:doc:`backup_test`.

Basic usage
-----------

.. code-block:: bash

   shamir-cli [GLOBAL OPTIONS] GROUP COMMAND [ARGS]...

Global options
--------------

.. option:: -r, --reader TEXT

   Select a reader by a case-insensitive substring of its name.

.. option:: -S, --simulator

   Use the JCOP simulator on ``localhost:8050`` instead of a physical reader.

.. option:: --sim-port INTEGER

   Simulator port (default ``8050``).

.. option:: -v, --verbose

   Print the raw APDU traffic, for debugging.

.. option:: -q, --quiet

   Suppress non-essential output.

.. option:: --json

   Emit machine-readable JSON, for scripting and integration.

Workflow commands
-----------------

The high-level, guided procedures. **Start here.**

full-ceremony
^^^^^^^^^^^^^

Generate a seed (or import one), split it, and distribute shares to storage cards.

.. code-block:: bash

   shamir-cli workflow full-ceremony -n N -k K -s SIZE [-t TYPE] \
       [--blessings-bundle FILE] [--rsa-key-file FILE] [--output-dir DIR]
       [--secret-file FILE | --secret HEX]

A real ceremony consumes the factory blessing bundle (``*.bundle.json``);
``--blessings-bundle`` is auto-discovered in the working dir if omitted. Only
``--test-mode`` runs without one.

Add ``--secret-file`` (or ``--secret``) to **import** an existing secret instead
of generating one on-card — same cards, same split, but the seed is not re-wrapped
to an HSM. See :doc:`ceremony` for the full procedure.

full-recovery
^^^^^^^^^^^^^

Reconstruct the seed from ``k`` storage cards and re-wrap it for a new HSM.

.. code-block:: bash

   shamir-cli workflow full-recovery -k K \
       [--rsa-key-file FILE] [--output-file FILE] [--pin PIN]

See :doc:`recovery`.

backup-test
^^^^^^^^^^^

Verify that shares still reconstruct the seed, without exporting it.

.. code-block:: bash

   shamir-cli workflow backup-test -k K [--pin PIN]

See :doc:`backup_test`.

ceremony-import
^^^^^^^^^^^^^^^

Import an **existing** seed and back it up with Shamir (rather than generating
a fresh one on-card). The secret is **required** — pass ``--secret-file`` (a hex
or raw file) or ``--secret`` (hex string); its length must equal ``-s``. There is
no random fallback: for a fresh seed use ``full-ceremony``.

.. code-block:: bash

   shamir-cli workflow ceremony-import -n N -k K -s SIZE [-t TYPE] \
       (--secret-file FILE | --secret HEX) [--output-dir DIR]

Reader commands
---------------

list
^^^^

List the connected smart card readers.

.. code-block:: bash

   shamir-cli reader list

Orchestrator commands
---------------------

These act on the orchestrator card. In normal use the **workflow** commands
above drive it for you — the two commands below are the only ones you invoke
directly.

info
^^^^

Show the card type, firmware version, and state.

.. code-block:: bash

   shamir-cli orchestrator info

reset
^^^^^

Reset the orchestrator to the initial state (``0x00``).

.. code-block:: bash

   shamir-cli orchestrator reset

Storage commands
----------------

These act on a storage card.

info
^^^^

Show the card type, version, and state.

.. code-block:: bash

   shamir-cli storage info

reset
^^^^^

Reset the storage card to ``0x00`` (requires the PIN).

.. code-block:: bash

   shamir-cli storage reset --pin 0000

verify-pin / change-pin
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   shamir-cli storage verify-pin [PIN]
   shamir-cli storage change-pin [NEW_PIN]

read-counter
^^^^^^^^^^^^

Read the export counter (for audit — see :doc:`security_model`).

.. code-block:: bash

   shamir-cli storage read-counter

pedersen-verify
^^^^^^^^^^^^^^^

Verify a single card — or a whole set with ``--readers`` — against its
ceremony, without exporting the seed. See :ref:`single-card-verify`.

.. code-block:: bash

   shamir-cli storage pedersen-verify
   shamir-cli storage pedersen-verify --readers "<reader-1>,<reader-2>,..."

Pure-software Shamir (no card)
------------------------------

Run Shamir's maths entirely in software — useful for testing and for
understanding the scheme. **No secret-bearing hardware is involved.**

split
^^^^^

.. code-block:: bash

   shamir-cli shamir split <SECRET_HEX> -k K -n N -s SIZE

recover
^^^^^^^

.. code-block:: bash

   shamir-cli shamir recover -s SIZE --share 1:HEX --share 2:HEX ...

verify
^^^^^^

.. code-block:: bash

   shamir-cli shamir verify <SECRET_HEX> -s SIZE --share 1:HEX ...

A concrete end-to-end example — split a 16-byte secret 2-of-3, then recover it
from any two shares:

.. code-block:: console

   $ shamir-cli shamir split 000102030405060708090a0b0c0d0e0f -k 2 -n 3 -s 16
     Share  1: 555f6ab7fdfe2769ceb6da59773e816d
     Share  2: aabdd36cf7f748cc9564aaa7e26ff4cb
     Share  3: 001c3c21f1f06a2f5c127af64da16b46

   $ shamir-cli shamir recover -s 16 \
       --share 1:555f6ab7fdfe2769ceb6da59773e816d \
       --share 3:001c3c21f1f06a2f5c127af64da16b46
     Recovered secret: 000102030405060708090a0b0c0d0e0f

.. note::

   These commands never touch a card and are safe to experiment with. Do not
   use them on a **real** secret on a networked machine — the secret is
   handled in plaintext in the host's memory, unlike the hardware workflows.

.. seealso::

   - :doc:`ceremony`, :doc:`recovery`, :doc:`backup_test` — the guided
     procedures built on these commands.
