// Prologue:
const {print, spawn, sleep, scheduler} = require('./runtime');


function handle (id) {
  print(id, 1);
  return print(id, 2);
}

handle("x");
handle("y");
spawn(handle, "x");
spawn(handle, "y");
        