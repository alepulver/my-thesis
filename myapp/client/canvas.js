setupCanvas = function() {
  var stage = new Kinetic.Stage({
    container: 'container',
    width: 578,
    height: 200
  });

  var layer = new Kinetic.Layer();

  var rect = new Kinetic.Rect({
    x: 239,
    y: 75,
    width: 100,
    height: 50,
    fill: 'green',
    stroke: 'black',
    strokeWidth: 4
  });

  // add the shape to the layer
  layer.add(rect);

  // add the layer to the stage
  stage.add(layer);
}

function update(activeAnchor) {
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
    image.setSize({width:width, height: height});
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
    update(this);
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
  var yodaGroup = new Kinetic.Group({
    x: 100,
    y: 110,
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
  layer.add(yodaGroup);
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
  // yoda
  var yodaImg = new Kinetic.Image({
    x: 0,
    y: 0,
    image: images.yoda,
    width: 93,
    height: 104,
    name: 'image'
  });

  yodaGroup.add(yodaImg);
  addAnchor(yodaGroup, 0, 0, 'topLeft');
  addAnchor(yodaGroup, 93, 0, 'topRight');
  addAnchor(yodaGroup, 93, 104, 'bottomRight');
  addAnchor(yodaGroup, 0, 104, 'bottomLeft');

  yodaGroup.on('dragstart', function() {
    this.moveToTop();
  });

  stage.draw();
}

var sources = {
  darthVader: 'http://www.html5canvastutorials.com/demos/assets/darth-vader.jpg',
  yoda: 'http://www.html5canvastutorials.com/demos/assets/yoda.jpg'
};
loadImages(sources, initStage);