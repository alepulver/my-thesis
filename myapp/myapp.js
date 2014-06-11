Results = new Meteor.Collection("results");

if (Meteor.isClient) {
  Session.set("active_stage", "experiment")
  
  Template.active_stage = function() {
    return Template[Session.get("active_stage")];
  };

  Template.questions.events({'submit form' : function(event, template) {
    event.preventDefault();

    var firstname = template.find("input[name=firstname]");
    var lastname = template.find("input[name=lastname]");   
    var email = template.find("input[name=email]");
    
    cfHandler.state.inputDone({
      firstname: firstname.value,
      lastname: lastname.value,
      email: email.value
    });
  }});

  Template.results.items = function() {
    return Results.find();
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
