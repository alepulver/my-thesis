setupCanvas = function() {
  //blah = new RSVP.Promise();

  var stage = new Kinetic.Stage({
	container: 'container',
	width: 800,
	height: 800
  });

  var cfHandler = new csExport.HandleCF(stage);
}


CanvasForCircles = function(layer) {
  this.layer = layer;
  this.circles = [];

  var background = new Kinetic.Rect({
    fill: '#eeffee',
    width: this.layer.getWidth(),
    height: this.layer.getHeight()
  });
  this.layer.add(background);
};

//CanvasForCircles.prototype = Object.create(WorkflowStep.prototype);

CanvasForCircles.prototype.new_circle = function(which, notifier) {
  this.notifier = notifier;

  var circle = new Kinetic.Circle({
    x: 0,
    y: 0,
    radius: 70,
    stroke: 'black',
    strokeWidth: 10,
    fill: 'transparent',
    name: 'image'
  });
  this.circle = circle;
  var button = new MyButton({x: 100, y: this.layer.getHeight()-100, width: 100, text: 'Accept'});
  var wrapper = new MyResizableWrapper(circle, this.layer);

  var self = this;
  button.on('mousedown', function() {
    // XXX: avoid error when mouseout arrives later
    button.off('mouseover');
    button.off('mouseout');
    button.remove();
    wrapper.remove();
    circle.setPosition(wrapper.getPosition());
    //self.layer.add(circle);
    self.layer.draw();
    self.notifier(circle);
    });

  this.layer.add(button);
  this.layer.add(wrapper);
  this.layer.draw();
};

CanvasForCircles.prototype.setColor = function(color) {
  this.circle.setStroke(color);
  this.circle.draw();
};

ColorChooser = function(colors, layer) {
  this.layer = layer;
  this.colors = colors;
  this.notifier = null;

  var position = 0;
  var self = this;
  _.each(this.colors, function(color) {
    var rect = new Kinetic.Rect({
      x: position,
      y: 5,
      width: 20,
      height: 20,
      fill: color
    });
    rect.on('mousedown', function() {
      self.notify(color);
    });
    rect.on('mouseover', function() {
      rect.setStroke('black');
      rect.setStrokeWidth(3);
      rect.draw();
    });
    rect.on('mouseout', function() {
      rect.setStroke('transparent');
      rect.setStrokeWidth(0);
      rect.getParent().draw();
    });
    self.layer.add(rect);
    position += 25;
  });

  this.layer.draw();
};

ColorChooser.prototype.notify = function(color) {
  if (this.notifier != null) {
    this.notifier(color);
  }
};

ColorChooser.prototype.setNotifier = function(notifier) {
  this.notifier = notifier;
};

TextCanvas = function(layer) {
  this.layer = layer;
};
