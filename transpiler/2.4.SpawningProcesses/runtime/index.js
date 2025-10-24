const {Scheduler} = require('./Scheduler')

/**
 * Global scheduler.
 */
const scheduler = new Scheduler();

/**
 * Start hanlding processes.
 */
scheduler.start();

/**
 * Print to stdout.
 */
function print(...args) {
  console.log(...args);
}

/**
 * Spawns a process.
 */
function spawn(fn, ...args) {
  return scheduler.spawn(fn, ...args);
}

/**
 * Sleep wrapper.
 */
async function sleep(ms) {
  return await scheduler.sleep(ms);
}

module.exports = {
  scheduler,
  print,
  spawn,
  sleep,
};