import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

// v1: screenshots the live homepage of the web repo, not the specific feature —
// Playwright has no way to navigate to "the page this commit touched" without a
// per-repo route map. Good enough to illustrate a post; not a pixel-exact repro.
export async function screenshotHomepage(liveUrl, aisOsDir, slug) {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await page.goto(liveUrl, { waitUntil: 'networkidle', timeout: 15000 });
    const dir = join(aisOsDir, 'screenshots', 'hermes');
    mkdirSync(dir, { recursive: true });
    const relPath = join('screenshots/hermes', `${slug}.png`);
    await page.screenshot({ path: join(aisOsDir, relPath) });
    return relPath;
  } catch (err) {
    console.error('[hermes-cron] screenshot failed', liveUrl, err.message);
    return null;
  } finally {
    await browser.close();
  }
}
