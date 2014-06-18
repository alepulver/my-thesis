Results = new Meteor.Collection("results");

if (Meteor.isClient) {
  Session.set("active_stage", "experiment")
  
  Template.active_stage = function() {
    return Template[Session.get("active_stage")];
  };

  Template.questions.events({'submit form' : function(event, template) {
    event.preventDefault();

    var name = template.find("input[name=name]");
    var age = template.find("input[name=age]");   
    var sex = template.find("input[name=sex]");
    var studying = template.find("input[name=studying]");
    var working = template.find("input[name=working]");
    var daynight = template.find("input[name=daynight]");
    var comments = template.find("textarea[name=comments]");
    
    cfHandler.state.inputDone({
      name: name.value,
      age: age.value,
      sex: sex.value,
      studying: studying.value,
      working: working.value,
      daynight: daynight.value,
      comments: comments.value,
    });
  }});

  Template.results.items = function() {
    return JSON.stringify(Results.find());
  };

  Meteor.startup(function() {
    // code to run on client at startup
    _ = lodash;
    setupCanvas();
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
    _ = lodash;
  });
}
