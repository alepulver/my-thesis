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
    name: 'background',
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
  group.height(rect.height());

  return group;
};

AddTooltip = function(shape, text) {
  var widget = new Kinetic.Text({
    text: text,
    fontSize: 17, fontFamily: 'Calibri',
    width: 100,
    align: 'center'
  });
  
  shape.on('mouseover', function() {
    var parent = this.getParent();
    widget.setPosition({
      x: this.getPosition().x - widget.getWidth()/2,
      y: this.getPosition().y - (this.getHeight()/2 + 30)
    });
    widget.fill(this.stroke());
    parent.add(widget);
    parent.draw();
  });
  
  shape.on('mouseout', function() {
    widget.remove();
    this.getParent().getParent().draw();
  });
};

function checkBounds(absPos, size, container) {
  var objectTopLeft = {
    x: (absPos.x - size.width/2),
    y: (absPos.y - size.height/2)
  };
  
  var containerPos = container.getAbsolutePosition();
  var containerTopLeft = {
    x: (containerPos.x - container.offsetX()),
    y: (containerPos.y - container.offsetY())
  };

  var ignoreX = false, ignoreY = false;

  if (objectTopLeft.x < containerTopLeft.x)
    ignoreX = true;
  if (objectTopLeft.y < containerTopLeft.y)
    ignoreY = true;
  if (objectTopLeft.x + size.width > containerTopLeft.x + container.getWidth())
    ignoreX = true;
  if (objectTopLeft.y + size.height > containerTopLeft.y + container.getHeight())
    ignoreY = true;

  return {x: ignoreX, y: ignoreY};
}

MyResizableWrapper = function(shape, layer) {
  var group = new Kinetic.Group({
    x: layer.getWidth()/2,
    y: layer.getHeight()/2,
    draggable: true
  });

  group.dragBoundFunc(function(pos) {
    var oldPos = this.getAbsolutePosition();
    var ignore = checkBounds(pos, this.size(), this.getLayer());
    return {
      x: (ignore.x ? oldPos.x : pos.x),
      y: (ignore.y ? oldPos.y : pos.y)
    };
  });

  group.width(shape.width());
  group.height(shape.height());
  group.add(shape);

  addAnchor(group, -shape.getWidth()/2, -shape.getHeight()/2, 'topLeft');
  addAnchor(group, shape.getWidth()/2, -shape.getHeight()/2, 'topRight');
  addAnchor(group, shape.getWidth()/2, shape.getHeight()/2, 'bottomRight');
  addAnchor(group, -shape.getWidth()/2, shape.getHeight()/2, 'bottomLeft');

  return group;
};

function updateAnchorMoved(activeAnchor) {
  var group = activeAnchor.getParent();
  var topLeft = group.find('.topLeft')[0];
  var topRight = group.find('.topRight')[0];
  var bottomLeft = group.find('.bottomLeft')[0];
  var bottomRight = group.find('.bottomRight')[0];
  var shape = group.find('.image')[0];

  var center = group.getAbsolutePosition();
  var other = activeAnchor.getAbsolutePosition();

  var radius = _.max([Math.abs(center.x - other.x), Math.abs(center.y - other.y)]);
  shape.radius(radius);
  shape.width(radius*2);
  shape.height(radius*2);

  group.width(shape.width());
  group.height(shape.height());

  topLeft.x(-shape.getWidth()/2);
  topLeft.y(-shape.getHeight()/2);
  topRight.x(shape.getWidth()/2);
  topRight.y(-shape.getHeight()/2);
  bottomLeft.x(-shape.getWidth()/2);
  bottomLeft.y(shape.getHeight()/2);
  bottomRight.x(shape.getWidth()/2);
  bottomRight.y(shape.getHeight()/2);
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

  anchor.dragBoundFunc(function(pos) {
    var oldPos = this.getAbsolutePosition();
    var ignore = checkBounds(pos, this.size(), this.getLayer());
      
    var center = group.getAbsolutePosition();
    var tooSmall = Math.pow(pos.x - center.x, 2) + Math.pow(pos.y - center.y, 2) < Math.pow(25, 2);
    if (tooSmall)
      return oldPos;

    var radius = _.max([Math.abs(center.x - pos.x), Math.abs(center.y - pos.y)]);
    var size = {width: radius*2, height: radius*2};
    var tooBig = checkBounds(center, size, this.getLayer());
    if (tooBig.x || tooBig.y)
      return oldPos;

    return {
      x: (ignore.x ? oldPos.x : pos.x),
      y: (ignore.y ? oldPos.y : pos.y)
    };
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