# Domain — release notes & announcements

Covers changelogs, GitHub Releases, version announcements, and short launch posts. Run with `professional-pass.md`; add `style-pass.md` for anything longer than a changelog.

## Human baseline

Terse, factual, user-impact-first. The reader is deciding **whether to upgrade and what will break** — everything serves that decision. Conventional structure (Keep a Changelog categories: Added / Changed / Fixed / Removed / Security; or the repo's own habit) is expected, not a tell.

## AI tells in this domain

| Tell | Fix |
|---|---|
| Marketing inflation: "We're thrilled/excited to announce", "powerful new features", "seamless experience", "supercharge your workflow" | State what changed. The feature is the news; enthusiasm is not |
| Benefit claims with no mechanism: "improved performance", "enhanced stability" | The number or the change itself: "cold start 1.8s → 0.4s", "fixed a race in the retry queue (#412)" |
| Every change narrated as a sentence-long story | One line per change, verb-first, no adjectives |
| Emoji headers and exclamation marks throughout | Match the repo's existing notes; default to none |
| An intro paragraph about the journey and a closing paragraph about the road ahead | Delete both. Version, date, changes, done |
| Symmetric prose for every item regardless of importance | Order by user impact; breaking changes first, one-word fixes last |

## Rules

1. **Breaking changes first**, with the exact migration step (the command, the config key, the renamed flag).
2. Every claim carries its artifact: issue/PR numbers, commit ranges, exact version strings, real benchmark numbers with conditions. No artifact → no claim.
3. Credit people plainly ("thanks @name for #398") — no gratitude paragraphs.
4. Length follows the release: a patch release is three lines; do not inflate it to look substantial.
5. Humor and voice are allowed if the repo's history has them; never inject them fresh into a repo that doesn't.
