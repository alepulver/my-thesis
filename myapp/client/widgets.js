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
    strokeWidth: 5,
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

  group.add(rect);
  group.add(complexText);

  return group;
};

MyResizableWrapper = function(shape, layer) {
  var group = new Kinetic.Group({
  	x: layer.getWidth()/2,
  	y: layer.getHeight()/2,
  	draggable: true
  });

  group.add(shape);
  addAnchor(group, -shape.getWidth()/2, -shape.getHeight()/2, 'topLeft');
  addAnchor(group, shape.getWidth()/2, -shape.getHeight()/2, 'topRight');
  addAnchor(group, shape.getWidth()/2, shape.getHeight()/2, 'bottomRight');
  addAnchor(group, -shape.getWidth()/2, shape.getHeight()/2, 'bottomLeft');

  return group;
};