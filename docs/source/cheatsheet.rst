Cheat sheet
===========

The three things people ask for most, as copy-paste one-liners. Each recipe
links to the full procedure — read it before doing this for real. Values like
``-n 3 -k 2`` and the reader names are **examples**; substitute your own.

.. note::

   **Reader selection.** Pass explicit reader names for a **multi-reader
   bench** (all cards powered at once). **Omit** them for a **single reader**
   (you are prompted to swap cards). Find the exact names with
   ``shamir-cli reader list``.

.. tip::

   **See what's on your readers first** — always safe, read-only::

      shamir-cli reader list
      shamir-cli --reader "<admin-reader>" orchestrator info
      shamir-cli --reader "<storage-reader>" storage info

I want to run a ceremony
------------------------

Generate a master secret, split it ``k``-of-``n``, write the shares to the
storage cards, run the backup test, and wrap the seed for the target — here a
**Cryptnox wallet** used as the HSM.

.. code-block:: bash

   # 2-of-3, 256-bit random seed, wrapped straight into a Cryptnox wallet
   shamir-cli workflow full-ceremony -n 3 -k 2 -s 32 \
       --blessings-bundle ./batch.bundle.json \
       --wallet-hsm "Cryptnox NFC" --wallet-pin 0000 \
       --output-dir ./ceremony-out

.. important::

   **A real ceremony consumes the factory blessing bundle** (``*.bundle.json``):
   it carries the group public key and each card's pre-signed blessing, which the
   orchestrator needs to accept the storage cards. You may **omit**
   ``--blessings-bundle`` only if exactly one ``*.bundle.json`` sits in the
   working directory (it is auto-discovered). Only ``--test-mode`` runs without a
   bundle.

Wrap for an **external HSM** instead of a wallet with
``--rsa-key-file hsm_pubkey.pem`` (or ``--kms-key-id`` for AWS KMS). On a bench,
add ``--orch-reader ... --storage-readers r1,r2,r3``.

→ Full guide: :doc:`ceremony`.

I want to reconstruct my secret into a wallet
---------------------------------------------

Collect ``k`` storage cards, rebuild the seed on an orchestrator, and import it
**directly into a Cryptnox wallet** (the seed never lands in a file).

.. code-block:: bash

   # any 2 of the 3 cards; insert them in share-index order when prompted
   shamir-cli workflow full-recovery -k 2 \
       --wallet-hsm "Cryptnox NFC" --wallet-pin 0000 \
       --pin 0000

Re-wrap for a **new HSM** instead with
``--rsa-key-file new_hsm_pubkey.pem --output-file recovered_seed.bin``.

→ Full guide: :doc:`recovery`.

I want to reset a storage card PIN with the Admin card
------------------------------------------------------

Reset a forgotten/locked PIN **without knowing the old one**, using the Admin
card (nonce challenge, signed by the Admin, verified by the storage card).

.. code-block:: bash

   # Prerequisite (set-once, FRESH card only — normally done at the factory):
   # the storage must carry the admin public key. On a fresh (0x00) card:
   shamir-cli --reader "<admin-reader>" admin get-pubkey          # -> <admin_pub hex>
   shamir-cli --reader "<storage-reader>" storage set-admin-pubkey <admin_pub hex>

   # Reset the PIN — bench (two readers, nothing to swap):
   shamir-cli workflow reset-pin --new-pin 1234 --admin-pin 0000 \
       --storage-reader "<storage-reader>" --admin-reader "<admin-reader>"

   # ...or single reader (insert/​swap the cards when prompted):
   shamir-cli workflow reset-pin --new-pin 1234 --admin-pin 0000

Verify afterwards with ``shamir-cli --reader "<storage-reader>" storage verify-pin 1234``.

.. important::

   **The Admin card has its own PIN** (``--admin-pin``, default ``0000``): it refuses
   to sign a reset until that PIN is verified — so a lost/stolen Admin card **alone**
   cannot reset anything (two-factor: possession **+** PIN). It allows **10** attempts
   and its lockout is **irreversible** (nothing sits above the Admin card), so keep the
   admin PIN safe and change it from the default at provisioning
   (``shamir-cli admin change-pin <new> --pin <current>``).

.. note::

   The admin public key must be provisioned on the storage card **before** the
   ceremony loads its share (it is accepted only on a fresh card). The factory does
   this during personalization; a card already carrying a share cannot be made
   admin-resettable retroactively.

.. note::

   If you **know** the current PIN and just want to change it (no Admin card),
   use ``storage verify-pin <old>`` then ``storage change-pin <new>``.

→ Context and custody policy: :doc:`governance`.

I want to check my backup is intact
-----------------------------------

Confirm ``k`` storage cards still reconstruct the original secret — **without
exporting the seed and without incrementing the read counter** of the cards.
This is the safe, repeatable health check.

.. code-block:: bash

   shamir-cli workflow backup-test -k 2 --pin 0000

It reports the reconstructed checksum for you to compare against the value
recorded at the ceremony. Read counters stay untouched, so you can run it as
often as you like.

→ Full guide: :doc:`backup_test`.

I want to reset a card so I can reuse it
----------------------------------------

Return a card to the factory state (state ``0x00``) to start a fresh ceremony
or re-provision it.

.. code-block:: bash

   # Orchestrator — back to 0x00 (e.g. after a recovery left it at 0x44):
   shamir-cli --reader "<admin-reader>" orchestrator reset

   # Storage — requires the current PIN AND a typed confirmation:
   shamir-cli --reader "<storage-reader>" storage reset --pin 0000
   #   -> prompts: Type 'I understand' to proceed

   # ...in a script, skip the confirmation with --yes:
   shamir-cli --reader "<storage-reader>" storage reset --pin 0000 --yes

.. warning::

   Resetting a **storage** card **permanently destroys its share** and cannot be
   undone. The command makes you type ``I understand`` first; ``--yes`` bypasses
   that for automation. Only reset a card whose share you no longer need, or
   after a successful recovery. Resetting the **orchestrator** is harmless — it
   holds no long-term secret, so it needs no confirmation.

   The **Admin card has no reset**: its key is the fleet's PIN-reset root (no
   rotation path), so it is permanent — decommissioning an Admin card is a factory
   re-flash, not a field operation.

→ Card states and lifecycle: :doc:`concepts` / :doc:`governance`.
