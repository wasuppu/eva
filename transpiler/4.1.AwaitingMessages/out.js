// Prologue:
const {print, spawn, sleep, scheduler, NextMatch} = require('./runtime');

let point = 2;
try {
  let {x: _x, y: _y} = point;
  if (((_x !== 1) || (_y !== 2))) throw NextMatch; 
  print("full match");
} catch (e) {
  if ((e !== NextMatch)) throw e; 
  try {
    let {x: _x, y: y} = point;
    if ((_x !== 1)) throw NextMatch; 
    print("x match, y is", y);
  } catch (e) {
    if ((e !== NextMatch)) throw e; 
    try {
      if ((1 !== point)) throw NextMatch; 
      print("point is 1");
    } catch (e) {
      if ((e !== NextMatch)) throw e; 
      print("no match");
    }
  }
}
        