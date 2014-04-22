setupCanvas = function() {
  //blah = new RSVP.Promise();

  var stage = new Kinetic.Stage({
	container: 'container',
	width: 800,
	height: 800
  });

  /*
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
  */

  //var workflow = new Workflow(stage);
  //workflow.run(workflowHandler(workflow));
  //alert(MyTEXT);
  spawnGenerator(workflowHandler(stage));
}

spawnGenerator = function(generatorFunc) {
  function continuer(verb, arg) {
	var result;
	/*
	try {
	  result = generator[verb](arg);
	} catch (err) {
	  return RSVP.Promise.reject(err);
	}
	*/
	result = generator[verb](arg);
	if (result.done) {
	  return result.value;
	} else {
	  return RSVP.Promise.resolve(result.value).then(onFulfilled, onRejected);
	}
  }
  
  var generator = generatorFunc();
  var onFulfilled = continuer.bind(continuer, "next");
  var onRejected = continuer.bind(continuer, "throw");
  
  return onFulfilled();
}

assert = function(condition, message) {
	if (!condition) {
		str = message || "Assertion failed";
		console.log(str);
		throw str;
	}
}

LayoutUtils = function() { };
LayoutUtils.generate = function(spec, dimensions) {
	switch (spec.type) {
		case 'horizontal':
			if (spec.sizes) {
				assert(spec.sizes.length == spec.sizes.length, 'sizes mismatch')
				var result = {};
				var position = 0;
				_.each(_.zip(spec.sizes, spec.contents), function(elem) {
					if (_.isObject(elem[1])) {
						// recursion
						var other = LayoutUtils.generate(elem[1].contents);
						_.extend(result, other);
					} else {
						result[elem[1]] = position;
					}
					position += elem[0]*dimensions.width;
				});
			}
			break;
		case 'vertical':
			break;
	}
}