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
  max_event_rate: 30,
  secondary_save: true
}

Results = new Meteor.Collection("Results");
//Errors = new Meteor.Collection("Errors");

Router.map(function() {
  this.route('experiments', {
    path: '/',
    data: function() {
      var params = this.params;
      var read_var = function(param_name, session_name, default_value) {
        var value;
        if (_.isUndefined(params[param_name])) {
          value = default_value;
        } else {
          value = params[param_name];
        }

        // FIXME: find a cleaner way to do this
        Session.set(session_name, value);
      };

      read_var('tedx_user_id', 'current_user', 'none');
      read_var('group_id', 'current_group', 'none');

      // XXX: why on Earth do we have to do this instead of cloning or just passing?
      Session.set("url_params", _.zipObject(_.keys(params), _.values(params)));

      return {};
    }
  });

  this.route('results');

  this.route('results_json_vivejaja', {
    path: '/results_json_vivejaja',
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

  Meteor.methods({
    getSummary: function() {
      var inital_time = 0;
      var tedx_time = 0;
      var fix_time = 0;

      var summary = {};

      summary['blah'] = Results.find().count();

      return summary;
    }
  });

  Results.allow({
    insert: function (userId, experiment) {
      return true;
    }
  });
}
