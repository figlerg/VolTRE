# Archiving the artifact (release zip + Zenodo)

How to turn a frozen state of this repo into the artifact zip and the Zenodo
deposit. This is internal release tooling. The whole `release/` folder is
`export-ignore`d in `.gitattributes`, so it does not ship inside the artifact
zip itself.

## What the zip contains

`git archive` includes only committed, tracked files, so gitignored paths
(`.venv/`, `wordgen/`, `artifact/output/`) never appear. On top of that, these
internal or dev-only paths are excluded via `export-ignore` in `.gitattributes`:

- `.claude/`, `.claude-sandbox/` (agent + sandbox internals)
- `.idea/`, `.obsidian/` (editor configs)
- `CLAUDE.md` (internal working notes)
- `notes/` (personal research notes)
- `vis_experiments/` (scratch PNGs)
- `release/` (this folder)

Everything else ships, including `NOTICE`, `LICENSE`, `Dockerfile`, `artifact/`,
`experiments/`, the code packages (`parse/`, `sample/`, `volume/`,
`probabilistic/`, `match/`, `misc/`), the four reviewer docs
(`README.md`, `INSTALL.md`, `REQUIREMENTS.md`, `STATUS.md`), `main.py`,
`minimal_example.py`, `tutorial.ipynb`, and `requirements.txt`.

## Recommended order (DOI ends up inside the zip)

1. Create a new upload at https://zenodo.org, type Software. Fill the fields
   from `release/zenodo-metadata.md`.
2. Reserve the DOI on the draft (Zenodo "Reserve DOI"), then paste it into the
   `STATUS.md` placeholder.
3. Commit that STATUS.md change and tag the frozen commit:

       git tag v1.0-emsoft26
       # push is done by Felix, not the agent:
       git push origin v1.0-emsoft26

4. Build the zip from the tag:

       git archive --format=zip --prefix=voltre-emsoft26/ -o voltre-emsoft26-artifact.zip v1.0-emsoft26

5. Verify the contents before uploading:

       unzip -l voltre-emsoft26-artifact.zip

   Confirm none of the export-ignored paths appear, and that `NOTICE`,
   `Dockerfile`, `artifact/`, `experiments/`, and the four docs are present.

6. Upload `voltre-emsoft26-artifact.zip` to the same Zenodo draft and publish.
   The reserved DOI activates on publish and already matches STATUS.md.

7. Put the published DOI in the HotCRP artifact form (Available badge).

## Previewing before the tag exists

To eyeball the zip from the current working tree without committing or tagging,
add `--worktree-attributes` so the uncommitted `.gitattributes` rules apply, and
archive `HEAD`:

    git archive --worktree-attributes --format=zip --prefix=voltre-emsoft26/ -o /tmp/preview.zip HEAD
    unzip -l /tmp/preview.zip

Note: `git archive` never includes untracked files, so anything newly created
(for example `NOTICE`) only shows up once it is committed.

## Notes

- Manual zip upload is used on purpose, not the Zenodo GitHub-release
  integration, so the DOI can be reserved before the content is final.
- `export-ignore` only takes effect for the rules present in `.gitattributes`
  at the archived ref, so those rules must be committed before the tag.
- Primary license is BSD-3-Clause. The bundled wordgen component is GPLv3, see
  `NOTICE` and the `COPYING` inside `artifact/wordgen-src-5502f65.tar.gz`.
