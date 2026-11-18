// npm install playwright, then: node scripts/browser-check.cjs http://localhost:8000/
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
(async () => {
  const browser = await chromium.launch({channel: process.env.BROWSER_CHANNEL || 'msedge', headless: true});
  try {
    const base = process.argv[2] || 'http://127.0.0.1:8000/';
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const errors = []; page.on('pageerror', error => errors.push(error.message));
    for (const width of [1440, 390]) {
      await page.setViewportSize({width, height: 1000});
      for (const path of ['index.html', 'classification/search.html', 'classification/class-25-clothing.html', 'guides/01-how-long-does-china-trademark-registration-take.html']) {
        const response = await page.goto(base + path, {waitUntil: 'domcontentloaded', timeout: 60000});
        assert.equal(response.status(), 200, path);
        if (path.includes('search.html')) {
          await page.waitForFunction(() => /items.*classes.*similar groups/.test(document.querySelector('#tm-status').textContent));
          await page.locator('#tm-q').fill('上衣');
          await page.waitForFunction(() => document.querySelector('#tm-results').textContent.includes('tops [clothing]'));
        }
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Overflow: ${path} at ${width}`);
      }
    }
    await page.setViewportSize({width: 1440, height: 1000});
    await page.goto(base + 'classification/search.html?class=25&q=clothing');
    await page.waitForSelector('.tm-add');
    assert((await page.locator('#tm-active').innerText()).includes('25'));
    await page.locator('.tm-add').first().click();
    assert.equal(await page.locator('#tm-selcount').innerText(), '1');
    assert((await page.locator('#tm-total').innerText()).includes('199'));
    await page.locator('#tm-clearall').click();
    assert.equal(await page.locator('#tm-selcount').innerText(), '0');
    await page.locator('#tm-clearall').click();
    assert.equal(await page.locator('#tm-selcount').innerText(), '1');
    const downloadPromise = page.waitForEvent('download');
    await page.locator('#tm-csv').click();
    assert((await downloadPromise).suggestedFilename().endsWith('.csv'));
    await page.evaluate(() => localStorage.setItem('cnclass.selection.v2', JSON.stringify({generated:'old-version',items:[{c:'25',s:'2501',zh:'上衣',en:'top',code:''}]})));
    await page.reload();
    await page.waitForSelector('.tm-saved-notice');
    assert.equal(await page.locator('#tm-selcount').innerText(), '1');
    assert((await page.locator('#tm-selbody').innerText()).includes('tops [clothing]'));
    assert.deepEqual(errors, []);
    console.log('PASS: responsive pages, CN/EN search, class filter, estimate, clear/undo, CSV and saved-list migration');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
