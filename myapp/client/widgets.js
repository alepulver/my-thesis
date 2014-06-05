MyButton = function(parameters) {
  var group = new Kinetic.Group({
    x: parameters.x,
    y: parameters.y,
  });

  var complexText = new Kinetic.Text({
    text: parameters.text,
    fontSize: 15,
    fontFamily: 'Calibri',
    fill: '#555',
    width: parameters.width,
    padding: 10,
    align: 'center'
  });

  var rect = new Kinetic.Rect({
    stroke: '#555',
    strokeWidth: 2,
    fill: '#ddd',
    width: parameters.width,
    height: complexText.height(),
    /*
    shadowColor: 'black',
    shadowBlur: 10,
    shadowOffset: {x:10,y:10},
    shadowOpacity: 0.2,
    */
    cornerRadius: 10
  });

  group.on('mouseover', function() {
    rect.setStrokeWidth(5);
    group.getParent().draw();
  });
  group.on('mouseout', function() {
    rect.setStrokeWidth(2);
    group.getParent().draw();
  });

  group.add(rect);
  group.add(complexText);

  return group;
};

function checkBounds(absPos, object, container) {
  var objectPos = object.getAbsolutePosition();
  var objectTopLeft = {
    x: (absPos.x - 2*object.offsetX()),
    y: (absPos.y - 2*object.offsetY())
  };
  
  var containerPos = container.getAbsolutePosition();
  var containerTopLeft = {
    x: (containerPos.x - container.offsetX()),
    y: (containerPos.y - container.offsetY())
  };

  if (objectTopLeft.x < containerTopLeft.x)
    return false;
  if (objectTopLeft.y < containerTopLeft.y)
    return false;
  if (objectTopLeft.x + object.getWidth() > containerTopLeft.x + container.getWidth())
    return false;
  if (objectTopLeft.y + object.getHeight() > containerTopLeft.y + container.getHeight())
    return false;

  return true;
}

MyResizableWrapper = function(shape, layer) {
  var group = new Kinetic.Group({
    x: layer.getWidth()/2,
    y: layer.getHeight()/2,
    draggable: true
  });

  group.dragBoundFunc(function(pos) {
    if (checkBounds(pos, this, this.getLayer()))
      return pos;
    else
      return this.getAbsolutePosition();
  });

  group.offsetX(shape.offsetX());
  group.offsetY(shape.offsetY());
  group.width(shape.width());
  group.height(shape.height());
  group.add(shape);
  addAnchor(group, -shape.getWidth()/2, -shape.getHeight()/2, 'topLeft');
  addAnchor(group, shape.getWidth()/2, -shape.getHeight()/2, 'topRight');
  addAnchor(group, shape.getWidth()/2, shape.getHeight()/2, 'bottomRight');
  addAnchor(group, -shape.getWidth()/2, shape.getHeight()/2, 'bottomLeft');

  return group;
};

ChooseElement = function(choices, layer) {
  this.choices = choices;
  this.layer = layer;
  this.deferred = null;
  var self = this;
  var p = 0.1;

  _.each(this.choices, function(element) {
    var button = new MyButton({
      text: element['text'],
      x: 30,
      y: self.layer.getHeight()*p,
      width: 100
    });
    self.layer.add(button);

    button.on('mousedown', function() {
      self.button_pressed(element['name']);
    });

    p += 0.8/self.choices.length;
  });
};

//ChooseElement.prototype = Object.create(WorkflowStep.prototype);

ChooseElement.prototype.get_click = function() {
  this.deferred = RSVP.defer();
  return this.deferred.promise;
};

ChooseElement.prototype.button_pressed = function(name) {
  if (this.deferred != null) {
    this.deferred.resolve(name);
  }
};

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

CanvasForCircles.prototype.new_circle = function() {
  this.deferred = RSVP.defer();

  var circle = new Kinetic.Circle({
    x: 70,
    y: 70,
    radius: 70,
    stroke: 'black',
    strokeWidth: 10,
    offsetX: 70,
    offsetY: 70,
    fill: 'transparent',
    name: 'image'
  });
  this.circle = circle;
  var button = new MyButton({x: 100, y: this.layer.getHeight()-100, width: 100, text: 'Accept'});
  var wrapper = new MyResizableWrapper(circle, this.layer);

  var self = this;
  button.on('mousedown', function() {
    button.remove();
    wrapper.remove();
    circle.setPosition(wrapper.getPosition());
      //self.layer.add(circle);
      self.layer.draw();
      self.deferred.resolve(circle);
    });

  this.layer.add(button);
  this.layer.add(wrapper);
  this.layer.draw();

  return this.deferred.promise;
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

function updateAnchorMoved(activeAnchor) {
  var group = activeAnchor.getParent();

  var topLeft = group.find('.topLeft')[0];
  var topRight = group.find('.topRight')[0];
  var bottomRight = group.find('.bottomRight')[0];
  var bottomLeft = group.find('.bottomLeft')[0];
  var image = group.find('.image')[0];

  var anchorX = activeAnchor.x();
  var anchorY = activeAnchor.y();

    // update anchor positions
    switch (activeAnchor.name()) {
      case 'topLeft':
      topRight.y(anchorY);
      bottomLeft.x(anchorX);
      break;
      case 'topRight':
      topLeft.y(anchorY);
      bottomRight.x(anchorX);
      break;
      case 'bottomRight':
      bottomLeft.y(anchorY);
      topRight.x(anchorX); 
      break;
      case 'bottomLeft':
      bottomRight.y(anchorY);
      topLeft.x(anchorX); 
      break;
    }

    var width = topRight.x() - topLeft.x();
    var height = bottomLeft.y() - topLeft.y();

    var center = {
      x: (topLeft.x() + bottomRight.x())/2,
      y: (topLeft.y() + bottomRight.y())/2
    };
    image.setPosition(center);

    if(width && height) {
      image.setSize({width: width, height: height});
    }
  }

  addAnchor = function(group, x, y, name) {
    var stage = group.getStage();
    var layer = group.getLayer();

    var anchor = new Kinetic.Circle({
      x: x,
      y: y,
      stroke: '#666',
      fill: '#ddd',
      strokeWidth: 2,
      radius: 8,
      name: name,
      draggable: true,
      dragOnTop: false
    });

    anchor.on('dragmove', function() {
      updateAnchorMoved(this);
    //layer.draw();
  });
    anchor.on('mousedown touchstart', function() {
      group.setDraggable(false);
      this.moveToTop();
    });
    anchor.on('dragend', function() {
      group.setDraggable(true);
    //layer.draw();
  });
    // add hover styling
    anchor.on('mouseover', function() {
      var layer = this.getLayer();
      document.body.style.cursor = 'pointer';
      this.setStrokeWidth(4);
        //layer.draw();
      });
    anchor.on('mouseout', function() {
      var layer = this.getLayer();
      document.body.style.cursor = 'default';
      this.strokeWidth(2);
    //layer.draw();
  });

    group.add(anchor);
  };