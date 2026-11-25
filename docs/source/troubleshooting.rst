Troubleshooting
===============

This page lists the situations you are most likely to hit and how to resolve
them. Status words (``SW=...``) are the two-byte codes returned by the card.

No readers found
----------------

*"No smart card readers found."*

- Confirm the reader is connected: ``shamir-cli reader list``.
- On Linux, ensure ``pcscd`` is running: ``sudo systemctl status pcscd``.
- You may need permissions — run under ``sudo`` or add your user to the
  ``pcscd`` group.
- Remember: **only contact readers** work. NFC / contactless is rejected.

Command not allowed (``SW=6985``)
---------------------------------

The card's state machine refused the command in its current state.

- You issued a step out of order (e.g. exporting a share before the seed was
  generated).
- The simplest fix is to **reset and start the workflow again**:

  .. code-block:: bash

     shamir-cli orchestrator reset

.. note::

   The guided workflows (:doc:`ceremony`, :doc:`recovery`) drive the state
   machine for you. If you see ``6985`` while using them, the card was likely
   left in a partial state — reset it and re-run.

Wrong data / crypto error (``SW=6A80``)
---------------------------------------

A cryptographic check failed. Common causes:

- The cards do **not** belong to the same set (a storage card from another
  set, or mixed with another orchestrator).
- The wrong **RSA key** was supplied for wrapping.

Re-run the workflow from a clean reset, using cards from the same set.

.. _troubleshooting-wrong-pin:

Wrong PIN
---------

*``SW=63CX`` — "Wrong PIN, X tries remaining".*

- ``X`` is the number of attempts left before lockout.
- After **three** wrong attempts, the card locks.
- The factory default PIN is ``0000``.

.. warning::

   A locked storage card cannot be read with its PIN. With an **Admin card**
   (PIN level C) you can reset it; otherwise the three-attempt budget is
   precious — keep PINs in your custody records. See :ref:`hardware:pin-levels`.

Resetting a stuck card
----------------------

If a card is left in a non-initial state (for example after an interrupted
ceremony), simply reset it:

.. code-block:: bash

   # Orchestrator
   shamir-cli orchestrator reset

   # Storage (PIN required)
   shamir-cli storage reset --pin 0000

If a storage card's PIN is lost or locked (after three wrong attempts):

- **With an Admin card (PIN level C)** — reset the card's PIN with the Admin
  card and set a new one. The card and its share are recovered. This is the
  recommended setup (see :ref:`hardware:pin-levels`).
- **Without an Admin card (level A/B)** — the card cannot be unlocked; it, and
  the share it holds, are lost. As long as you still have ``k`` working cards,
  recovery is unaffected; if you drop below ``k``, the secret can no longer be
  reconstructed from the cards.

.. note::

   The **orchestrator** is different: it holds **no secret** at rest. If an
   orchestrator card is lost, damaged, or locked, it is not a security concern
   — request a replacement orchestrator card (matched to your card set) from
   Cryptnox at contact@cryptnox.com. Your storage cards and their shares are
   unaffected.

Cards still "Loaded" before a new ceremony
------------------------------------------

If a storage card reports state ``0x02`` (Loaded), it still holds a share from
a previous ceremony. Reset it first:

.. code-block:: bash

   shamir-cli storage reset --pin 0000

Recovery produced the wrong secret
----------------------------------

The recovery completed but the ``Recovery checksum`` does **not** match the
checksum recorded at the ceremony.

- **Cause:** the cards were inserted in the wrong order, or cards from a
  different ceremony were mixed in. The system relies on inserting cards in
  **share-index order** (:ref:`ceremony:labelling`).
- **Fix:** do not import the result. Re-run, inserting the correctly labelled
  cards (#1 first, #2 second, …).

.. important::

   Always verify the ``Recovery checksum`` against your ceremony record
   **before** importing a recovered seed into an HSM.

Reconstruction is slow
----------------------

On-card reconstruction performs modular inversions, which are expensive on a
smart card. A large threshold on a large curve (for example ``k = 7`` on
P-521) can take on the order of a second. This is expected.

.. seealso::

   - :doc:`recovery` — the correct recovery procedure.
   - :doc:`security_model` — PINs, lockout, and the audit counter.
