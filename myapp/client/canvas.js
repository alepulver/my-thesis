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

  var workflow = new Workflow(stage);

  var choice_menu = new ChooseElement(workflow);
  var my_choices = {
    one: 'Present',
    two: 'Past',
    third: 'Future'
  };
  var remaining = 3;
  var canvas_circles = new CanvasForCircles(workflow);

  workflow.run(function(result) {
    if (result.step == 'start') {
      choice_menu.call_with(my_choices);
    
    } else if (result.step == choice_menu) {
      delete my_choices[result.results];
      remaining -= 1;
      canvas_circles.call_with(result.results);
    
    } else if (result.step == canvas_circles) {
      if (remaining > 0) {
        choice_menu.call_with(my_choices);
      } else {
        alert('end');
      }
    }
  });

  //myFuncTest();
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

  var width = topRight.x() - topLeft.x();
  var height = bottomLeft.y() - topLeft.y();

  image.setPosition(topLeft.getPosition());

  if(width && height) {
    image.setSize({width: width, height: height});
    image.setOffsetX(- width / 2);
    image.setOffsetY(- height / 2);
    /*
    image.setAttrs({
      x: image.getOffsetX(),
      y: image.getOffsetY()
    });
    */
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