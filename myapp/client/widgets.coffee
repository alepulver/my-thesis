_ = lodash

createButton = (parameters) ->
	group = new Kinetic.Group({
		x: parameters.x,
		y: parameters.y,
	})

	text = new Kinetic.Text({
		text: parameters.text,
		fontSize: 15,
		fontFamily: 'Calibri',
		fill: '#555',
		width: parameters.width,
		padding: 10,
		align: 'center',
		name: 'text'
	})

	rect = new Kinetic.Rect({
		stroke: '#555',
		strokeWidth: 2,
		fill: '#ddd',
		width: parameters.width,
		height: text.height(),
		name: 'background',
		cornerRadius: 10
	})

	group.on('mouseover', ->
		rect.setStrokeWidth(5)
		group.getParent().draw()
	)
	group.on('mouseout', ->
		rect.setStrokeWidth(2)
		group.getParent().draw()
	)

	group.add(rect)
	group.add(text)
	group.height(rect.height())

	group


addBorder = (layer) ->
	border = new Kinetic.Line({
		points: [0, 0, layer.width(), 0, layer.width(), layer.height(), 0, layer.height(), 0, 0],
		dash: [20, 5],
		stroke: 'black',
		strokeWidth: 5
	})
	layer.add border
	layer.draw()


addTooltip = (shape, text) ->
	widget = new Kinetic.Text({
		text: text,
		fontSize: 17, fontFamily: 'Calibri',
		width: 100,
		align: 'center'
	})
  
	shape.on('mouseover', ->
		parent = this.getParent()
		widget.setPosition({
			x: this.getPosition().x - widget.getWidth()/2,
			y: this.getPosition().y - (this.getHeight()/2 + 30)
		})
		widget.fill(this.stroke())
		parent.add(widget)
		parent.draw()
	)
  
	shape.on('mouseout', ->
		widget.remove()
		this.getParent().getParent().draw()
	)


createInteractiveFor = (shape, layer) ->
	group = new Kinetic.Group({
		x: layer.getWidth()/2,
		y: layer.getHeight()/2,
		draggable: true
	})

	group.dragBoundFunc((pos) ->
		oldPos = this.getAbsolutePosition()
		ignore = checkBounds(pos, this.size(), this.getLayer())
		return {
			x: (if ignore.x then oldPos.x else pos.x),
			y: (if ignore.y then oldPos.y else pos.y)
		}
	)

	group.width(shape.width())
	group.height(shape.height())
	group.add(shape)

	addAnchor(group, -shape.getWidth()/2, -shape.getHeight()/2, 'topLeft')
	addAnchor(group, shape.getWidth()/2, -shape.getHeight()/2, 'topRight')
	addAnchor(group, shape.getWidth()/2, shape.getHeight()/2, 'bottomRight')
	addAnchor(group, -shape.getWidth()/2, shape.getHeight()/2, 'bottomLeft')

	return group


checkBounds = (absPos, size, container) ->
	objectTopLeft = {
		x: (absPos.x - size.width/2),
		y: (absPos.y - size.height/2)
	}
  
	containerPos = container.getAbsolutePosition()
	containerTopLeft = {
		x: (containerPos.x - container.offsetX()),
		y: (containerPos.y - container.offsetY())
	}

	ignoreX = false
	ignoreY = false

	if (objectTopLeft.x < containerTopLeft.x)
		ignoreX = true
	if (objectTopLeft.y < containerTopLeft.y)
		ignoreY = true
	if (objectTopLeft.x + size.width > containerTopLeft.x + container.getWidth())
		ignoreX = true
	if (objectTopLeft.y + size.height > containerTopLeft.y + container.getHeight())
		ignoreY = true

	return {x: ignoreX, y: ignoreY}


updateAnchorMoved = (activeAnchor) ->
	group = activeAnchor.getParent();
	topLeft = group.find('.topLeft')[0];
	topRight = group.find('.topRight')[0];
	bottomLeft = group.find('.bottomLeft')[0];
	bottomRight = group.find('.bottomRight')[0];
	shape = group.find('.image')[0];

	center = group.getAbsolutePosition();
	other = activeAnchor.getAbsolutePosition();

	radius = _.max([Math.abs(center.x - other.x), Math.abs(center.y - other.y)]);
	shape.radius(radius);
	shape.width(radius*2);
	shape.height(radius*2);

	group.width(shape.width());
	group.height(shape.height());

	topLeft.x(-shape.getWidth()/2);
	topLeft.y(-shape.getHeight()/2);
	topRight.x(shape.getWidth()/2);
	topRight.y(-shape.getHeight()/2);
	bottomLeft.x(-shape.getWidth()/2);
	bottomLeft.y(shape.getHeight()/2);
	bottomRight.x(shape.getWidth()/2);
	bottomRight.y(shape.getHeight()/2);


addAnchor = (group, x, y, name) ->
	stage = group.getStage()
	layer = group.getLayer()

	anchor = new Kinetic.Circle({
		x: x,
		y: y,
		stroke: '#666',
		fill: '#ddd',
		strokeWidth: 2,
		radius: 8,
		name: name,
		draggable: true,
		dragOnTop: false
	})

	anchor.dragBoundFunc((pos) ->
		oldPos = this.getAbsolutePosition()
		ignore = checkBounds(pos, this.size(), this.getLayer())

		center = group.getAbsolutePosition()
		tooSmall = Math.pow(pos.x - center.x, 2) + Math.pow(pos.y - center.y, 2) < 1
		if (tooSmall)
			return oldPos

		radius = _.max([Math.abs(center.x - pos.x), Math.abs(center.y - pos.y)])
		size = {width: radius*2, height: radius*2}
		tooBig = checkBounds(center, size, this.getLayer())
		if (tooBig.x || tooBig.y)
			return oldPos

		return {
			x: (if ignore.x then oldPos.x else pos.x),
			y: (if ignore.y then oldPos.y else pos.y)
		}
	)
	anchor.on('dragmove', ->
		updateAnchorMoved(this);
	)
	anchor.on('mousedown touchstart', ->
		group.setDraggable(false)
		this.moveToTop()
	)
	anchor.on('dragend', ->
		group.setDraggable(true)
	)
	# add hover styling
	anchor.on('mouseover', ->
		layer = this.getLayer()
		document.body.style.cursor = 'pointer'
		this.setStrokeWidth(4)
	)
	anchor.on('mouseout', ->
		layer = this.getLayer()
		document.body.style.cursor = 'default'
		this.strokeWidth(2)
	)

	group.add(anchor)


@Widgets ?= {}
_.merge(@Widgets, {
	createButton: createButton
	createInteractiveFor: createInteractiveFor
	addBorder: addBorder
	addTooltip: addTooltip
})