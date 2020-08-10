
let car;
let track = false;
let outerTrack = true;
let pointsOuter = [{ x: 60, y: 388 }, { x: 57, y: 245 }, { x: 62, y: 96 }, { x: 223, y: 34 }, { x: 338, y: 28 }, { x: 525, y: 25 }, { x: 848, y: 61 }, { x: 917, y: 118 }, { x: 687, y: 254 }, { x: 676, y: 301 }, { x: 788, y: 308 }, { x: 886, y: 281 }, { x: 960, y: 340 }, { x: 974, y: 411 }, { x: 960, y: 476 }, { x: 710, y: 480 }, { x: 469, y: 484 }, { x: 253, y: 472 }, { x: 138, y: 448 }]
let pointsInner = [{ x: 148, y: 299 }, { x: 150, y: 173 }, { x: 251, y: 129 }, { x: 394, y: 118 }, { x: 512, y: 119 }, { x: 582, y: 116 }, { x: 666, y: 131 }, { x: 521, y: 212 }, { x: 506, y: 289 }, { x: 540, y: 342 }, { x: 574, y: 372 }, { x: 674, y: 390 }, { x: 763, y: 390 }, { x: 634, y: 395 }, { x: 376, y: 386 }, { x: 240, y: 356 }]
let checkbox;

let v1;

function setup() {
  createCanvas(1000, 500);
  car = new Car(100, 250, 15, 30)

}

function draw() {
  background(51);

  noFill();
  strokeJoin(MITER);

  fill('gray')
  beginShape();
  pointsOuter.forEach(p => vertex(p.x, p.y))
  endShape(CLOSE);

  fill(51)
  beginShape();
  pointsInner.forEach(p => vertex(p.x, p.y))
  endShape(CLOSE);

  removeElements()
  createSpan("(" + mouseX + ", " + mouseY + ")")
  createCheckbox('Draw track', track);
  createCheckbox('Outer track', outerTrack);

  car.move()
  car.display()

  for (let i = 0; i < pointsOuter.length; i++) {
    if (i + 1 === pointsOuter.length) {
      car.collide(pointsOuter[i], pointsOuter[0])
    } else {
      car.collide(pointsOuter[i], pointsOuter[i + 1])
    }
  }
  for (let i = 0; i < pointsInner.length; i++) {
    if (i + 1 === pointsInner.length) {
      car.collide(pointsInner[i], pointsInner[0])
    } else {
      car.collide(pointsInner[i], pointsInner[i + 1])
    }
  }

}

function mousePressed() {
  if (track) {
    if (outerTrack) {
      pointsOuter.push({ x: mouseX, y: mouseY })
    } else {
      pointsInner.push({ x: mouseX, y: mouseY })
    }
  }
}

function keyTyped() {
  if (key === 't') {
    outerTrack = !outerTrack;
  }
  if (key === 'c') {
    console.log(pointsOuter)
    console.log(pointsInner)
    console.log(car)
  }
  if (key === 'r') {
    car.reset()
  }
  if (key === 'd') {
    track = !track;
  }
}