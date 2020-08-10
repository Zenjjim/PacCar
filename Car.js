class Car {
  velocity = createVector(0, 0);
  acceleration = 0;
  gas = 0.1
  speedLimit = 10;
  alpha = 0;
  delta = 0.09;
  color = 'blue'
  friction = 0.98

  constructor(x, y, w, h) {
    this.resetPosition = createVector(x, y)
    this.position = createVector(x, y)
    this.prevPosition = createVector(x, y)
    this.size = createVector(w, h)
  }

  move() {
    this.acceleration = 0
    if (keyIsDown(UP_ARROW)) {
      if (pythagoras(this.velocity) < this.speedLimit) this.acceleration = -this.gas
    }
    if (keyIsDown(DOWN_ARROW)) {
      if (pythagoras(this.velocity) > -this.speedLimit) this.acceleration = this.gas
    }
    if (keyIsDown(LEFT_ARROW)) {
      this.alpha -= this.delta;
    }
    if (keyIsDown(RIGHT_ARROW)) {
      this.alpha += this.delta;
    }
    this.velocity.x += this.acceleration * -sin(this.alpha)
    this.velocity.y += this.acceleration * cos(this.alpha)
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
    this.velocity.x *= this.friction
    this.velocity.y *= this.friction
  }

  display() {
    fill('red');
    push()
    translate(this.position.x, this.position.y);
    rotate(this.alpha);
    fill(this.color)
    rect(-this.size.x / 2, -this.size.y / 2, this.size.x, this.size.y);
    fill('yellow')
    this.rect = rect(-5, -this.size.y / 2, 10, 10);
    pop();

    this.nv = createVector(this.position.x + (-this.size.x / 2 * cos(this.alpha) - this.size.y / 2 * sin(this.alpha)), this.position.y + (-this.size.x / 2 * sin(this.alpha) + this.size.y / 2 * cos(this.alpha)))
    this.ov = createVector(this.position.x + (-this.size.x / 2 * cos(this.alpha) - -this.size.y / 2 * sin(this.alpha)), this.position.y + (-this.size.x / 2 * sin(this.alpha) + -this.size.y / 2 * cos(this.alpha)))
    this.nh = createVector(this.position.x + (this.size.x / 2 * cos(this.alpha) - this.size.y / 2 * sin(this.alpha)), this.position.y + (this.size.x / 2 * sin(this.alpha) + this.size.y / 2 * cos(this.alpha)))
    this.oh = createVector(this.position.x + (this.size.x / 2 * cos(this.alpha) - -this.size.y / 2 * sin(this.alpha)), this.position.y + (this.size.x / 2 * sin(this.alpha) + -this.size.y / 2 * cos(this.alpha)))
    this.color = "blue"
  }

  reset() {
    this.position.x = this.resetPosition.x
    this.position.y = this.resetPosition.y
    this.alpha = 0;
    this.acceleration = 0;
    this.velocity = createVector(0, 0)
  }

  collide(v1, v2) {
    let colFront = collideLineLine(v1.x, v1.y, v2.x, v2.y, this.ov.x, this.ov.y, this.oh.x, this.oh.y, false)
    let colLeft = collideLineLine(v1.x, v1.y, v2.x, v2.y, this.ov.x, this.ov.y, this.nv.x, this.nv.y, false)
    let colRight = collideLineLine(v1.x, v1.y, v2.x, v2.y, this.nh.x, this.nh.y, this.oh.x, this.oh.y, false)
    let colBack = collideLineLine(v1.x, v1.y, v2.x, v2.y, this.nv.x, this.nv.y, this.nh.x, this.nh.y, false)
    if (colFront || colLeft || colRight || colBack) {
      this.color = "red"
    }
  }

}

function pythagoras(vector) {
  let a = sqrt(vector.x * vector.x + vector.y * vector.y)
  return a;
}

function collideLineLine(x1, y1, x2, y2, x3, y3, x4, y4, calcIntersection) {

  var intersection;

  // calculate the distance to intersection point
  var uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1));
  var uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1));

  // if uA and uB are between 0-1, lines are colliding
  if (uA >= 0 && uA <= 1 && uB >= 0 && uB <= 1) {

    if (calcIntersection) {
      // calc the point where the lines meet
      var intersectionX = x1 + (uA * (x2 - x1));
      var intersectionY = y1 + (uA * (y2 - y1));
    }

    if (calcIntersection) {
      intersection = {
        "x": intersectionX,
        "y": intersectionY
      }
      return intersection;
    } else {
      return true;
    }
  }
  if (calcIntersection) {
    intersection = {
      "x": false,
      "y": false
    }
    return intersection;
  }
  return false;
}