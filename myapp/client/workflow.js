function assert(condition, message) {
    if (!condition) {
    	console.log(message || "Assertion failed");
        throw message || "Assertion failed";
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