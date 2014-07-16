Results = new Meteor.Collection("results");

Router.map(function() {
  this.route('experiments', {path: '/'});
  this.route('results');
});

if (Meteor.isClient) {
  Session.set("active_stage", "loading");
  
  Template.active_stage = function() {
    return Template[Session.get("active_stage")];
  };

  Template.results.items = function() {
    return JSON.stringify(Results.find());
  };

  Meteor.startup(function() {
    // code to run on client at startup
    _ = lodash;
    startMainApp();
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
    _ = lodash;
  });
}
