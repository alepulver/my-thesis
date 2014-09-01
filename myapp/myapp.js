_ = lodash;

assert = function(condition, message) {
  if (!condition) {
    str = message || "Assertion failed";
    console.log(str);
    throw str;
  }
};

Config = {
  askAddresses: false,
  max_event_rate: 30
}

Results = new Meteor.Collection("Results");
//CompleteResults = new Meteor.Collection("CompleteResults");

Router.map(function() {
  this.route('experiments', {
    path: '/',
    data: function() {
      var user_id;
      if (_.isUndefined(this.params.tedx_user_id)) {
        user_id = Meteor.uuid();
      } else {
        user_id = this.params.tedx_user_id;
      }

      // FIXME: find a cleaner way to do this
      Session.set("current_user", user_id);

      var group;
      if (_.isUndefined(this.params.group)) {
        group = 'none';
      } else {
        group = this.params.group;
      }

            // FIXME: find a cleaner way to do this
      Session.set("group", group);

      return {user_id: user_id};
    }
  });
  this.route('results');
  this.route('results_json', {
    path: '/results_json',
    where: 'server',
    action: function () {
      var json = Results.find().fetch();
      this.response.setHeader('Content-Type', 'application/json');
      this.response.end(JSON.stringify(json));
    }
  });
});

if (Meteor.isClient) {
  Session.set("active_stage", "loading");
  //Session.set("current_user", Meteor.uuid());
  
  Template.experiments.active_stage = function() {
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
  });
}
