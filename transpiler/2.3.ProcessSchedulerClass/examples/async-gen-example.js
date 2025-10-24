
function print(...args) {
    console.log(...args);
}

//////////////////////////////////////////////////////////////////////
// function handle (id) {
//     print(id, 1);
//     return print(id, 2);
// }

// handle("x");
// handle("y");

// spawn(handle, "x");
// spawn(handle, "y");

////////////////////////////////////////////////////////////
// function* _handle(id) {
//     print(id, 1);
//     yield;
//     print(id, 2);
// }

// const xGen = _handle('x');
// const yGen = _handle('y');

// 1st iteration;
// xGen.next();
// yGen.next();

// 2nd iteration;
// xGen.next();
// yGen.next();

///////////////////////////////////////////////////////////////////////
// Round Robin Scheduling (processes run in queue)
// function* _handle(id) {
//     print(id, 1);
//     yield;
//     print(id, 2);
// }

// function spawn(fn, ...args) {
//     const gen = fn(...args);
//     schedule(gen);
// }

// const runQueue = [];

// function schedule(gen) {
//     runQueue.push(gen);
// }

// function schedulerLoop() {
//     while (runQueue.length > 0) {
//         const gen = runQueue.shift();

//         // Next iteration:
//         const result = gen.next();

//         if (!result.done) {
//             schedule(gen);
//         }
//     }
// }

// spawn(_handle, 'x');
// spawn(_handle, 'y');

// schedulerLoop();


///////////////////////////////////////////////////////
// async function* _handle(id) {
//     print(id, 1);
//     yield;
//     print(id, 2);
// }
// spawn(_handle, 'x');
// spawn(_handle, 'y');


function spawn(fn, ...args) {
    const gen = fn(...args);
    schedule(gen);
}

const runQueue = [];

function schedule(gen) {
    runQueue.push(gen);
}

async function* _handle(id, ms) {
    print(id, 1);
    yield await sleep(ms);
    print(id, 2);
    yield await sleep(ms);
    print(id, 3);
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function handleProcess(gen) {
    for await (let _ of gen) {}
}

function schedulerLoop() {
    // Parallel execution:
    Promise.all(runQueue.map(gen => handleProcess(gen)));

    // Flash the queue:
    runQueue.length = 0;
}

spawn(_handle, 'x', 300);
spawn(_handle, 'y', 1000);

schedulerLoop();




