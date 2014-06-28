_ = lodash

class QuestionsEnd
  constructor: ->
    @name = "questions_ending"
    self = this
    Template.questions_ending.events({
      'submit form': (event, template) -> self.formSubmitted(event, template)
    })

  start: (@workflow) ->
    # do nothing

  formSubmitted: (event, template) ->
    event.preventDefault()

    variables = ['daynight']
    results = {}
    _.each(variables, (field) ->
      results[field] = template.find("input[name=#{field}]").value
    )
    results['comments'] = template.find("textarea[name=comments]").value
    
    @workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
  QuestionsEnd: QuestionsEnd
})