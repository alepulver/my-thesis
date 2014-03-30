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

MyChoiceMenu = function(stage, choices) {
  var p = 0.1;
  var layer = new Kinetic.Layer();
  var promise = new RSVP.Promise(function(resolve, reject) {
    // XXX: Javascript "for (var key in ...)" bindings for "key" don't work, we need a function argument
    _.each(choices, function(value, key) {
      var button = new MyButton({
        text: value,
        x: 30,
        y: stage.getHeight()*p,
        width: 200
      });
      layer.add(button);

      button.on('mousedown', function() {
        resolve(key);
      });

      p += 0.8/Object.keys(choices).length;
    });
  });
  return {layer: layer, promise: promise};
};

MyResizableWrapper = function(shape) {
  var group = new Kinetic.Group({
  	x: 100,
  	y: 100,
  	draggable: true
  });

  group.add(shape);
  addAnchor(group, 0, 0, 'topLeft');
  addAnchor(group, shape.getWidth(), 0, 'topRight');
  addAnchor(group, shape.getWidth(), shape.getHeight(), 'bottomRight');
  addAnchor(group, 0, shape.getHeight(), 'bottomLeft');

  return group;
};
