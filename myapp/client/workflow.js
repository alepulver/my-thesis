Workflow = function(kineticStage) {
	this.stage = kineticStage;
	this.current_step = null;
	this.current_layer = null;
};

Workflow.prototype.run = function(returnHandler) {

};

WorkflowStep = function(workflow) {
	this.workflow = workflow;
}

WorkflowStep.prototype.setup_operation = function(parameters) {
	throw 'subclass responsability';
};

WorkflowStep.prototype.return_value = function(result) {
	this.workflow.step_return(this, result);
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
    	x: 0,
    	y: 0,
    	radius: 70,
    	stroke: 'black',
    	strokeWidth: 10,
    	offsetX: 0,
    	offsetY: 0,
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
			y: 0,
			width: 20,
			height: 20,
			fill: color
		});
		rect.on('mousedown', function() {
			self.notify(color);
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