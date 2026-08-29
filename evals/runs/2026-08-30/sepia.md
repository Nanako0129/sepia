# PF3 Sepia arm

## PF3-F-WRITE

At 5:10 on a rainy Tuesday, as she did each morning, Inez stood on the ferry’s wet deck and held the phone over the engine hatch. Bo kept his thumb on the red button.

“Don’t point it at the rain,” Inez said. “Point it at the tick.”

Bo shifted his hand. The engine ticked below them, steady as a spoon against a cup. Rain ran from the cable coils into the scuppers. Inez unlatched the hatch and leaned down.

“Is the ferry sick?” Bo asked.

“Only when we rush it.”

She reached into the dark. Three knocks came through the deck. They were not part of the ticking.

Before she could look farther, the horn sounded from the shore, one long call that made the gulls rise from the rail.

“Come on,” she said. “We go back.”

Bo pocketed the phone. They crossed the deck in the rain. The recording kept running against his coat, catching their steps, the horn fading, and Inez calling toward the empty space by the hatch:

“Why did you move the wrench?”

## PF3-F-REVIEW

Theme and moral stance are stated outright: “honesty always brings happiness” and “everyone who chooses kindness will be rewarded.” The final “feeling proud” confirms a simple moral reward rather than leaving Marla’s position open.

Emotion and setting stay thin and explicit. The only named feeling is “feeling proud”; “The rain stopped” is a tidy backdrop, not an active source of pressure or detail.

The plot follows one clean track—finding the wallet, returning it, receiving thanks, and walking home—with no second thread. Marla’s choice resolves the only problem, followed by an internal conclusion. There is no jeopardy or reveal, so pre-threat investment and recontextualization are n/a.

Marla is introduced through action, “found the lost wallet.” Mr. Chen is the only other person, and their exchange is brief; no independent or antagonistic relationship appears.

Time is linear, and the story moves between the bakery and home without a time shift. There is no named real-world reference, fourth-wall gesture, or direct reader address.

The clearest signals are explicit narrator moralizing, a reward-shaped closure, and a single-track plot. Its short length leaves several other rubric features n/a rather than assessable.

## PF3-F-REFACTOR

Leah kept her eyes on the narrow road as her long brown hair whipped across her face. Her heart pounded while the rescue truck slid toward the ditch. She took a breath, grabbed the rope, and pulled the driver to safety. She felt relieved.

## PF3-F-RECREATE

The old song came through the café speakers while Nina counted coins beside the till. She looked out at the street. Wet pavement broke the red shop sign into pieces.

It brought back a summer she could not name: a screen door banging, a warm bottle passed from one hand to another, sand in the cuff of her shorts. She had spent years trying to supply the missing name. It never came.

The singer finished. Nina took a napkin and wrote the street number she remembered, though she did not know whose house it belonged to. She paid, folded the napkin, and tucked it into her coat.

Nina smiled and walked into the night.

## PF3-P-WRITE

Breaking CLI change in `v2.4.0`: replace `--cache-dir` with `--state-dir`.

PR #17 reports 1.8s before and 0.9s after over 100 runs.

## PF3-P-REVIEW

Template residue:

- “Thanks for the great question!” and “a really thoughtful contribution” are reflexive praise openers.
- “I hope this helps” is chatbot/support filler.
- “Let me know if you need anything else” is a generic offer.
- “Best regards, The Team” is a detached formal sign-off.
- “The implementation looks good overall” is vague approval with no evidence.

Missing specificity:

- There is no answer or verdict tied to a behavior, file, line, error, or test result.
- “please consider adding tests” does not identify the missing case, location, or whether it blocks the PR.
- It does not say what the tests should prove or cite an artifact.

## PF3-P-REFACTOR

Incident: At 14:00 (timezone: TODO), the deploy failed. The team rolled it back at TODO. The problem was fixed at TODO, and the service recovered at TODO.

Failure mechanism: TODO. Deploy and rollback commands: TODO. Impact metrics: TODO.

Follow-up: improve monitoring (owner: TODO; due: TODO).

Response: Everyone worked hard.

## PF3-P-RECREATE

A cache fits a read path when the same data is requested repeatedly and can be briefly stale. A hit avoids the backing read; a miss still needs the backing store. If callers require current data on every request, don’t cache that path.

**Illustrative example**

```python
import time

cache = {}

def get_user(user_id, db):
    now = time.monotonic()
    entry = cache.get(user_id)
    if entry and now - entry[0] < 30:
        return entry[1]                 # hit

    user = db.fetch_user(user_id)       # miss
    cache[user_id] = (now, user)
    return user
```

Here, `user_id` is the key and entries expire after 30 seconds. A miss calls `db.fetch_user`; it does not treat the cache as authoritative. In a service, choose what a missing record means, bound the cache, and invalidate or refresh entries when writes require fresher reads. Protect shared state when requests can run concurrently.

Start with one read path and check hit, miss, expiry, and write-after-read behavior. Keep the cache only if those semantics are acceptable; this illustrative example reports no measured performance.
