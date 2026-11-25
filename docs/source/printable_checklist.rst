Printable Checklist
===================

A condensed, sign-off version of the custody controls. Print this page and keep
the signed copies with your custody log. Full detail is in the Governance
section of the documentation.

.. tip::

   To print, open this page in a browser and use **Print → Save as PDF**.

Deployment
----------

.. code-block:: text

   Set ID: ____________   Date: __________   k-of-n: ____ / ____   Seed: ____ B
   Seed checksum: __________________________   PIN level (A/B/C): ____

Ceremony
--------

.. code-block:: text

   [ ] Cards from one set; PIN level chosen
   [ ] Offline trusted machine; four-eyes
   [ ] Real HSM RSA public key used (--rsa-key-file)
   [ ] Ceremony completed; backup test PASSED
   [ ] Each storage card's share number written as it is loaded (#1, #2, ...)
   [ ] Card backs filled in, codes only (never full names, no signature):
       all = Bundle + code + ceremony date (Notes); storage = also share number
   [ ] k-of-n (total + threshold) in the custody log ONLY, never on the cards
   [ ] Wrapped seed imported to HSM, then file destroyed
   [ ] Custody log filled; cards sealed in separate locations
   [ ] Orchestrator reset; Admin card stored separately

   Officer 1: ______________   Officer 2: ______________   Date: __________

Annual verification
-------------------

.. code-block:: text

   Year: ______
   [ ] Collected cards (all n, or k + rotate): #____  #____  #____  #____
   [ ] backup-test RESULT = PASS
   [ ] Export counters checked against log
   [ ] Cards returned & sealed; log updated

   Signed: ______________   Date: __________

Custodian change
----------------

.. code-block:: text

   Leaving: ____________   New holder: ____________   Card #____
   [ ] Card retrieved
   [ ] PIN reset with Admin card + new PIN set (or card re-provisioned)
   [ ] Reassigned; custody log updated
   [ ] backup-test PASSED

   Signed: ______________   Date: __________

Lost / damaged / locked card
----------------------------

.. code-block:: text

   Card #____   Issue: ____________________
   [ ] Forgotten/locked PIN, card in hand -> reset with Admin card
   [ ] Lost/destroyed -> usable cards remaining: ____  (need >= k = ____)
       [ ] >= k -> recovery OK; plan re-ceremony to restore redundancy
       [ ] <  k -> CANNOT reconstruct from cards; escalate immediately

   Signed: ______________   Date: __________
