# Use shared NFKC text normalization

Resume Review normalizes text with Unicode NFKC, Unicode-aware trimming, and field-appropriate whitespace collapsing before validation. User-facing capitalization and meaningful punctuation are preserved; skills are deduplicated by the case-folded normalized value while retaining the first accepted display spelling, and Skill Evidence references use the same comparison key.

The backend owns normalization and exposes normalized persisted values; frontend normalization is advisory. The same rules and test vectors apply to upload text thresholds, Profile Validity, Interview Readiness, and correction persistence so the UI and API cannot disagree about empty values, duplicates, or evidence references.
