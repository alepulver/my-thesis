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

    results = {}
    results['daynight'] = template.find("select[id=daynight]").value
    results['comments'] = template.find("textarea[id=comments]").value
    
    @workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
  QuestionsEnd: QuestionsEnd
})