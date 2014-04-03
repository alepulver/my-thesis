function assert(condition, message) {
    if (!condition) {
    	str = message || "Assertion failed";
    	console.log(str);
        throw str;
    }
}

Workflow = function(kineticStage) {
	this.stage = kineticStage;
	this.current_step = null;
	this.current_layer = null;
};

Workflow.prototype.run = function(returnHandler) {
	this.handler = returnHandler;
	this.handler({step: 'start', results: 'none'});
};

Workflow.prototype.step_call = function(step, parameters) {
	assert(this.current_step == null, "wrong call");
	
	this.current_step = step;
	var layer = step.setup_operation(parameters);
	this.current_layer = layer;
	this.stage.add(layer);
};

Workflow.prototype.step_return = function(step, results) {
	assert(step == this.current_step, "wrong return")
	
	this.current_step = null;
	this.current_layer.remove();
	this.current_layer = null;
	this.handler({step: step, results: results});
};

WorkflowStep = function(workflow) {
	this.workflow = workflow;
}

WorkflowStep.prototype.call_with = function(parameters) {
	this.workflow.step_call(this, parameters);
}

WorkflowStep.prototype.setup_operation = function(parameters) {
	throw 'subclass responsability';
};

WorkflowStep.prototype.return_value = function(result) {
	this.workflow.step_return(this, result);
};

ChooseElement = function(workflow) {
	WorkflowStep.call(this, workflow);
}

ChooseElement.prototype = Object.create(WorkflowStep.prototype);

ChooseElement.prototype.setup_operation = function(choices) {
	var menu = MyChoiceMenu(this.workflow.stage, choices);
	var self = this;
	menu.promise.then(function(result) {
		self.return_value(result);
	});
	return menu.layer;
};

CanvasForCircles = function(workflow) {
	WorkflowStep.call(this, workflow);
	this.layer = new Kinetic.Layer();

	var background = new Kinetic.Rect({
    	fill: '#eeffee',
    	width: this.workflow.stage.getWidth(),
    	height: this.workflow.stage.getHeight()
  	});
  	this.layer.add(background);
};

CanvasForCircles.prototype = Object.create(WorkflowStep.prototype);

CanvasForCircles.prototype.setup_operation = function() {

	var circle = new Kinetic.Circle({
    	x: 0,
    	y: 0,
    	radius: 70,
    	stroke: 'black',
    	offsetX: -70,
    	offsetY: -70,
    	fill: 'transparent',
    	name: 'image'
    });
    var button = new MyButton({x: 100, y: this.workflow.stage.getHeight()-100, width: 100, text: 'Accept'});
    var wrapper = new MyResizableWrapper(circle);

    var self = this;
    button.on('mousedown', function() {
    	button.remove();
    	wrapper.remove();
    	self.layer.add(circle);
    	self.return_value(circle.getPosition());
    });

  	this.layer.add(button);
  	this.layer.add(wrapper);

  	return this.layer;
};