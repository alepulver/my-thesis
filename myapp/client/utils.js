assert = function(condition, message) {
	if (!condition) {
		str = message || "Assertion failed";
		console.log(str);
		throw str;
	}
}

submitAnswers = function() {
	cfHandler.state.inputDone({a: 1, b: 2});
};

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

    /*
    var spec = {
      type: 'vertical',
      sizes: [0.3, 0,2, 0,5],
      contents: [
      {
        type: 'horizontal',
        contents: ['choose', 'colors'],
      },
      'text',
      'canvas'
      ]   
    };
    */