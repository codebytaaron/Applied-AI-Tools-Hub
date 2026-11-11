# Repository maintenance

Projects keep their existing folder names so bookmarks and project-specific instructions remain valid. Similar titles can represent different industries; do not delete or merge projects based only on their names.

## Add or update a project

1. Keep its README, dependency manifest, and sample inputs together in the project folder.
2. For Python prompt templates, include `main.py`, `prompt.py`, `requirements.txt`, `.env.example`, and `examples/input.txt`.
3. Keep real credentials in ignored `.env` files. Commit only blank or placeholder values in `.env.example`.
4. Regenerate navigation and run the checks:

   ```bash
   python3 scripts/catalog.py
   python3 scripts/check_repo.py
   ```

The catalog groups top-level folders by their files; nested projects remain accessible through their collection folders. Update the README counts if top-level projects change.

## What the checks cover

The GitHub Actions workflow parses Python source and JSON, verifies template setup files, and checks that the catalog is current. It uses the Python standard library and makes no model API calls. It does not install or execute every independent application, validate live integrations, or verify other language toolchains. Run a changed application's own checks separately.

## Existing incomplete project

`46-ops-dashboard/` contains a README but no implementation or dependency files. Its setup instructions cannot run as-is. It remains in the catalog for visibility; restore its source before treating it as a working application.

## License

Maintenance instructions do not change the repository's licensing terms. See the root [LICENSE](../LICENSE) and any project-specific license files.
