# PF3-EVAL-V1 grades

| ID | B-OP | B-ROUTE | B-FACTS | B-I1 | B-I2 | B-I3 | B-I4 | S-OP | S-ROUTE | S-FACTS | S-I1 | S-I2 | S-I3 | S-I4 | HUMAN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PF3-F-WRITE | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | NOT_RUN |
| PF3-F-REVIEW | PASS | PASS | FAIL | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_RUN |
| PF3-F-REFACTOR | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | NOT_RUN |
| PF3-F-RECREATE | PASS | PASS | FAIL | PASS | FAIL | PASS | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_RUN |
| PF3-P-WRITE | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | FAIL | NOT_RUN |
| PF3-P-REVIEW | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_RUN |
| PF3-P-REFACTOR | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | NOT_RUN |
| PF3-P-RECREATE | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | NOT_RUN |

## Evidence

### Case 1

Baseline is a fiction scene beginning “At 5:10 each morning” with “Inez, the ferry mechanic,” and “Bo held the phone,” but it never identifies Bo as a child; it includes “three knocks,” “horn called them back to shore,” and “moved the wrench.” Sepia instead says “Inez stood on the ferry’s wet deck and held the phone” and “Bo kept his thumb on the red button”: it never identifies Inez as the ferry mechanic or explicitly establishes Bo as a child holding the phone. Sepia still states “At 5:10 on a rainy Tuesday,” “Three knocks came through the deck,” and ends with “Why did you move the wrench?”

### Case 2

Baseline is diagnosis-only, with “Character and stakes,” “Connection,” and “Ending and theme,” and quotes “honesty always brings happiness”; it only says “found the lost wallet” and does not identify the bakery or walk home. It also never marks the unsupported jeopardy, reveal, or allusive-gesture dimensions as not applicable. Sepia explicitly says “There is no jeopardy or reveal” and identifies “no named real-world reference, fourth-wall gesture, or direct reader address,” while covering “between the bakery and home” and “finding the wallet, returning it, receiving thanks, and walking home.”

### Case 3

Baseline preserves “blue eyes” and “long brown hair,” then “grabbed the rope” and “pulled the driver to safety,” with “felt relieved.” Sepia preserves the rescue sequence and relief but says only “kept her eyes,” so the protected blue-eye fact is absent. Both reduce the stacked cues and remove the explanatory courage ending.

### Case 4

Baseline retains “old song,” “café,” “summer she could not name,” the singer’s finish, and walking “toward the station,” but ends without a smile; that omitted protected anchor also fails the corrected I4 condition. Sepia has “The singer finished” and “Nina smiled and walked into the night.” Both use fresh concrete material and no lyrics.

### Case 5

Baseline leads with “User impact,” keeps the exact mapping, and says “No other release changes are supplied.” Sepia keeps “PR #17 reports 1.8s before and 0.9s after over 100 runs” and the flag mapping, but labels it a “Breaking CLI change,” an unsupplied compatibility claim.

### Case 6

Both identify supplied residue, including “Thanks for the great question!”, “I hope this helps,” “Let me know if you need anything else,” “Best regards, The Team,” and “please consider adding tests”; both note missing file, line, and test specifics without providing a replacement.

### Case 7

Baseline keeps the known timeline and TODOs for “Root cause and mechanism,” “Commands used,” “Impact metrics,” and “Owner and due date,” but does not mark separate rollback and fix timestamps and retains “Everyone worked hard during the response.” Sepia marks “rolled it back at TODO,” “fixed at TODO,” and “recovered at TODO,” yet still retains “Response: Everyone worked hard.”

### Case 8

Both label the example “Illustrative example,” explain hit/miss behavior, and avoid measured results. Baseline uses “profile:user-42” with bounded TTL and invalidation; Sepia supplies `db.fetch_user`, 30-second expiry, write-after-read checks, and closes “reports no measured performance.”
