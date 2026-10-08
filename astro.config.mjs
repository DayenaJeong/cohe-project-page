import { defineConfig } from 'astro/config';

// The deployment workflow supplies the URL returned by GitHub Pages itself.
// Local previews keep the project path to exercise asset routing before publication.
const pagesURL = process.env.PAGES_URL ? new URL(process.env.PAGES_URL) : undefined;
export default defineConfig({
  output: 'static',
  site: pagesURL?.origin,
  base: pagesURL?.pathname ?? '/cohe-project-page/',
  trailingSlash: 'always',
  devToolbar: { enabled: false },
});
