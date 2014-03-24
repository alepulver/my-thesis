function Workflow() {

}

Workflow.prototype.run = function() {
	//this.step = new EmptyStep();
};

Workflow.prototype.step_call = function(step, parameters) {

};

Workflow.prototype.step_return = function(parameters) {

};

function WorkflowStep(workflow) {
	this.workflow = workflow;
}

WorkflowStep.prototype.ret = function(result) {
	this.workflow.step_return(result);
};

function ChooseElement(workflow) {
	WorkflowStep.call(this, workflow);
}

ChooseElement.prototype = Object.create(WorkflowStep.prototype);

ChooseElement.prototype.start = function(choices) {
	var rect = new Kinetic.Rect({
		x: 239,
		y: 75,
		width: 100,
		height: 50,
		fill: 'green',
		stroke: 'black',
		strokeWidth: 4
	});

	var simpleText = new Kinetic.Text({
		x: stage.width() / 2,
		y: 15,
		text: 'Simple Text',
		fontSize: 30,
		fontFamily: 'Calibri',
		fill: 'green'
	});
};

ChooseElement.prototype.finish = function(result) {
	
};