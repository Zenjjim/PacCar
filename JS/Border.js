class Border {
  dx = 5;
  dy = this.dx;
  sdx = 2;
  sdy = this.sdx;
  a = 0;
  da = 0.1;

  constructor(x, y, w, h) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }

  display() {
    push()
    translate(this.x, this.y);
    rotate(this.a);
    rect(-this.w / 2, -this.h / 2, this.w, this.h);
    pop();
  }
}