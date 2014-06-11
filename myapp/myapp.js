Results = new Meteor.Collection("results");

if (Meteor.isClient) {
  Session.set("active_stage", "experiment")
  
  Template.active_stage = function() {
    return Template[Session.get("active_stage")];
  };

  Template.questions.events({'submit form' : function(event, template) {
    event.preventDefault();
    submitAnswers();
  }});

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
