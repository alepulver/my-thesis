_ = lodash

class QuestionsEnd
  constructor: ->
    @name = "questions_ending"
    self = this
    Template.questions_ending.events({
      'success.form.bv': (event, template) -> self.formSubmitted(event, template)
    })

  start: (@workflow) ->
    notSelected =
      message: 'No seleccionaste ninguna opción'
      callback: (value, validator) ->
        value != null
    
    $('form[id="myform"]').bootstrapValidator(
      feedbackIcons:
        valid: 'glyphicon glyphicon-ok'
        invalid: 'glyphicon glyphicon-remove'
        validating: 'glyphicon glyphicon-refresh'

      fields:
        daynight:
          validators:
            callback: notSelected
    )

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