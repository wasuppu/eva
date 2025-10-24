// Prologue:
const {print, spawn, sleep, scheduler, NextMatch, send, receive} = require('./runtime');


function success (param) {
  return print("Success =", param);
}


function notFound (url) {
  return print("Not found:", url);
}


async function* _handleConnection (data) {
  let request = await receive(this);
  try {
    if (("hello" !== request)) throw NextMatch; 
    success(100);
  } catch (e) {
    if ((e !== NextMatch)) throw e; 
    try {
      let {code: _code, len: len} = request;
      if ((_code !== 200)) throw NextMatch; 
      {
        success(len);
        yield* _handleConnection.call(this, data);
      }
    } catch (e) {
      if ((e !== NextMatch)) throw e; 
      try {
        let {code: _code, url: url} = request;
        if ((_code !== 404)) throw NextMatch; 
        notFound(url);
      } catch (e) {
        if ((e !== NextMatch)) throw e; 
        return print(data);
      }
    }
  }
}

let p1 = spawn(_handleConnection, "default");
let i = 0;

function sendMessage () {
  i = (i + 1);
  if ((i <= 5)) send(p1, {code: 200, len: i});  else send(p1, "hello");
}

setInterval(sendMessage, 500);
        