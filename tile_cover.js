#!/usr/bin/env node

var fs = require('fs');
var program = require('commander');
var tileCover = require('@mapbox/tile-cover');

program.version('0.1.0')
    .option('-s, --start <n>', 'Start Index', parseInt, 0)
    .option('-e, --end <n>', 'End Index', parseInt)
    .option('-g, --geoid <str>', 'GeoID Column')
    .option('-a, --min <n>', 'Min Zoom', parseInt)
    .option('-b, --max <n>', 'Max Zoom', parseInt)
    .option('-i, --input  <str>', 'Input: GeoJSON file')
    .option('-o, --output <str>', 'Output: JSON')
    .parse(process.argv);


geoid = program.geoid;
min = program.min
max = program.max
output = program.output;
input = program.input;
start = program.start;
var geojson = JSON.parse(fs.readFileSync(input));
if (program.end || program.end<geojson.features.length) {
    end = program.end;
} else {
    end = geojson.features.length}

console.log('Start: %j', start);
console.log('End: %j', end);
console.log('GeoID: %j', geoid);
console.log('Min: %j', min);
console.log('Max: %j', max);
console.log('Input: %j', input);
console.log('Output: %j', output);
console.log('Length: %j', geojson.features.length)



var obj = [];
var i;
for (i = start; i < end; i++) {
    // var geo = tileCover.geojson(geojson.features[i].geometry, {min_zoom: 7, max_zoom: 18});
    // var tiles = tileCover.geojson(geojson.features[i].geometry, {min_zoom: 7, max_zoom: 10})
    var index = tileCover.indexes(geojson.features[i].geometry, {min_zoom: min, max_zoom: max});
    obj.push({geoid: geojson.features[i].properties[geoid], qtid: index})
}

var json = JSON.stringify(obj);
fs.writeFile (output, json, (err) => {
    if (err) {
	console.error(err);
	return;
    };
    console.log('complete');
});
