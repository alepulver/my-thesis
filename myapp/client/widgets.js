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
  var objectTopLeft = {
    x: (absPos.x - object.width()/2),
    y: (absPos.y - object.height()/2)
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
  if (objectTopLeft.x + object.getWidth() > containerTopLeft.x + container.getWidth())
    ignoreX = true;
  if (objectTopLeft.y + object.getHeight() > containerTopLeft.y + container.getHeight())
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
    var ignore = checkBounds(pos, this, this.getLayer());
    return {
      x: (ignore.x ? oldPos.x : pos.x),
      y: (ignore.y ? oldPos.y : pos.y)
    };
  });

  //group.offsetX(shape.radius());
  //group.offsetY(shape.radius());
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
    //image.setPosition(center);

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