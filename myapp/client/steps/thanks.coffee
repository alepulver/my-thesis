_ = lodash

class Thanks
	constructor: ->
		@name = "thanks"

	start: (@workflow) ->
		# do nothing


@Steps ?= {}
_.merge(@Steps, {
	Thanks: Thanks
})