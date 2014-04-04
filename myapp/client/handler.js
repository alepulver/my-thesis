workflowHandler = wrapGenerator.mark(function(workflow) {
    var choice_menu, my_choices, remaining, canvas_circles, choice, circle;

    return wrapGenerator(function($ctx0) {
        while (1) switch ($ctx0.prev = $ctx0.next) {
        case 0:
            choice_menu = new ChooseElement(workflow);

            my_choices = {
                one: 'Present',
                two: 'Past',
                third: 'Future'
            };

            remaining = 3;
            canvas_circles = new CanvasForCircles(workflow);
        case 4:
            if (!(remaining > 0)) {
                $ctx0.next = 15;
                break;
            }

            $ctx0.next = 7;
            return {step: choice_menu, parameters: my_choices}
        case 7:
            choice = $ctx0.sent;
            delete my_choices[choice];
            remaining -= 1;
            $ctx0.next = 12;
            return {step: canvas_circles, parameters: choice}
        case 12:
            circle = $ctx0.sent;
            $ctx0.next = 4;
            break;
        case 15:
            alert("end");
        case 16:
        case "end":
            return $ctx0.stop();
        }
    }, this);
});