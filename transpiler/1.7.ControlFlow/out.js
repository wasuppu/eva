// Prologue:
const {print} = require('./runtime');

{
  let i = 5;
  while ((i > 0)) {
    print("i =", i);
    i = (i - 1);
  }
}
        