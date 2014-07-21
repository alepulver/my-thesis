Results = new Meteor.Collection("results");

Router.map(function() {
  this.route('experiments', {path: '/'});
  this.route('results');
});

if (Meteor.isClient) {
  Session.set("active_stage", "loading");
  Session.set("current_user", Meteor.uuid());
  
  Template.active_stage = function() {
    return Template[Session.get("active_stage")];
  };

  Template.results.as_json = function() {
    data = Results.find().fetch();
    return JSON.stringify(data, null, 2);
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
