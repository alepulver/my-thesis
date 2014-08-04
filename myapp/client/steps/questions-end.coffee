_ = lodash

class QuestionsEnd
  constructor: ->
    @name = "questions_ending"
    self = this
    Template.questions_ending.events({
      'success.form.bv': (event, template) -> self.formSubmitted(event, template)
    })
    
    @choices = {
      size: 'Tamaño',
      position: 'Ubicación',
      cololr: 'Color'
    }
    @questions = _.shuffle(_.keys(@choices))
    Template.questions_ending.items_forced = () ->
      _.map(self.questions, (key) ->
        {code: key, name: self.choices[key]})

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
        represents_time:
          validators:
            callback: notSelected
    )

    $('.slider').slider({tooltip: 'hide'})

  formSubmitted: (event, template) ->
    event.preventDefault()

    results = {}
    results['represents_time'] = template.find("select[id=represents_time]").value
    results['daynight'] = template.find("select[id=daynight]").value
    results['comments'] = template.find("textarea[id=comments]").value
    _.forEach(@questions, (key) ->
      name = 'slider-' + key
      results[name] = $('#' + name).data('slider').getValue()
    )
    
    @workflow.stepFinished(results)


@Steps ?= {}
_.merge(@Steps, {
  QuestionsEnd: QuestionsEnd
})