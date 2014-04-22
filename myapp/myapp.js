if (Meteor.isClient) {
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
