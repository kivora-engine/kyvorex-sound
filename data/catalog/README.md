# Catalog sources

The site loads `data/sounds.json` at runtime. That file is **generated**
from the four source files in this folder:

- `interface.json` — Interface category
- `alerts.json` — Alerts category
- `gameplay.json` — Gameplay category
- `sci-fi.json` — Sci-Fi category

Each source file has the shape:

    {
      "category": "<Category>",
      "sounds": [ ... ]
    }

## Adding a new sound

1. Put its audio files in `audio/wav/<id>.wav` and `audio/mp3/<id>.mp3`.
2. Open the JSON file of the correct category.
3. Add a new object to the `sounds` array, following the same structure
   as the other entries (`id`, `name`, `category`, `description`, `tags`,
   `duration`, `date`, `mp3`, `wav`, `license`, `status`, `previewMode`,
   `wavMode`, `mp3Mode`).
4. Set `status` to `"available"` if both audio files exist,
   `"coming-soon"` otherwise.
5. Regenerate the full catalog:

       python3 scripts/build_catalog.py

   or run the full build (`npm run build`, which calls this script).

## Checking the result

    python3 scripts/build_catalog.py

It prints one line per source file and either:

- writes `data/sounds.json` on success, or
- fails with a clear message (missing field, duplicate id, wrong
  category, invalid JSON…).

## Duplicate ids

The builder refuses to produce a catalog if two sounds share the same
`id`. Fix the duplicate in the source file and re-run.

## Do not edit `data/sounds.json` by hand

It is regenerated from these sources. Any manual edit will be lost
on the next build.