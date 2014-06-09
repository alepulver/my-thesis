setupCanvas = function() {
  //blah = new RSVP.Promise();

  var stage = new Kinetic.Stage({
	container: 'container',
	width: 800,
	height: 800
  });

  var cfHandler = new csExport.HandleCF(stage);
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
