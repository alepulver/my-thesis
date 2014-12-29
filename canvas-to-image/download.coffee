# casperjs module code
#require = patchRequire(require);

casper = require('casper').create(
    verbose: true
    logLevel: "debug"
)
_ = require('underscore')
fs = require('fs')

getLinks = ->
    $('a').map((i,e) -> $(e).attr('href'))

casper.start "http://localhost:8080/stages", ->
    @echo 'Entered home page'
    links = @evaluate getLinks
    _.each links, (x) ->
        casper.then ->        
            casper.echo(x)
            casper.thenOpen("http://localhost:8080"+x, ->
                @waitForText('Download', ->
                    data = @evaluate ->
                        $('#download').attr('href')
                    data = data.replace('data:image/octet-stream;base64,', '')
                    filename =  @evaluate ->
                        $('#download').attr('download')

                    #fs.write('images/' + filename, data)
                    @evaluate ->
                        $('#download').hide()
                    @capture('images/' + filename)
                , -> console.log('ouch')
                10000
                )
            )

casper.run ->
    @echo 'done'