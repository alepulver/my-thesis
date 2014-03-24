function MyButton(parameters) {
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
}

function MyChoiceMenu(stage, choices) {
  var p = 0.1;
  var layer = new Kinetic.Layer();

  //alert(_.size(choices));
  for (var key in choices) {
    button = new MyButton({
      text: choices[key],
      x: 30,
      y: stage.getHeight()*p,
      width: 200
    });
    layer.add(button);
    p += 0.8/Object.keys(choices).length;
  }
  return layer;
}

setupCanvas = function() {
  //blah = new RSVP.Promise();

  var stage = new Kinetic.Stage({
    container: 'container',
    width: window.innerWidth * 0.7,
    height: window.innerHeight * 0.9
  });

  window.onresize = function() {
    var width = window.innerWidth * 0.7;
    var height = window.innerHeight * 0.9;
    var scalex = width/stage.getWidth();
    var scaley = height/stage.getHeight();

    stage.setWidth(width);
    stage.setHeight(height);
    stage.scaleX(stage.scaleX()*scalex);
    stage.scaleY(stage.scaleY()*scaley);
    stage.draw();
  }

  var layer = new Kinetic.Layer();

  /*
  var button = MyButton({
    text: 'blah blah blah',
    x: 50,
    y: 50,
    width: 200
  });
    var button2 = MyButton({
    text: 'some text',
    x: 50,
    y: 150,
    width: 100
  });

  layer.add(button);
  layer.add(button2);
  */

  // add the shape to the layer
  layer.add(new Kinetic.Rect({
    fill: '#eeffee',
    width: stage.getWidth(),
    height: stage.getHeight()
  }));

  // add the layer to the stage
  stage.add(layer);

  stage.add(MyChoiceMenu(stage, {
    one: 'first button',
    two: 'second button',
    third: 'another button'
  }))
}

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

  image.setPosition(topLeft.getPosition());

  var width = topRight.x() - topLeft.x();
  var height = bottomLeft.y() - topLeft.y();
  if(width && height) {
    image.setSize({width: width, height: height});
  }
}

function addAnchor(group, x, y, name) {
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
    layer.draw();
  });
  anchor.on('mousedown touchstart', function() {
    group.setDraggable(false);
    this.moveToTop();
  });
  anchor.on('dragend', function() {
    group.setDraggable(true);
    layer.draw();
  });
  // add hover styling
  anchor.on('mouseover', function() {
    var layer = this.getLayer();
    document.body.style.cursor = 'pointer';
    this.setStrokeWidth(4);
    layer.draw();
  });
  anchor.on('mouseout', function() {
    var layer = this.getLayer();
    document.body.style.cursor = 'default';
    this.strokeWidth(2);
    layer.draw();
  });

  group.add(anchor);
}
function loadImages(sources, callback) {
  var images = {};
  var loadedImages = 0;
  var numImages = 0;
  for(var src in sources) {
    numImages++;
  }
  for(var src in sources) {
    images[src] = new Image();
    images[src].onload = function() {
      if(++loadedImages >= numImages) {
        callback(images);
      }
    };
    images[src].src = sources[src];
  }
}

function initStage(images) {
  var stage = new Kinetic.Stage({
    container: 'container',
    width: 578,
    height: 400
  });

  var darthVaderGroup = new Kinetic.Group({
    x: 270,
    y: 100,
    draggable: true
  });

  var layer = new Kinetic.Layer();

  /*
   * go ahead and add the groups
   * to the layer and the layer to the
   * stage so that the groups have knowledge
   * of its layer and stage
   */
  layer.add(darthVaderGroup);
  stage.add(layer);

  // darth vader
  var darthVaderImg = new Kinetic.Image({
    x: 0,
    y: 0,
    image: images.darthVader,
    width: 200,
    height: 138,
    name: 'image'
  });

  darthVaderGroup.add(darthVaderImg);
  addAnchor(darthVaderGroup, 0, 0, 'topLeft');
  addAnchor(darthVaderGroup, 200, 0, 'topRight');
  addAnchor(darthVaderGroup, 200, 138, 'bottomRight');
  addAnchor(darthVaderGroup, 0, 138, 'bottomLeft');

  darthVaderGroup.on('dragstart', function() {
    this.moveToTop();
  });

  stage.draw();
}

var sources = {
  darthVader: 'http://www.html5canvastutorials.com/demos/assets/darth-vader.jpg',
};
//loadImages(sources, initStage);