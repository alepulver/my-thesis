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

	makeHoverable group, rect

	group.add(rect)
	group.add(text)
	group.height(rect.height())

	group


class inputSlider
	constructor: (@group, @text) ->
		commonText = (moreParams) ->
			localParams = {
				fontSize: 20, fontFamily: 'Calibri',
				fill: '#555',
				width: 200,
				align: 'center'
			}
			params = _.merge({}, localParams, moreParams)
			new Kinetic.Text(params)

		line = new Kinetic.Line({
			points: [0, 0, 500, 0],
			offsetX: 250,
			stroke: 'black', strokeWidth: 2
		})
		@background = new Kinetic.Rect({
			x: 0, y: 0,
			width: 540,	height: 30,
			offsetX: 270, offsetY: 15,
			fill: 'transparent'
		})
		textLeft = commonText({
			text: 'Nada forzado',
			x: -250-100, y: 20
		})
		textRight = commonText({
			text: 'Muy forzado',
			x: 250-100, y: 20
		})
		textTop = commonText({
			text: text,
			fontSize: 25,
			fill: '#555',
			offsetX: 100,
			x: 0, y: -60
		})
		@bar = new Kinetic.Rect({
			x: 0, y: 0,
			width: 6, height: 30,
			offsetX: 3, offsetY: 15,
			fill: 'grey'
		})
		@group.add line
		@group.add textLeft
		@group.add textRight
		@group.add textTop
		@group.add @bar
		@group.add @background

	enable: (@notifier) ->
		self = this
		@bar.fill('brown')
		@bar.getLayer().draw()
		@background.on('mousemove', ->
			stage = this.getStage()
			pos = stage.getPointerPosition()

			center = self.group.getAbsolutePosition()
			vector = {
				x: pos.x - center.x,
				y: pos.y - center.y
			}
			self.bar.x(Widgets.constrainBetween(vector.x, -250, 250))
			self.group.getLayer().draw()
		)
		@background.on('mousedown', ->
			self.clickHandler()
		)

	clickHandler: ->
		# XXX: avoid error when mouseout arrives later
		@background.off('mousemove')
		@background.off('mousedown')

		@bar.fill('black')
		@bar.getLayer().draw()

		value = (@bar.x()+250)/500
		console.log(value)
		@notifier value


addBorder = (layer) ->
	###
	border = new Kinetic.Line({
		points: [0, 0, layer.width(), 0, layer.width(), layer.height(), 0, layer.height(), 0, 0],
		dash: [20, 5],
		stroke: 'black',
		strokeWidth: 5
	})
	###
	border = new Kinetic.Rect({
		x: 2, y: 2,
		width: layer.width()-4, height: layer.height()-2,
		stroke: 'grey', strokeWidth: 4,
		fill: 'transparent'
	})
	layer.add border
	layer.draw()


defaultPosFunc = (widget, shape) ->
	{
		x: shape.getPosition().x,
		y: shape.getPosition().y - (shape.getHeight()/2 + 30)
	}


addTooltip = (shape, text, positionFunc = defaultPosFunc) ->
	widget = new Kinetic.Text({
		text: text,
		fontSize: 18, fontFamily: 'Calibri',
		width: 100,
		align: 'center',
		offsetX: 50
	})

	shape.on('mouseover', ->
		parent = this.getParent()
		widget.setPosition(positionFunc(widget, this))
		color = this.stroke()
		if (color == 'yellow')
			color = 'gold'
		widget.fill(color)
		parent.add(widget)
		parent.draw()
	)

	shape.on('mouseout', ->
		widget.remove()
		this.getParent().getParent().draw()
	)


boundingBoxPositionsFor = (shape) ->
	{
		topLeft: {
			x: shape.x - shape.width/2,
			y: shape.y - shape.height/2
		},
		topRight: {
			x: shape.x + shape.width/2,
			y: shape.y - shape.height/2
		},
		bottomLeft: {
			x: shape.x - shape.width/2,
			y: shape.y + shape.height/2
		},
		bottomRight: {
			x: shape.x + shape.width/2,
			y: shape.y + shape.height/2
		}
	}


boundingBoxFits = (shape, container) ->
	shapeBB = boundingBoxPositionsFor shape
	adjustedContainer = {
		x: container.x + container.width/2,
		y: container.y + container.height/2,
		width: container.width,
		height: container.height
	}
	containerBB = boundingBoxPositionsFor adjustedContainer

	isLeft = shapeBB.topLeft.x < containerBB.topLeft.x
	isRight = shapeBB.bottomRight.x > containerBB.bottomRight.x
	isUp = shapeBB.topLeft.y < containerBB.topLeft.y
	isDown = shapeBB.bottomRight.y > containerBB.bottomRight.y

	isHorizontalOff = isLeft || isRight
	isVerticalOff = isUp || isDown
	
	{
		x: !isHorizontalOff,
		y: !isVerticalOff,
		all: !(isHorizontalOff || isVerticalOff)
	}


rectCollision = (rect1, rect2) ->
	right = rect2.x > rect1.x+rect1.width
	left = rect2.x+rect2.width < rect1.x
	down = rect2.y > rect1.y+rect1.height
	up = rect2.y+rect2.height < rect1.y

	!(right || left || down || up)


constrainedPosUpdate = (shape, container, newPos) ->
	newShape = {
		x: newPos.x,
		y: newPos.y,
		width: shape.width,
		height: shape.height
	}
	result = boundingBoxFits newShape, container
	
	{
		x: (if result.x then newPos.x else shape.x),
		y: (if result.y then newPos.y else shape.y)
	}


makeHoverable = (group, shape) ->
	# add hover styling
	group.on('mouseover', ->
		#layer = this.getLayer()
		document.body.style.cursor = 'pointer'
		shape.strokeWidth(4)
		shape.getLayer().draw()
	)
	group.on('mouseout', ->
		#layer = this.getLayer()
		document.body.style.cursor = 'default'
		shape.strokeWidth(2)
		shape.getLayer().draw()
	)


@Widgets ?= {}
_.merge(@Widgets, {
	createButton: createButton
	inputSlider: inputSlider
	addBorder: addBorder
	addTooltip: addTooltip
	boundingBoxPositionsFor: boundingBoxPositionsFor
	boundingBoxFits: boundingBoxFits
	constrainedPosUpdate: constrainedPosUpdate
	makeHoverable: makeHoverable
	rectCollision: rectCollision
})