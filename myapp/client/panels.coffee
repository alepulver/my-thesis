_ = lodash

class ChoosePanel
	constructor: (choices, @layer) ->
		self = this
		@choices = _.mapValues(choices, (text) ->
			{text: text, button: null, dot: null}
		)
		@remaining = _.size(@choices)
		@current = null
		@notifier = null
		
		p = 0.1
		px = 0
		total = 0
		@keys = _.keys(@choices)
		@keys = _.shuffle(@keys)
		_.forEach(@keys, (key) ->
			if (total == 4)
				px += 170
				p = 0.1
				total -= 4
			data = self.choices[key]
			button = Widgets.createButton({
      			text: data.text,
      			x: px + 30,
      			y: self.layer.getHeight()*p,
      			width: 100
			})
			button.on('mousedown', ->
				self.itemStarted(key)
			)
			data.button = button
			self.layer.add button

			dot = new Kinetic.Circle(
				x: px + 15
				y: self.layer.height()*p + button.height()/2
				radius: 5
				stroke: 'black'
			)
			data.dot = dot
			self.layer.add dot

			p += 0.8/_.min([_.size(self.choices), 4])
			total++
		)

	setNotifier: (@notifier) ->
		#@layer.listening(@notifier != null)
		@layer.visible(@notifier != null)
		@layer.draw()

	itemStarted: (key) ->
		@active_item = key
		@remaining--

		@choices[key].dot.fill('black')
		@choices[key].button.listening(false)
		@choices[key].button.find('.background')[0].fill('#bbb')
		@layer.draw()

		@notifier(key) if @notifier != null

	itemEnded: ->


	colorSelected: (color) ->
		shape = @choices[@active_item].dot
		shape.fill(color)
		shape.getParent().draw()


class DrawingPanel
	constructor: (@layer, @createShape) ->
		@current = null

	addShape: (@name, tooltip) ->
		self = this
	
		@current = @createShape(@layer)
		@current.addTooltip(tooltip)
		
		@button = Widgets.createButton({
			x: 50,
			y: -100,
			width: 100,
			text: 'Aceptar'
		})
		@button.on('mousedown', -> self.acceptedShape())

		@layer.add @button
		@layer.add @current.group
		@layer.draw()

		@current

	acceptedShape: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()

		result = @current.fixState()
		@notifier(@name, result) # if @notifier != null

	setColor: (color) ->
		@current.setColor color
		@layer.draw()

	setNotifier: (@notifier) ->
		@layer.listening(@notifier != null)
		@layer.draw()

	askFinish: (@end_notifier) ->
		self = this
		
		@button = Widgets.createButton({
			x: 50,
			y: -100,
			width: 100,
			text: 'Finalizar'
		})
		@button.on('mousedown', -> self.finishClicked())

		@layer.add @button
		@layer.draw()

	finishClicked: ->
		# XXX: avoid error when mouseout arrives later
		@button.off('mouseover')
		@button.off('mouseout')
		@button.remove()
		@layer.draw()

		@end_notifier()


class ColorsPanel
	constructor: (@colors, @layer) ->
		@notifier = null
		@buttons = []

		position = 0
		horizMax = 4
		currentHoriz = 0
		offsetY = 0

		self = this;
		_.each(@colors, (color) ->
			rect = new Kinetic.Rect({
				x: position, y: offsetY + 10,
				width: 30, height: 30,
				fill: color
			})
			rect.on('mousedown', -> self.notify(color))
			rect.on('mouseover', ->
				rect.setStroke('black')
				rect.setStrokeWidth(3)
				rect.draw()
			)
			rect.on('mouseout', ->
				rect.setStroke('transparent')
				rect.setStrokeWidth(0)
				rect.getParent().draw()
			)
			self.buttons.push(rect);
			self.layer.add(rect);
			position += 40;
			currentHoriz++

			if (currentHoriz == horizMax)
				currentHoriz = 0
				offsetY += 40
				position = 0
		)

		@layer.draw()

	notify: (color) ->
		if (@notifier != null)
			@notifier(color)

	setNotifier: (@notifier) ->
		if (@notifier != null)
			@layer.show()
		else
			@layer.hide()
		@layer.draw()


class SliderChoosePanel
	constructor: (@questions, @layer) ->
		@current_index = 0
		@choices = _.shuffle(@questions)
		@remaining = _.size(@choices)
		@data = {
			show_order: @choices,
			results: {}
		}
	
	start: (@notifier) ->
		@group = new Kinetic.Group({
			x: @layer.width()/2,
			y: @layer.height()/2
		})
		line = new Kinetic.Rect({
			x: 0, y: 0,
			width: 500,	height: 20,
			offsetX: 250, offsetY: 10,
			fillLinearGradientStartPoint: {x: 0, y: 0},
			fillLinearGradientEndPoint: {x: 500, y: 0},
			fillLinearGradientColorStops: [0, 'white', 1, 'black']
		})
		@background = new Kinetic.Rect({
			x: 0, y: 0,
			width: 500,	height: 100,
			offsetX: 250, offsetY: 50
		})
		textLeft = new Kinetic.Text({
			text: 'Nada forzado',
			fontSize: 20, fontFamily: 'Calibri',
			fill: '#555',
			width: 200,
			align: 'left',
			x: -250, y: 40
		})
		textRight = new Kinetic.Text({
			text: 'Muy forzado',
			fontSize: 20, fontFamily: 'Calibri',
			fill: '#555',
			width: 200,
			align: 'right',
			x: 250-200, y: 40
		})
		@group.add line
		@group.add textLeft
		@group.add textRight
		@group.add @background
		@layer.add @group
		@layer.draw()

		this.askForClick()

	finish: ->
		@notifier(@data)

	askForClick: ->
		self = this
		@current_result = {
			start_time: Steps.currentTime()
		}

		@textTop = new Kinetic.Text({
			text: @choices[@current_index],
			fontSize: 25, fontFamily: 'Calibri',
			fill: '#555',
			width: 200, offsetX: 100,
			align: 'center',
			x: 0, y: -100
		})
		@theBar = new Kinetic.Rect({
			x: 0, y: 0,
			width: 6, height: 30,
			offsetX: 3, offsetY: 15,
			fill: 'brown'
		})
		@group.add @textTop
		@group.add @theBar
		@layer.draw()

		@background.moveToTop()
		@background.on('mousemove', ->
			stage = this.getStage()
			pos = stage.getPointerPosition()

			center = self.group.getAbsolutePosition()
			vector = {
				x: pos.x - center.x,
				y: pos.y - center.y
			}
			self.theBar.x(vector.x)
			self.layer.draw()
		)
		@background.on('mousedown', ->
			value = (self.theBar.x()+250)/500
			self.sliderClicked value
		)

	sliderClicked: (position) ->
		# XXX: avoid error when mouseout arrives later
		@background.off('mousemove')
		@background.off('mousedown')

		_.merge(@current_result, {
			end_time: Steps.currentTime(),
			value: position
		})
		@data.results[@choices[@current_index]] = @current_result

		@theBar.remove()
		@textTop.remove()
		@layer.draw()

		@current_index++
		@remaining--

		if (@remaining > 0)
			this.askForClick()
		else
			this.finish()


class TextPanel
	constructor: (@layer) ->


@Panels ?= {}
_.merge(@Panels,
	Choose: ChoosePanel
	Drawing: DrawingPanel
	Colors: ColorsPanel
	Text: TextPanel
	SliderChoose: SliderChoosePanel
)