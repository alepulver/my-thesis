_ = lodash

class Introduction
	constructor: ->
		@name = "introduction"
		self = this
		Template.introduction.events({
			'click #start': (event, template) -> self.startPressed(event, template)
		})

	start: (@workflow) ->
		# do nothing

	startPressed: (event, template) ->
		event.preventDefault()

		results = {
			ip_address: headers.getClientIP(),
			user_agent: navigator.userAgent,
			group: Session.get("current_group"),
			participant: Session.get("current_user"),
			local_id: ReactiveStore.get("local_id")
		}
		###
		geo = Geolocation.getInstance()
		results['geolocation'] = {
			latitude: geo.lat,
			longitude: geo.lng,
			error: geo.error
		}
		###

		@workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
	Introduction: Introduction
})