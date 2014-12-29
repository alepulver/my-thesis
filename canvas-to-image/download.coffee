# casperjs module code
#require = patchRequire(require);

casper = require('casper').create(
    verbose: true
    logLevel: "debug"
)
_ = require('underscore')

i = -1
links = [1, 2, 3]

getLinks = ->
    $('a').map((i,e) -> $(e).attr('href'))

fs = require('fs')

casper.start "http://localhost:8080/stages", ->
    @echo 'Entered home page'
    links = @evaluate getLinks
    _.each links, (x) ->
        casper.then ->        
            casper.echo(x)
            casper.thenOpen("http://localhost:8080"+x, ->
                @waitForText('Download', ->
                    thing = @evaluate ->
                        $('#download').attr('href')
                    #@clickLabel 'Download'
                    #@on 'resource.received', (resource) ->
                        #casper.download resource.url
                    @echo thing.length
                    fs.write('test.png', thing)
                , -> console.log('ouch')
                10000
                )
            )

casper.run ->
    @echo 'done'