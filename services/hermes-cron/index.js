import { createServer } from 'node:http';
import { runHermesScan } from './lib/run.js';
import { INTERVAL_HOURS } from './lib/config.js';

// Railway healthcheck needs something listening on PORT.
createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('hermes-cron ok\n');
}).listen(process.env.PORT || 8080);

async function tick() {
  try {
    await runHermesScan();
  } catch (err) {
    console.error('[hermes-cron] scan failed', err);
  }
}

tick();
setInterval(tick, INTERVAL_HOURS * 60 * 60 * 1000);
console.log(`[hermes-cron] started, scanning every ${INTERVAL_HOURS}h`);
